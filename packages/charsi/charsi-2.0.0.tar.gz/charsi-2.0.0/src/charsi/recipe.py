from typing import List, Dict, IO
from .instruction import parse, Instruction, InstructionInvoker
from .strings import GameStringTable, GameStringLanguage
from .utils import filter_irrelevant, split_text


class Recipe:
    _instructions: List[Instruction]
    _tags: Dict[str, str]

    @property
    def instructions(self):
        return self._instructions

    def load(self, fp: IO):
        lines = [line.strip() for line in fp.readlines()]

        self._instructions = [parse(line) for line in filter_irrelevant(lines)]
        self._tags = {}

        for line in filter(lambda line: line != '' and line[0:2] == '##', lines):
            fds = split_text(line, ':')
            self._tags[fds[0][2:].strip()] = fds[1].strip()

        return self

    def build(self, stbl: GameStringTable, invoker: InstructionInvoker = None):
        if invoker is None:
            invoker = InstructionInvoker.default

        for inst in self._instructions:
            if (inst.lang is None) and ('Language' in self._tags):
                inst.lang = self._tags['Language']

            langs = GameStringLanguage.get_values() if inst.lang is None else [inst.lang]

            for s in stbl.findall(inst.query):
                s.update({lang: invoker.invoke(inst, s[lang]) for lang in langs})
