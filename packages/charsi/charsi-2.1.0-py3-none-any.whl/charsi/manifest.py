import json
from typing import List
from dataclasses import dataclass
from pathlib import Path

from charsi.strings import GameStringTable
from charsi.recipe import Recipe


@dataclass
class Task:
    base_dir: Path
    input: str
    output: str
    recipes: List[str]

    def guess_path(self, filepath: Path | str) -> Path:
        filepath = Path(filepath)

        if filepath.is_file():
            return filepath

        return filepath.joinpath(self.base_dir, filepath)

    def run(self):
        stbl = GameStringTable()
        with self.guess_path(self.input).open('r', encoding='utf-8-sig') as fp:
            stbl.load(fp)

        for recipe_file in self.recipes:
            recipe = Recipe()
            with self.guess_path(recipe_file).open('r', encoding='utf-8') as fp:
                recipe.load(fp)

            recipe.build(stbl)

        with self.guess_path(self.output).open('w', encoding='utf-8-sig') as fp:
            stbl.dump(fp)


class ManifestFile:
    _tasks: List[Task]

    @property
    def tasks(self) -> List[Task]:
        return self._tasks

    def load_file(self, filepath: Path):
        with filepath.open('r', encoding='utf-8') as fp:
            self._tasks = [Task(base_dir=filepath.parent, **item) for item in json.load(fp)]
