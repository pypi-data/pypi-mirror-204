import sys
from typing import IO

import click

from charsi.strings import GameStringTable
from charsi.recipe import Recipe
from charsi.instruction import InstructionInvoker
from charsi.asset import AssetFinder
from charsi.utils import charsi_dir


@click.command('build')
@click.option('--recipe-file', help='Path of recipe file.', metavar='FILE', type=click.File(mode='r', encoding='utf-8'), required=True)
@click.argument('stbl-file', metavar='FILE', type=click.File(mode='r', encoding='utf-8-sig'), required=True)
def build_command(recipe_file: IO[str], stbl_file: IO[str]):
    assets = AssetFinder(charsi_dir())

    for file in assets.instruction_files:
        InstructionInvoker.default.load_lua(file.read_text(encoding='utf-8'))

    recipe = Recipe()
    recipe.load(recipe_file)

    stbl = GameStringTable()
    stbl.load(stbl_file)

    recipe.build(stbl)
    stbl.dump(sys.stdout)
