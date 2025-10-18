"""Example version command for toolbox CLI."""

import click
import sys


@click.command()
def version():
    """Show Python and toolbox version information."""
    import toolbox
    click.echo(f"Toolbox version: {toolbox.__version__}")
    click.echo(f"Python version: {sys.version}")
