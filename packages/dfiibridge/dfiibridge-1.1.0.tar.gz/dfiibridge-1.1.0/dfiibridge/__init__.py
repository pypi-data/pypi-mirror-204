"""
Python API for executing commands in a remote virtuoso session

- allows to connect to virtuoso session running on remote machine
- manages virtuoso sessions in ~/.dfiiBridge
- adds user authentication to command execution to prevent unauthorized users
  from using the command interface

The most relevant objects are:

- sessions.VirtuosoSessionManager to list sessions and to connect to them
- workspace.Workspace to execute skill commands in the remote session
"""

from .workspace import Workspace
from .sessions import VirtuosoSessionManager, Session

from .logger import configure_logger, LOGGER_FILE_NAME, LOGGER_NAME
from .callback_decorator import callback, skill_callback, log_callback
