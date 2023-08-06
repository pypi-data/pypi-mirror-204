import sys
import os
from typing import List, Iterable


def split_text(text: str, sep: str) -> List[str]:
    i = text.find(sep)
    if i == -1:
        return [text.strip()]

    return [text[0:i].strip(), text[i + len(sep):].strip()]


def filter_irrelevant(lines: List[str]) -> Iterable:
    return filter(lambda line: line != '' and line[0] != '#', map(lambda line: line.strip(), lines))


def charsi_dir():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.dirname(sys.executable)

    return os.getcwd()
