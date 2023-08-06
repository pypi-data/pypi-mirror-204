#!/usr/bin/env python3
"""
Python server that receives requests and, if they are valid, executes them in virtuoso.
"""

import sys
from sys import stdout, stdin, stderr
import os
import re
from argparse import ArgumentParser
import subprocess
import json
import datetime
import glob

from dfiibridge_server.helpers import execute_inside_skill
from dfiibridge import VirtuosoSessionManager
from dfiibridge_core import DfiiBridgeServer, RemoteCallback, LoggingCallback, CoreSessionManager
from dfiibridge import callback, log_callback
import dfiibridge_server

import logging
import signal
import sys


global log_file_name, log_level
log_file_name: str = None
log_level:int = 30

@callback
def get_server_loglevel(ws) -> str:
    """ Get the loglevel
    """
    global log_level
    return str(log_level)

@callback
def set_server_loglevel(ws, _log_level:str) -> str:
    """ Set the loglevel
    """
    global log_level
    log_level = int(_log_level)
    execute_inside_skill(f"DfiiBridge['server]['verbosity] = {log_level}")
    write_to_log(f"[INFO] Setting dfiibridge server loglevel to {log_level}")
    return "True"

@log_callback
def log(log_level_in, log_message):
    """ Logging callback (see https://docs.python.org/3/library/logging.html#logging-levels)
        10: Critical + Error + Warning + Debug + Info messages
        20: Critical + Error + Warning + Debug        messages
        30: Critical + Error + Warning                messages
        40: Critical + Error                          messages
        50: Critical                                  messages
    """
    global log_level

    if log_level > log_level_in:
        return

    write_to_log(f"{datetime.datetime.now()} {log_level_in}: {log_message}\n")

@callback
def skill(ws, skill_code:str) -> str:
    return execute_inside_skill(skill_code)


def write_to_log(msg:str, mode:str="a"):
    global log_file_name

    with open(log_file_name, mode) as f:
        f.write(msg.strip()+"\n")

def cleanup_log(csm : CoreSessionManager):
    """Clean up the session directory of old log files

    Args:
        csm: Session Manager
    """
    root = csm.get_root_directory()
    logs = list(glob.glob(os.path.join(root, "*.log")))
    # Create a list with (file name, modification time stamp)
    files = [(log_file, os.stat(log_file).st_mtime) for log_file in logs]
    # Sort for modification time stamp (newest one is at 0)
    files.sort(key=lambda entry: entry[1], reverse=True)

    # Do not allow more than 10 log files -> remove oldest ones
    if len(files)>10:
        for file in files[-10:]:
            try:
                os.remove(file[0])
            except Exception:
                continue # jump of non-deletable files

class VirtuosoServer:

    def __init__(self, session_dir:str, verbosity:int, user_data:str, cds_log_path:str):
        """ VirtuosoServer
        Extend this class and define our custom userdata structure for your design environment.
        """
        global log_file_name, log_level

        log_level = int(verbosity)

        csm = CoreSessionManager(session_dir)

        cleanup_log(csm)

        # Additional extra fields can be passed by the environment variable $DFIIBRIDGE_EXTRA
        # It can be set in the session_maker.py create_session() function call
        extra_fields = json.loads(user_data)

        # Add the cds log path
        extra_fields.update({"cds_log": cds_log_path})

        self.server = DfiiBridgeServer(csm, {
                "type": "virtuoso",
                **extra_fields
            })

        # Register the skill callback handler
        log_file_name = csm.get_log_file_path(self.server.get_hostname(), self.server.get_port())

        write_to_log(f"""
##################################################################################################
########################################### DfiiBridge ###########################################
##################################################################################################
    Server started:          {datetime.datetime.now()}
    Hostname:                {self.server.get_hostname()}
    Port:                    {self.server.get_port()}
    Log file:                {log_file_name}
    Session directory:       {session_dir}
    Session file:            {self.server.get_session_file_path()}
    Verbosity:               {verbosity}
    DfiiBridge-Tool-Version: {dfiibridge_server.__version__}
##################################################################################################""", mode="w")

        self.server.register_function("skill", skill)
        self.server.register_function("set_server_loglevel", set_server_loglevel)
        self.server.register_function("get_server_loglevel", get_server_loglevel)
        self.server.register_logging_function(log)

        # Save session information for skill
        execute_inside_skill(f"DfiiBridge['server]['log] = \"{log_file_name}\"")
        execute_inside_skill(f"DfiiBridge['server]['hostname] = \"{self.server.get_hostname()}\"")
        execute_inside_skill(f"DfiiBridge['server]['port] = {self.server.get_port()}")
        execute_inside_skill(f"DfiiBridge['server]['session_file] = \"{self.server.get_session_file_path()}\"")
        execute_inside_skill(f"setShellEnvVar(\"DFIIBRIDGE_VIRTUOSO_SESSION_FILE\" \"{self.server.get_session_file_path()}\")")

        # Echo for Session Manager GUI
        execute_inside_skill("""system("echo [INFO] DfiiBridge running on """ +
                            f"""{self.server.get_hostname()}:{self.server.get_port()} status:OK")""")

        sys.stdout.flush()

    def listen(self):
        """Start listening
        """
        try:
            self.server.listen() # blocking
        except RuntimeError as e:
            print(f"[ERROR] DfiiBridge encountered an error: {e}")
            write_to_log(f"[ERROR] DfiiBridge encountered an error: {e}")
            raise
        except Exception as e:
            write_to_log(f"[INFO] {e}. This exception is okay, if the server is being terminated by the user.")

        server.stop()

        print("[INFO] DfiiBridge terminates now.")

    def stop(self):
        self.server.unregister_logging_function(log)
        self.server.stop()
        write_to_log("[INFO] Server stopped.")

if __name__ == '__main__':

    argument_parser = ArgumentParser(sys.argv[0])
    argument_parser.add_argument('--session_dir',
                                type=str,
                                default=os.path.join(os.environ["HOME"], ".dfiiBridge"),
                                help='Directory to store the session file (default: ~/.dfiiBridge)')
    argument_parser.add_argument('--user_data',
                                type=str,
                                default="{}",
                                help='User data that is attached to the session, e.g. project information (default: {})')
    argument_parser.add_argument('--cdslog',
                                type=str,
                                default="",
                                help='Path to the cdslog file of the current session (default: "")')

    argument_parser.add_argument('-v', '--verbose', default=30, help="Set the veribosity level")

    args = argument_parser.parse_args()

    server = VirtuosoServer(args.session_dir, args.verbose, args.user_data, args.cdslog)
    server.listen()

