from abc import ABC, abstractmethod
from .hints import Skill, SkillCode

class AbstractWorkspace(ABC):

    @abstractmethod
    def execute_raw(self, data:str, parse_return_value:bool=False, request_reply:bool=True, timeout:int=-1) -> any:
        return NotImplemented