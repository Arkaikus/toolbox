"""Example hello command for toolbox CLI."""

import click


@click.command()
@click.option('--name', default='World', help='Name to greet.')
@click.option('--count', default=1, help='Number of times to greet.')
def hello(name, count):
    """Say hello to NAME."""
    for _ in range(count):
        click.echo(f'Hello, {name}!')
