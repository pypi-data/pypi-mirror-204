"""
This module provides object mapping between SKILL and Python

Internal package - does not need to be used
"""

from typing import Any, List, Optional, cast, Union, overload, Sequence, Iterable, MutableMapping, Iterator, Callable

from .functions import RemoteFunction
from .hints import SkillCode, Symbol, Var, Skill
from .abstract_translator import AbstractTranslator, ParseError

def is_jupyter_magic(attribute: str) -> bool:
    ignore = {
        '_ipython_canary_method_should_not_exist_',
        '_ipython_display_',
        '_repr_mimebundle_',
        '_repr_html_',
        '_repr_markdown_',
        '_repr_svg_',
        '_repr_png_',
        '_repr_pdf_',
        '_repr_jpeg_',
        '_repr_latex_',
        '_repr_json_',
        '_repr_javascript_',
        '_rapped',
        '__wrapped__',
        '__call__',
    }
    return attribute in ignore


class RemoteVariable:
    _attributes = {'_execute_raw', '_variable', '_translate'}

    def __init__(self, variable: str, translator: AbstractTranslator) -> None:
        self._execute_raw = translator.execute_raw
        self._variable = SkillCode(variable)  # example "__py_db_0x2259de1a"
        self._translate = translator

    def __repr_skill__(self) -> SkillCode:
        return SkillCode(self._variable)

    def _send(self, command: SkillCode) -> Any:
        return self._execute_raw(command).strip()

    def __repr__(self) -> str:
        return self.__str__()

    def _call(self, function: str, *args: Skill, **kwargs: Skill) -> Skill:
        code = self._translate.encode_call(function, *args, **kwargs)
        result = self._send(code)
        return self._translate.decode(result)

    def __dir__(self) -> Iterable[str]:
        response = self._send(self._translate.encode_dir(self._variable))
        attributes = self._translate.decode_dir(response)
        return attributes

class RemoteObject(RemoteVariable):

    @property
    def skill_id(self) -> int:
        addr = self._variable[5:].rsplit('_', maxsplit=1)[1]  # "__py_db_0x2259de1a" -> "0x2259de1a"
        return addr

    @property
    def skill_parent_type(self) -> str:
        return self._variable[5:].rsplit('_', maxsplit=1)[0]

    def _is_open_file(self) -> bool:
        return self._variable.startswith('__py_openfile_')

    @property
    def skill_type(self) -> Optional[str]:
        if self._is_open_file():
            return 'open_file'

        try:
            typ = self.obj_type
        except RuntimeError:
            return None
        if typ is None:
            return None
        if isinstance(typ, Symbol):
            return typ.name[2:-4]
        return cast(str, typ)

    def __str__(self) -> str:
        typ = self.skill_type or self.skill_parent_type
        if typ == 'open_file':
            result = self._send(self._translate.encode_call('sprintf', None, '%s', self))
            name = self._translate.decode(result)[6:-1]  # type: ignore
            return f"<remote open_file {name!r}>"
        return f"<remote {typ}@{self.skill_id}>"

    def __dir__(self) -> Iterable[str]:
        if self._is_open_file():
            return super().__dir__()

        response = self._send(self._translate.encode_dir(self._variable))
        attributes = self._translate.decode_dir(response)
        return attributes

    def __getattr__(self, key: str) -> Any:
        if is_jupyter_magic(key):
            raise AttributeError(key)

        result = self._send(self._translate.encode_getattr(self._variable, key))
        return self._translate.decode(result)

    def __setattr__(self, key: str, value: Any) -> None:
        if key in RemoteObject._attributes:
            return super().__setattr__(key, value)

        result = self._send(self._translate.encode_setattr(self._variable, key, value))
        self._translate.decode(result)

    def getdoc(self) -> str:
        return "Properties:\n- " + '\n- '.join(dir(self))

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, RemoteObject):
            return self._variable == other._variable
        return NotImplemented

    def __ne__(self, other: Any) -> bool:
        if isinstance(other, RemoteObject):
            return self._variable != other._variable
        return NotImplemented

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        command = self._translate.encode_call('funcall', self, *args, **kwargs)
        result = self._send(code)
        return self._translate.decode(result)

    @property
    def lazy(self) -> 'LazyList':
        return LazyList(self._variable, self._translate)


class LazyList(RemoteVariable):
    arg = Var('arg')

    def __getattr__(self, attribute: str) -> 'LazyList':
        variable = SkillCode(f"{self._variable}~>{attribute}")
        return LazyList(variable, self._translator)

    def __str__(self) -> str:
        return f"<lazy list {self._variable}>"

    @staticmethod
    def _condition(filters: Sequence[SkillCode]) -> SkillCode:
        if len(filters) == 1:
            return SkillCode(f'arg->{filters[0]}')
        parameters = ' '.join(f'arg->{f}' for f in filters)
        return SkillCode(f'and({parameters})')

    def filter(self, *args: str, **kwargs: Any) -> 'LazyList':
        if not args and not kwargs:
            return self

        arg_filters = [SkillCode(arg) for arg in args]
        kwarg_filters = [
            SkillCode(f"{key} == {self._translator.encode(value)}")
            for key, value in kwargs.items()
        ]
        filters = self._condition(arg_filters + kwarg_filters)
        variable = SkillCode(f'setof(arg {self._variable} {filters})')

        return LazyList(variable, self._translator)

    @overload
    def __getitem__(self, item: int) -> RemoteObject:
        ...  # pragma: nocover

    @overload  # noqa
    def __getitem__(self, item: slice) -> List[RemoteObject]:  # noqa
        ...  # pragma: nocover

    def __getitem__(self, item: Union[int, slice]) -> Union[RemoteObject, List[RemoteObject]]:  # noqa
        if isinstance(item, int):
            code = self._translator.encode_call('nth', item, Var(self._variable))
        else:
            if item.start is not None or item.stop is not None or item.step is not None:
                raise RuntimeError("cannot slice lazy list with arbitrary bounds")

            code = self._variable

        result = self._send(code)
        return self._translator.decode(result)  # type: ignore

    def __len__(self) -> int:
        code = self._translator.encode_call('length', Var(self._variable))
        return self._translator.decode(self._send(code))  # type: ignore

    def foreach(self, func: Union['RemoteFunction', SkillCode], *args: Any) -> None:
        if isinstance(func, RemoteFunction):
            args = args or (LazyList.arg,)
            func = func.lazy(*args)
        elif args:
            raise RuntimeError("cannot combine args with remote function")

        code = self._translator.encode_call('foreach', LazyList.arg, Var(self._variable), Var(func))
        result = self._send(code + ',nil')
        self._translator.decode(result)



class RemoteCollection(RemoteVariable):
    def __str__(self) -> str:
        return f'<remote {self._call("lsprintf", "%L", self)}>'

    def __len__(self) -> int:
        return cast(int, self._call('length', self))

    def __getitem__(self, item: Skill) -> Skill:
        return self._call('arrayref', self, item)

    def __setitem__(self, key: Skill, value: Skill) -> None:
        self._call('setarray', self, key, value)

    def __delitem__(self, item: Skill) -> None:
        self._call('remove', item, self)

class RemoteTable(RemoteCollection, MutableMapping[Skill, Skill]):
    def __getitem__(self, item: Skill) -> Skill:
        try:
            return super().__getitem__(item)
        except ParseError:
            raise KeyError(item) from None

    def __getattr__(self, item: str) -> Skill:
        return self[Symbol(item)]

    def __setattr__(self, key: str, value: Skill) -> None:
        if key in self._attributes:
            super().__setattr__(key, value)
        else:
            self[Symbol(key)] = value

    def __iter__(self) -> Iterator[Skill]:
        code = self._translate.encode_getattr(self.__repr_skill__(), '?')
        result = self._send(code)
        return iter(self._translate.decode(result) or ())  # type: ignore


class RemoteVector(RemoteCollection):
    def __getitem__(self, item: Skill) -> Skill:
        try:
            return super().__getitem__(item)
        except RuntimeError as e:
            if "array index out of bounds" in str(e):
                raise IndexError(f"list index {item} out of range (len={len(self)})") from None
            raise  # pragma: no cover
        except ParseError:
            raise IndexError(f"list index {item} out of range (len={len(self)})") from None

    def __setitem__(self, item: Skill, value: Skill) -> None:
        try:
            super().__setitem__(item, value)
        except RuntimeError as e:
            if "array index out of bounds" in str(e):
                raise IndexError(f"list index {item} out of range (len={len(self)})") from None
            raise  # pragma: no cover