# toolbox

A collection of useful Python scripts with an extensible CLI.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone https://github.com/Arkaikus/toolbox.git
cd toolbox

# Install with uv
uv pip install -e .
```

## Usage

The toolbox CLI is accessible via the `tb` command:

```bash
# Show help
tbox --help

# Show version
tbox --version

# Run a command
tbox hello
tbox hello --name "Your Name" --count 3

# Show version information
tbox version
```

## Extending with Custom Commands

You can easily add new commands to the toolbox CLI by creating new Python files in the `src/toolbox/commands/` directory.

### Creating a New Command

1. Create a new file in `src/toolbox/commands/`, e.g., `mycommand.py`
2. Define a Click command or group:

```python
import click

@click.command()
@click.option('--option', default='value', help='An option')
def mycommand(option):
    """Description of your command."""
    click.echo(f'Running mycommand with option: {option}')
```

3. The command will be automatically discovered and added to the CLI

### Example Commands

The toolbox includes example commands to get you started:

- `hello` - A simple greeting command with options
- `version` - Shows version information

## Development

```bash
# Install in editable mode
uv pip install -e .

# Run the CLI
tbox --help
```

## Requirements

- Python >= 3.12
- click >= 8.3.0

