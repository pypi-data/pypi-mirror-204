import re
import json
from typing import TypedDict, IO, List, Dict, Optional
from enum import Enum
from functools import reduce


# pylint: disable=invalid-name
class GameStringLanguage(Enum):
    enUS = 'enUS'
    zhTW = 'zhTW'
    deDE = 'deDE'
    esES = 'esES'
    frFR = 'frFR'
    itIT = 'itIT'
    koKR = 'koKR'
    plPL = 'plPL'
    esMX = 'esMX'
    jaJP = 'jaJP'
    ptBR = 'ptBR'
    ruRU = 'ruRU'
    zhCN = 'zhCN'

    @staticmethod
    def get_values() -> List[str]:
        return [x.value for x in GameStringLanguage]


class GameString(TypedDict):
    id: str
    Key: str
    enUS: str
    zhTW: str
    deDE: str
    esES: str
    frFR: str
    itIT: str
    koKR: str
    plPL: str
    esMX: str
    jaJP: str
    ptBR: str
    ruRU: str
    zhCN: str


class GameStringTable:
    _strings: List[GameString]
    _indices: Dict[str, int]

    def __init__(self):
        self._strings = []
        self._indices = {}

    @property
    def strings(self):
        return self._strings

    def load(self, fp: IO):
        self._strings = json.load(fp)
        self._indices = {self._strings[i]['Key']: i for i in range(0, len(self._strings))}

        return self

    def dump(self, fp: IO):
        json.dump(self._strings, fp, ensure_ascii=False, indent=2)

        return self

    def find(self, key: str) -> Optional[GameString]:
        if key not in self._indices:
            raise LookupError(key)

        return self._strings[self._indices[key]]

    def findall(self, query: str) -> List[dict]:
        if query.find(',') > -1:
            return reduce(lambda v, sl: v + sl, [self.findall(q.strip()) for q in query.split(',')], [])

        m = re.match(r'^\s*([\w\s]+)\s*~\s*([\w\s]+)\s*$', query)

        if not m:
            return [self.find(query)]

        if (m.group(1) not in self._indices) or (m.group(2) not in self._indices):
            raise IndexError(query)

        start_index = self._indices[m.group(1)]
        end_index = self._indices[m.group(2)] + 1
        if start_index > end_index:
            raise IndexError(query)

        return self._strings[start_index:end_index]
