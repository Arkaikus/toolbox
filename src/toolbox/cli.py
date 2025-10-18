"""Main CLI entry point for toolbox."""

import click
import importlib
import pkgutil
from pathlib import Path


@click.group()
@click.version_option(version="0.1.0", prog_name="toolbox")
def cli():
    """Toolbox - A collection of useful Python scripts."""
    pass


def load_commands():
    """Dynamically load all commands from the commands package."""
    import toolbox.commands as commands_package
    
    # Get the path to the commands package
    commands_path = Path(commands_package.__file__).parent
    
    # Iterate through all modules in the commands package
    for _, module_name, _ in pkgutil.iter_modules([str(commands_path)]):
        # Skip __init__ and private modules
        if module_name.startswith('_'):
            continue
            
        # Import the module
        module = importlib.import_module(f'toolbox.commands.{module_name}')
        
        # Look for Click commands or groups in the module
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            # Check if it's a Click command or group
            if isinstance(attr, (click.Command, click.Group)) and not attr_name.startswith('_'):
                # Add the command to the CLI group
                cli.add_command(attr)


def main():
    """Main entry point."""
    load_commands()
    cli()


if __name__ == "__main__":
    main()
