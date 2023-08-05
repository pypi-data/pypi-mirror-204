from __future__ import annotations
import re
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional
from lupa import LuaRuntime

from .utils import split_text


@dataclass
class Instruction:
    name: str
    query: str
    args: List[str]
    lang: Optional[str] = None


class _InstructionError(Exception):
    ...


class InstructionFormatError(_InstructionError):
    ...


def parse(text: str) -> Instruction:
    fds = split_text(text, ':')
    if len(fds) < 2:
        raise InstructionFormatError(text)

    m = re.match(r'^\s*(\w+)\s*(\[[^]]+])\s*(\[[^]]+])?', fds[0])

    if not m:
        raise InstructionFormatError(text)

    return Instruction(
        name=m.group(1),
        query=m.group(2).strip(' []'),
        args=[arg.strip() for arg in split_text(fds[1], '#')[0].split(',')],
        lang=None if m.group(3) is None else m.group(3).strip(' []')
    )


class InstructionInvoker:
    _handlers: Dict[str, Callable]
    _lua: LuaRuntime

    default: InstructionInvoker

    def __init__(self):
        self._handlers = {}
        self._lua = LuaRuntime(unpack_returned_tuples=True, register_builtins=False)

        lua_globals = self._lua.globals()
        lua_globals['python'] = None
        lua_globals['RegisterInstruction'] = self.register
        lua_globals['UnregisterInstruction'] = self.unregister
        lua_globals['InstructionRegistered'] = self.is_registered

    def register(self, name: str, handler: Callable):
        if name in self._handlers:
            raise InstructionConflictError(name)

        self._handlers[name] = handler

    def unregister(self, name: str):
        if name not in self._handlers:
            raise InstructionUndefinedError(name)

        del self._handlers[name]

    def is_registered(self, name: str):
        return name in self._handlers

    def invoke(self, inst: Instruction, text: str) -> str:
        if not self.is_registered(inst.name):
            raise InstructionUndefinedError(inst.name)

        result = self._handlers[inst.name](text, *inst.args)

        if isinstance(result, str):
            return result.replace('{origin}', text)

        if isinstance(result, tuple):
            return result[0].replace('{origin}', text)

        raise TypeError(type(result))

    def load_lua(self, codes: str):
        self._lua.execute(codes)


class _InstructionInvokeError(Exception):
    ...


class InstructionConflictError(_InstructionInvokeError):
    ...


class InstructionUndefinedError(_InstructionInvokeError):
    ...


InstructionInvoker.default = InstructionInvoker()
