from typing import List
from glob import glob
from pathlib import Path


class AssetFinder:
    base_dir: str

    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    @property
    def instruction_files(self) -> List[Path]:
        return [Path(path) for path in glob(f'{self.base_dir}/instructions/**/*.lua', recursive=True)]
