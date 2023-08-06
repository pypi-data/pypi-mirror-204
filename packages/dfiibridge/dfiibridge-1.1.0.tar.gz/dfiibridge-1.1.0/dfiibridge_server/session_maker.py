import time
import json
import subprocess
import os
import re
import sys
from select import select
from typing import Callable

from .globals import DFII_LABEL_PATTERN, COMMAND_VIRTUOSO, DFII_SERVER_PY, DFII_SERVER_SKILL
class TimeoutException(Exception):
    pass
class DfiiBridgeServerNotStartedException(Exception):
    pass

def data_available_with_timeout(stream, timeout):
    """
    This is to check if output is available,
    before actually calling read/readline,
    so that non-blocking reads can be achieved.
    """
    readable, _, _ = select([stream], [], [], timeout)

    return bool(readable)
class SessionMaker:
    """
    Class that provides methods for session creation.
    """

    @staticmethod
    def create_session(no_cdsinit:bool=False,
                       no_gui:bool=False,
                       cmd:Callable=None,
                       env:dict=None,
                       session_root:str=None,
                       extra_fields:dict=None,
                       python_executable:str=None):
        """
        Start a Virtuoso session, inside or outside of Camino (depending on using_camino).
        """

        # build virtuoso command string
        init = "-nocdsinit" if no_cdsinit else ""
        gui = "-nograph" if no_gui else ""

        if cmd is None:
            cmd = COMMAND_VIRTUOSO

        command_virtuoso_f = cmd(
            init=init,
            gui=gui,
            path_to_skill_server=DFII_SERVER_SKILL
        )

        if env is None:
            env = os.environ.copy()  # Use current environment
        if extra_fields is None:
            extra_fields = {}
        if python_executable is None:
            python_executable = sys.executable

        # Update path to the executable
        env["DFIIBRIDGE_DFII_SERVER"] = python_executable + " " + DFII_SERVER_PY
        env["DFIIBRIDGE_EXTRA"] = json.dumps(extra_fields)
        if session_root is not None:
            env["DFIIBRIDGE_SESSION_ROOT"] = session_root

        # start the process and return the created process
        print(f"Starting: {command_virtuoso_f}")

        proc = subprocess.Popen(
            command_virtuoso_f,
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE, # we also need stdin because otherwise the normal stdin is messed up
            stderr=subprocess.STDOUT,
            env=env
        )
        return proc

    @staticmethod
    def _wait_for_file(caller_self, session_manager, session_adress_status, on_output):
        # look for the session file so we can read it
        session_file = session_manager.get_session_file_path(session_adress_status['hostname'],
                                                             int(session_adress_status['port']),
                                                             False)

        # wait until session file becomes alive
        if on_output:
            on_output(caller_self, "Waiting until sessionfile available...\n")

        w = 0
        while os.path.exists(session_file) == False:
            time.sleep(1)
            w += 1

            if w > 30:  # longer than 30sec => error
                raise TimeoutException("Timeout while waiting for sessionfile...")

        # the session file is available, so we can now get the real session object
        return session_manager.get_session(session_file, False)

    @staticmethod
    def wait_for_session(proc, session_manager, caller_self=None, on_output=None):
        """
        Wait for the session to start. The process was already created.
        """
        # wait until the process completes
        while True:
            # check if the process is still alive
            if proc.poll() is not None:
                break

            # check if data is available on process' stdout
            if data_available_with_timeout(proc.stdout, 240):

                # read from stdout now that output is available
                out = proc.stdout.readline().decode("utf-8")

                # try to find the session creation pattern
                m = re.findall(DFII_LABEL_PATTERN, out)

                if m:
                    # convert it into dictionary and emits it as new created session.
                    # Python server sends string beginning with '%%%DfiiBridge%%%' label
                    # followed by a dictionary.
                    session_adress_status = {
                        "hostname": m[0][0],
                        "port": m[0][1],
                        "status": m[0][2]
                    }

                    # get session data on success
                    if session_adress_status["status"] == "OK":

                        # notify about success
                        if on_output:
                            on_output(caller_self, "Session Status OK\n")

                        # return session object
                        return SessionMaker._wait_for_file(caller_self, session_manager, session_adress_status, on_output)
                    else:
                        # status was not OK, return None (failure)
                        raise DfiiBridgeServerNotStartedException(f"Status of server: {session_adress_status['status']}")

                else:
                    # call output handler, if available
                    if on_output:
                        on_output(caller_self, out)

            else:
                # call stdout wait timeout handler, if available
                raise TimeoutException("Timeout while waiting for output...")

        # If the session was not started successfully (wherever we exited the while loop),
        # we kill the session manually.
        raise DfiiBridgeServerNotStartedException("DfiiBridgeServer and/or Virtuoso could not be started!")
