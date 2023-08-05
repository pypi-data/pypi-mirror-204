from pathlib import Path

import click

from charsi.manifest import ManifestFile
from charsi.asset import AssetFinder
from charsi.utils import charsi_dir
from charsi.instruction import InstructionInvoker


@click.command('build-manifest')
@click.argument('manifest-file', metavar='FILE', type=click.Path(exists=True, dir_okay=False), required=True)
def build_manifest_command(manifest_file: str):
    assets = AssetFinder(charsi_dir())

    for file in assets.instruction_files:
        InstructionInvoker.default.load_lua(file.read_text(encoding='utf-8'))

    manifest = ManifestFile()
    manifest.load_file(Path(manifest_file))

    for task in manifest.tasks:
        task.run()
