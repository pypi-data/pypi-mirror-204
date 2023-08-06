"""
This module provides SKILL function abstractions and
multiple functions (collections) for remote execution.

Internal package - does not need to be used
"""

from typing import List
from functools import lru_cache

from .hints import SkillCode, Skill, Key
from .abstract_translator import AbstractTranslator

class FunctionCollection:
    """
    Dictionary of remote function objects. This collection contains all functions.
    Contents are looked up in Virtuoso and cached for later usage
    """
    def __init__(self, ws, translator: AbstractTranslator):
        self._workspace = ws
        self._translate = translator

    def __repr__(self) -> str:
        """
        Print the list of functions nicely
        """
        return f"<function collection*>\n{dir(self)}"

    @lru_cache(maxsize=128)
    def __dir__(self) -> List[str]:
        """
        Create command to query list of functions and execute it, afterwards cache the results.
        """
        command = self._translate.encode_globals("^[A-Za-z]")  # all functions
        result = self._workspace.execute_raw(command, parse_return_value=False)
        return self._translate.decode_globals(result)

    def __getattr__(self, item: str) -> 'RemoteFunction':
        """
        Looking up the function in the dictionary returns the function object
        """
        return RemoteFunction(self._workspace, item, self._translate)


class RemoteFunction:
    """
    Function object for function that can be executed in Virtuoso
    """
    def __init__(self, ws, func: str, translator: AbstractTranslator):
        self._workspace = ws
        self._translate = translator
        self._function = func

    def __call__(self, *args: Skill, **kwargs: Skill) -> Skill:
        """
        Call function in Virtuoso using the channel and return the result
        """
        command = self.lazy(*args, **kwargs)
        return self._workspace.execute_raw(command, parse_return_value=True)

    def lazy(self, *args: Skill, **kwargs: Skill) -> SkillCode:
        """
        Create function call for Virtuoso, but do not call it
        """
        return self._translate.encode_call(self._function, *args, **kwargs)

    def __repr__(self) -> str:
        """
        Print the function help instead of calling it
        """
        command = self._translate.encode_help(self._function)
        result = self._workspace.execute_raw(command, parse_return_value=False)
        return self._translate.decode_help(result)
