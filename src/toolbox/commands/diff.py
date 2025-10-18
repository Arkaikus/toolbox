"""Diff command for comparing files and folders."""

import click
import os
from pathlib import Path
from typing import Set, Tuple, List
from datetime import datetime


def get_folder_structure(path: Path) -> Set[str]:
    """Get the relative file/folder structure of a directory."""
    structure = set()
    
    if not path.exists():
        return structure
    
    if path.is_file():
        return {path.name}
    
    # Common dependency folders to ignore
    ignore_folders = {
        'node_modules', '__pycache__', '.git', '.svn', '.hg', 
        'venv', 'env', '.venv', '.env', 'virtualenv',
        'build', 'dist', 'target', 'bin', 'obj',
        '.pytest_cache', '.coverage', 'coverage',
        '.mypy_cache', '.tox', '.nox',
        'vendor', 'bower_components', 'jspm_packages',
        '.idea', '.vscode', '.vs', '.DS_Store',
        'Thumbs.db', '.Trash-1000'
    }
    
    for root, dirs, files in os.walk(path):
        root_path = Path(root)
        rel_path = root_path.relative_to(path)
        
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_folders]
        
        # Add directories (after filtering)
        for dir_name in dirs:
            if rel_path == Path('.'):
                structure.add(dir_name)
            else:
                structure.add(str(rel_path / dir_name))
        
        # Add files
        for file_name in files:
            if rel_path == Path('.'):
                structure.add(file_name)
            else:
                structure.add(str(rel_path / file_name))
    
    return structure


def compare_folders(path1: Path, path2: Path) -> Tuple[bool, List[str], List[str]]:
    """Compare two folder structures and return differences."""
    structure1 = get_folder_structure(path1)
    structure2 = get_folder_structure(path2)
    
    only_in_path1 = structure1 - structure2
    only_in_path2 = structure2 - structure1
    
    are_same = len(only_in_path1) == 0 and len(only_in_path2) == 0
    
    return are_same, sorted(only_in_path1), sorted(only_in_path2)


def write_to_log(log_filename: str, content: str):
    """Write content to log file."""
    with open(log_filename, 'w', encoding='utf-8') as f:
        f.write(content)


@click.command()
@click.argument('path1', type=click.Path(exists=True))
@click.argument('path2', type=click.Path(exists=True))
def diff(path1, path2):
    """Compare two files or folders.
    
    For folders: compares file/folder structure and shows differences.
    For files: comparison is TBD (not yet implemented).
    
    Output is written to diff-{date}.log file.
    """
    path1 = Path(path1)
    path2 = Path(path2)
    
    # Generate log filename with current date
    current_date = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    log_filename = f"diff-{current_date}.log"
    
    # Prepare log content
    log_content = f"Diff Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    log_content += f"Comparing: {path1} vs {path2}\n"
    log_content += "=" * 50 + "\n\n"
    
    # Check if both paths are files
    if path1.is_file() and path2.is_file():
        message = "File comparison is TBD (not yet implemented)"
        click.echo(message, err=True)
        log_content += f"ERROR: {message}\n"
        write_to_log(log_filename, log_content)
        return
    
    # Check if both paths are directories
    if path1.is_dir() and path2.is_dir():
        are_same, only_in_path1, only_in_path2 = compare_folders(path1, path2)
        
        if are_same:
            message = "they are the same"
            click.echo(click.style(message, fg='green'))
            log_content += f"RESULT: {message}\n"
        else:
            # Show differences in red
            log_content += "DIFFERENCES FOUND:\n\n"
            
            if only_in_path1:
                message = f"Only in {path1}:"
                click.echo(click.style(message, fg='red'))
                log_content += f"{message}\n"
                for item in only_in_path1:
                    item_message = f"  {item}"
                    click.echo(click.style(item_message, fg='red'))
                    log_content += f"{item_message}\n"
                log_content += "\n"
            
            if only_in_path2:
                message = f"Only in {path2}:"
                click.echo(click.style(message, fg='red'))
                log_content += f"{message}\n"
                for item in only_in_path2:
                    item_message = f"  {item}"
                    click.echo(click.style(item_message, fg='red'))
                    log_content += f"{item_message}\n"
                log_content += "\n"
    
    else:
        message = "Error: Both paths must be either files or directories"
        click.echo(message, err=True)
        log_content += f"ERROR: {message}\n"
    
    # Write to log file
    write_to_log(log_filename, log_content)
    click.echo(f"\nReport saved to: {log_filename}")
