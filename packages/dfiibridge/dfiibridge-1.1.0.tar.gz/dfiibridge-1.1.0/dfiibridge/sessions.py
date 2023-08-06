import logging
import os
from typing import Callable, List

from dfiibridge_core import CoreSessionManager, Session

from .workspace import Workspace
from .logger import LOGGER_NAME

from dfiibridge_server.session_maker import SessionMaker


logger = logging.getLogger(LOGGER_NAME)


class VirtuosoSessionManager(CoreSessionManager):

    def get_workspace(self, session: Session = None) -> Workspace:
        """
        Returns a workspace object for the remote session

        .. highlight:: python
        .. code-block:: python

            from DfiiBridge import VirtuosoSessionManager

            # first create an instance of the SessionManager
            session_manager = VirtuosoSessionManager()

            # Connect to the session of the current project (if available)
            ws = session_manager.get_workspace()

            # Get all sessions manually and select one
            sessions = session_manager.find_sessions(True)
            ws = session_manager.get_workspace(sessions[0])

        """
        # If no session is given try all sessions of the current project
        # Make sure to remove invalid session files
        # this should be done------
        if session is None:
            session = self.find_virtuoso_session_from_env()
            return self.get_workspace(session)

        if isinstance(session, Session):
            return Workspace(session)

        raise Exception(f"Unsupported argument type of {session}")

    def kill_session(self, session: Session):
        """Kill a session safely

        Args:
            session: Session to be killed
        """
        ws = self.get_workspace(session)
        if not ws.execute_raw('DfiiBridge__safeExit( )', request_reply=True, timeout=1000):
            raise Exception("DfiiBridge__safeExit() call returned False. Please report this bug.")

        self.delete_session_file(session)

    def create_virtuoso_workspace(self,
                                  no_cdsinit:bool=False,
                                  no_gui:bool=False,
                                  cmd:Callable=None,
                                  python_executable:str=None,
                                  env:dict=None,
                                  extra_fields:dict=None,
                                  on_output:Callable=None)->Workspace:
        """Create a new Virtuoso session and connect to it

        Args:
            no_cdsinit (bool, optional): Start Virtuoso with the nocdsinit flag. Defaults to False.
            no_gui (bool, optional): Start Virtuoso with the nogui flag. Defaults to False.
            cmd (Callable, optional): Override command to start Virtuoso (lambda returning a list that is passed to Popen()). Defaults to None.
            env (dict, optional): Override the environment to be used. Defaults to None (taking os.environ.copy()).
            extra_fields (dict, optional): Add additional fields to the server. Defaults to None.
            on_output (Callable, optional): Add callback to capture stdout of the subprocess. Defaults to None (printing on stdout).

        Returns:
            Workspace: The workspace object
        """

        proc = SessionMaker.create_session(no_gui=no_gui,
                                           no_cdsinit=no_cdsinit,
                                           cmd=cmd,
                                           env=env,
                                           session_root=self.get_root_directory(),
                                           extra_fields=extra_fields,
                                           python_executable=python_executable)

        if on_output is None:
            on_output_callback = lambda _, msg: print(msg, end="")
        else:
            on_output_callback = on_output

        session = SessionMaker.wait_for_session(proc, self,  on_output=on_output_callback)
        return self.get_workspace(session)

    def find_virtuoso_sessions(self, connection_check:bool=True) -> list[Session]:
        """Find all available virtuoso sessions

        Args:
            connection_check (bool, optional): Check connection before returning. Defaults to True.

        Returns:
            list[Session]: List of valid virtuoso sessions
        """
        search_criteria = {"type": "virtuoso"}
        return self.find_sessions(search_criteria, connection_check)


    def find_virtuoso_session_from_env(self, connection_check:bool=True) -> Session:
        """
        Find a session by reading the $DFIIBRIDGE_VIRTUOSO_SESSION_FILE environment variable.
        Useful, if you start a terminal from within Virtuoso and you want
        to connect to exactly this Virtuoso session.
        """
        session_file = os.getenv("DFIIBRIDGE_VIRTUOSO_SESSION_FILE", default="")

        if session_file:
            logger.info(f"Read session from $DFIIBRIDGE_VIRTUOSO_SESSION_FILE = {session_file}")
            return self.get_session(session_file, connection_check)

        raise Exception(f"The environmentvariable $DFIIBRIDGE_VIRTUOSO_SESSION_FILE not found. Was this shell started from within Virtuoso?")
