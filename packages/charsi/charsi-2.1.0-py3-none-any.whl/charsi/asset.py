from typing import List, Dict
from glob import glob
from pathlib import Path

from charsi.utils import filter_irrelevant


def _load_properties(filepath: str | Path) -> dict:
    props = {}
    with open(filepath, 'r', encoding='utf-8') as fp:
        for line in filter_irrelevant(fp.readlines()):
            fds = [x.strip() for x in line.split('=')]
            props[fds[0]] = fds[1]

    return props


class AssetFinder:
    base_dir: str

    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    @property
    def instruction_files(self) -> List[Path]:
        return [Path(path) for path in glob(f'{self.base_dir}/instructions/**/*.lua', recursive=True)]

    def get_alias(self, name: str) -> Dict | None:
        filepath = Path(self.base_dir).joinpath('alias', f'{name}.alias')

        if not filepath.exists():
            return None

        return _load_properties(filepath)
