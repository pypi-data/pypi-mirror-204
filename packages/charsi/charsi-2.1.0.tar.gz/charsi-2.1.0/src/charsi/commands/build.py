import sys
from pathlib import Path

import click

from charsi.strings import GameStringTable
from charsi.recipe import Recipe
from charsi.instruction import InstructionInvoker
from charsi.asset import AssetFinder
from charsi.utils import charsi_dir


@click.command('build')
@click.option('--recipe-file', help='Path of recipe file.', metavar='FILE', type=click.Path(exists=True, dir_okay=False), required=True)
@click.argument('stbl-file', metavar='FILE', type=click.Path(exists=True, dir_okay=False), required=True)
def build_command(recipe_file: str, stbl_file: str):
    assets = AssetFinder(charsi_dir())

    for file in assets.instruction_files:
        InstructionInvoker.default.load_lua(file.read_text(encoding='utf-8'))

    recipe = Recipe()
    with open(recipe_file, 'r', encoding='utf-8') as fp:
        recipe.load(fp)

    stbl = GameStringTable()
    with open(stbl_file, 'r', encoding='utf-8-sig') as fp:
        stbl.load(fp)

    alias_table = assets.get_alias(Path(stbl_file).name.split('.')[0])

    if alias_table:
        stbl.set_alias(alias_table)

    recipe.build(stbl)
    stbl.dump(sys.stdout)
