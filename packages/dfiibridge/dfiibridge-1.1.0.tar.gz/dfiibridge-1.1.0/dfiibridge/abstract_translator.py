from abc import ABC, abstractmethod
from typing import Callable
from .hints import Skill, SkillCode

class ParseError(Exception):
    pass

class AbstractTranslator(ABC):

    def __init__(self, execute_raw : Callable) -> None:
        self.execute_raw = execute_raw

    @abstractmethod
    def encode_call(self, func_name: str, *args: Skill, **kwargs: Skill) -> SkillCode:
        return NotImplemented

    @abstractmethod
    def encode_dir(self, obj: SkillCode) -> SkillCode:
        return NotImplemented

    @abstractmethod
    def decode_dir(self, code: str) -> list[str]:
        return NotImplemented

    @abstractmethod
    def encode_getattr(self, obj: SkillCode, key: str) -> SkillCode:
        return NotImplemented

    @abstractmethod
    def encode_globals(self, filter_regex: str) -> SkillCode:
        return NotImplemented

    @abstractmethod
    def decode_globals(self, code: str) -> list[str]:
        return NotImplemented

    @abstractmethod
    def encode_help(self, symbol: str) -> SkillCode:
        return NotImplemented

    @abstractmethod
    def decode_help(self, help_: str) -> str:
        return NotImplemented

    @abstractmethod
    def encode_setattr(self, obj: SkillCode, key: str, value: any) -> SkillCode:
        return NotImplemented

    @abstractmethod
    def encode(self, value: Skill) -> SkillCode:
        return NotImplemented

    @abstractmethod
    def decode(self, code: str) -> Skill:
        return NotImplemented