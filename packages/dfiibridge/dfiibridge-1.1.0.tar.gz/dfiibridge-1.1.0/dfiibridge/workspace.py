"""
This module provides the remote workspace
"""

from typing import Optional, Callable, Any, Iterable, cast
from json import dumps
from inspect import signature
from textwrap import dedent
from dfiibridge_core import DfiiBridgeClient, Session, LoggingCallback

from .hints import SkillCode, Skill, Function, Symbol
from .functions import FunctionCollection, RemoteFunction
from .translator import Translator
from .logger import SimpleStdoutLogger
from .abstract_workspace import AbstractWorkspace

def _python_value_to_skill(value: Skill, is_on_top_level:bool=True) -> SkillCode:
    """
    When "is_on_top_level" is True, we inject a call to __pyReconstructSkillObjects,
    so that SKILL evaluates the symbols starting from the top level.
    For all nested/deeper elements this variable is false to continue with regular processing.
    """
    try:
        return value.__repr_skill__()  # type: ignore
    except AttributeError:
        pass

    if isinstance(value, dict):
        items = ' '.join(f"{key} {_python_value_to_skill(value, is_on_top_level=False)}" for key, value in value.items())
        if not is_on_top_level:
            return SkillCode(f'(nil {items})')
        return SkillCode(f'__pyReconstructSkillObjects(\'(nil {items}))')

    if value is False or value is None:
        return SkillCode('nil')

    if value is True:
        return SkillCode('t')

    if isinstance(value, (int, float, str)):
        return SkillCode(dumps(value))

    if isinstance(value, (list, tuple)):
        inner = ' '.join(_python_value_to_skill(item, is_on_top_level=False) for item in value)
        if not is_on_top_level:
            return SkillCode(f'({inner})')
        return SkillCode(f'__pyReconstructSkillObjects(\'({inner}))')

    type_ = type(value).__name__
    raise RuntimeError(f"Cannot convert object {type_!r} to skill.") from None

def encode_call(func_name: str, *args: Skill, **kwargs: Skill) -> SkillCode:
    args_code = ' '.join(map(_python_value_to_skill, args))
    kw_keys = kwargs
    kw_values = map(_python_value_to_skill, kwargs.values())
    kwargs_code = ' '.join(f'?{key} {value}' for key, value in zip(kw_keys, kw_values))
    return SkillCode(f'{func_name}({args_code} {kwargs_code})')

class Workspace(AbstractWorkspace):

    def __init__(self, session: Session):
        self.session = session
        self._client = DfiiBridgeClient()
        self._client.connect_to_endpoint(session) # connect to remote session

        self._translator = Translator(self.execute_raw)
        self.timeout = -1
        # add function collection "skill" to the workspace
        # usage: self.skill.functionName(...)
        setattr(self, "skill", FunctionCollection(self, self._translator))

    def set_origin_session(self, session: Session):
        """Register the origin session so that you can call Python function from
        skill via DfiiBridgeClient_executeCommand().

        Args:
            session: Session of the server that runs on the client side
        """
        self._client.set_origin_session(session)

    def set_timeout(self, timeout:int):
        """
        Set the timeout (in seconds) of the tcp connection between client and Virtuoso server.
        Timeout = -1 removes the timeout
        """
        self.timeout = timeout

    def clear_timeout(self):
        """Set the timeout to -1 and therefore disable it"""
        self.timeout = -1

    def get_virtuoso_verbosity(self) -> int:
        """ Get the verbosity of the virtuoso server.
        """
        return int(self._client.execute("get_server_loglevel", [])[0])

    def set_virtuoso_verbosity(self, verbosity:int):
        """ Set the verbosity of the virtuoso server.
        More messages lead to slower speed because of logging overhead.

        10: Critical + Error + Warning + Debug + Info messages
        20: Critical + Error + Warning + Debug        messages
        30: Critical + Error + Warning                messages
        40: Critical + Error                          messages
        50: Critical                                  messages
        """
        self._client.execute("set_server_loglevel", [str(verbosity)])

    def enable_debug_mode(self):
        """
        Enable verbose mode for client and server
        """
        # Increase verbosity on the server side
        self.set_virtuoso_verbosity(10)
        self._simple_logger = SimpleStdoutLogger()
        self.register_logger(self._simple_logger)

    def register_logger(self, logger:LoggingCallback):
        """
        Register a logger for the client (must be an instance of the subclass of LoggingCallback).
        """
        self._client.register_logging_function(logger)

    def __getitem__(self, item: str) -> RemoteFunction:
        """
        The workspace can be used like a dictionary to return a function object.
        """
        return RemoteFunction(self, item, self._translator)

    def execute(self, func_name: str, *args, **kwargs) -> any:
        """
        Executes a remote SKILL function with arguments 'args' and returns the result
        """
        return self.__getitem__(func_name)(*args, **kwargs)

    def execute_raw(self, data:str, parse_return_value:bool=False, request_reply:bool=True, timeout:int=None) -> any:

        if timeout is None:
            timeout = self.timeout

        if parse_return_value and not request_reply:
            raise Exception("You can only parse the return value if you are also receiving it!")

        # There should be one or none response
        ret = self._client.execute("skill", [data], request_reply, timeout)

        if request_reply:
            parsed_ret = self.parse_response(ret[0]) # Evaluate success/fail message
            if parse_return_value:
                return self._translator.decode(parsed_ret)
            return parsed_ret.strip() # Strip whitespace (\n at end of line)
        return None # Return nothing if no return is expected

    def set(self, var_name:str, value:any) -> None:
        """
        Define a variable on the skill side
        """
        cmd = f"{var_name} = {self._translator.encode(value)}"
        self.execute_raw(data=cmd, request_reply=True)

    def get(self, var_name:str) -> any:
        """
        Get a variable on the skill side
        """
        return self.execute_raw(data=var_name, parse_return_value=True, request_reply=True)

    def define(self, name: str, args: Iterable[str], code: str) -> None:
        """
        Define a function on the skill side.
        """
        code = code.replace('\n', ' ')
        arg_list = ' '.join(args)
        code = f'defun(user{name} ({arg_list}) {code})'
        cast(Symbol, self._translator.decode(self.execute_raw(code)))

    @staticmethod
    def parse_response(response: str) -> str:
        """
        Parse the string response from virtuoso.
        It contains the status (True/False), which is stripped from the response.
        """
        if response.startswith("failure "):
            _, err_msg = response.split(' ', maxsplit=1)
            raise RuntimeError(err_msg)

        return response

    @staticmethod
    def fix_completion() -> None:
        try:
            ipy = get_ipython()  # type: ignore
        except NameError:
            pass
        else:
            ipy.Completer.use_jedi = False
            ipy.Completer.greedy = True

    @staticmethod
    def _build_function(function: Callable[..., Any]) -> Function:
        if not function.__doc__:
            raise RuntimeError("Function does not have a doc string.")

        s = signature(function)

        if s.return_annotation is s.empty:
            raise RuntimeError("Function does not have a return annotation.")

        param_doc = []
        for p in s.parameters.values():
            if p.default is p.empty:
                param = p.name

                if p.annotation is Optional:
                    param = f"    [ {param} ]"
                else:
                    param = f"    {param}"
            else:
                param = f"    [ ?{p.default} {p.name} ]"

            param_doc.append(param)

        doc = [
            function.__name__ + "(",
            *param_doc,
            f"=> {'nil' if s.return_annotation is None else s.return_annotation}",
            "",
        ]

        doc_string = '\n'.join(doc) + dedent(function.__doc__)

        return Function(function.__name__, doc_string, set())
