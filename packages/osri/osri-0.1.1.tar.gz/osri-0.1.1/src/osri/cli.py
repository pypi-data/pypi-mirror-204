"""
CLI module that defines the behaviour of `osri`.
"""
import sys

import click
from prettytable import PrettyTable

from . import config, errors


@click.group
def cli() -> None:
    """
    Funtion that will groups all cli subcommands.
    """
    pass


@cli.command
def version() -> None:
    """
    Invoked whe running `osri version`, printing the CLI version.
    """
    v = '0.1.1'

    click.echo(f'v{v}')


@cli.command
@click.option('--path', default='/etc/os-release', help='os release file path to parse')
def display(path : str) -> None:
    """
    Load, parse and show data from an os-release file.

    It parses the config file from `/etc/os-release` if no path is provided.

    Parsed data is shown in a table.
    """
    data = config.load(path)

    table = PrettyTable([], header=False, align='l')
    for k,v in data.items():
        table.add_rows([[k, v]])
    
    click.echo(table)


def run() -> None:
    """
    Run the CLI by invoking the `cli()` function.

    It will gracefully fail if a `errors.OSRIError` is risen.
    """
    try:
        cli()
    except errors.OSRIError as e:
        sys.stderr.write(f'{e}\n')
        sys.exit(e.code)
