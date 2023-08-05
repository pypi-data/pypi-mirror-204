import click
from charsi.commands import command_group


@click.group(commands=command_group)
@click.version_option(message='%(version)s')
def cli():
    """A command-line tool to help game modders build string resources for Diablo II: Resurrected."""


if __name__ == '__main__':
    cli()
