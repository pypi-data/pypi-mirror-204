"""
This module provides object translation between SKILL and Python

Internal package - does not need to be used
"""

from typing import NoReturn, Any, List, Iterable, cast
from json import dumps, loads
from warnings import warn_explicit

from .hints import SkillCode, Skill, Symbol
from .abstract_translator import AbstractTranslator
from .abstract_workspace import AbstractWorkspace
from .objects import RemoteObject, RemoteTable, RemoteVector


class Translator(AbstractTranslator):

    def _raise_error(message: str) -> NoReturn:
        raise ParseError(message)

    def _show_warning(self, message: str, result: Any) -> Any:
        for i, line in enumerate(message.splitlines(keepends=False)):
            warn_explicit(line.lstrip("*WARNING*"), UserWarning, "Skill response", i)

        return result

    def _skill_value_to_python(self, string: str) -> Skill:
        return eval(  # type: ignore
            string,
            {
                'Remote': lambda skill_string: RemoteObject(skill_string, self),
                'Table': lambda skill_string: RemoteTable(skill_string, self),
                'Vector': lambda skill_string: RemoteVector(skill_string, self),
                'Symbol': Symbol,
                'error': self._raise_error,
                'warning': self._show_warning
            }
        )

    def _python_value_to_skill(self, value: Skill, is_on_top_level:bool=True) -> SkillCode:
        """
        When "is_on_top_level" is True, we inject a call to DfiiBridge__pyReconstructSkillObjects,
        so that SKILL evaluates the symbols starting from the top level.
        For all nested/deeper elements this variable is false to continue with regular processing.
        """
        try:
            return value.__repr_skill__()  # type: ignore
        except AttributeError:
            pass

        if isinstance(value, dict):
            items = ' '.join(f"{key} {self._python_value_to_skill(value, is_on_top_level=False)}" for key, value in value.items())
            if not is_on_top_level:
                return SkillCode(f'(nil {items})')
            return SkillCode(f'DfiiBridge__pyReconstructSkillObjects(\'(nil {items}))')

        if value is False or value is None:
            return SkillCode('nil')

        if value is True:
            return SkillCode('t')

        if isinstance(value, (int, float, str)):
            return SkillCode(dumps(value))

        if isinstance(value, (list, tuple)):
            inner = ' '.join(self._python_value_to_skill(item, is_on_top_level=False) for item in value)
            if not is_on_top_level:
                return SkillCode(f'({inner})')
            return SkillCode(f'DfiiBridge__pyReconstructSkillObjects(\'({inner}))')

        type_ = type(value).__name__
        raise RuntimeError(f"Cannot convert object {type_!r} to skill.") from None

    def build_skill_path(self, components: Iterable[str]) -> SkillCode:
        it = iter(components)
        path = str(next(it))

        for component in it:
            if isinstance(component, int):
                path = f'(nth {component} {path})'
            else:
                path = f'{path}->{component}'

        return SkillCode(path)


    def build_python_path(self, components: Iterable[str]) -> SkillCode:
        it = iter(components)
        path = str(next(it))

        for component in it:
            if isinstance(component, int):
                path = f'{path}[{component}]'
            else:
                path = f'{path}.{component}'

        return SkillCode(path)


    def encode_call(self, func_name: str, *args: Skill, **kwargs: Skill) -> SkillCode:
        args_code = ' '.join(map(self._python_value_to_skill, args))
        kw_keys = kwargs
        kw_values = map(self._python_value_to_skill, kwargs.values())
        kwargs_code = ' '.join(f'?{key} {value}' for key, value in zip(kw_keys, kw_values))
        return SkillCode(f'{func_name}({args_code} {kwargs_code})')

    def encode_dir(self, obj: SkillCode) -> SkillCode:
        parts = ' '.join(
            (
                f'{obj}->?',
                f"if( type({obj}) == 'rodObj then {obj}->systemHandleNames)",
                f'if( type({obj}) == \'rodObj then {obj}->userHandleNames)',
            )
        )
        code = f'mapcar(lambda((attr) sprintf(nil "%s" attr)) nconc({parts}))'
        return SkillCode(code)

    def decode_dir(self, code: str) -> List[str]:
        attributes = self._skill_value_to_python(code) or ()
        return [attr for attr in cast(List[str], attributes)]

    def encode_getattr(self, obj: SkillCode, key: str) -> SkillCode:
        return self.build_skill_path([obj, key])

    def encode_globals(self, filter_regex: str) -> SkillCode:
        return SkillCode(f'buildString(listFunctions("{filter_regex}"))')

    def decode_globals(self, code: str) -> List[str]:
        return [f for f in loads(code).split()]

    def encode_help(self, symbol: str) -> SkillCode:
        code = f"""
            _text = outstring()
            poport = _text help({symbol})
            poport = stdout getOutstring(_text)
        """.replace(
            "\n", " "
        )
        return SkillCode(code)

    def decode_help(self, help_: str) -> str:
        return loads(help_)  # type: ignore

    def encode_setattr(self, obj: SkillCode, key: str, value: Any) -> SkillCode:
        code = self.build_skill_path([obj, key])
        value = self._python_value_to_skill(value)
        return SkillCode(f'{code} = {value}')

    def encode(self, value: Skill) -> SkillCode:
        return self._python_value_to_skill(value)

    def decode(self, code: str) -> Skill:
        return self._skill_value_to_python(code)

