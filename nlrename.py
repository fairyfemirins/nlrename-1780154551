#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)

Rename files using natural language expressions:
- `nlrename "today's date + original name"`
- `nlrename "s/IMG/DSC/"`
- `nlrename "lowercase all"`
- `nlrename "uppercase all"`

Usage:
    nlrename [--dry-run] <expression> [files...]
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Optional, Callable

import click
from dateutil.relativedelta import relativedelta


def parse_expression(expression: str) -> callable:
    """Parse natural language expression into a renaming function."""
    expression = expression.strip().lower()

    # Date transformations
    if "today's date" in expression:
        today = datetime.now().strftime("%Y-%m-%d")
        if "original name" in expression:
            return lambda name: f"{today}_{name}"
        return lambda name: f"{today}_{name}"

    # Regex substitution
    if expression.startswith("s/"):
        parts = expression[2:].split("/")
        if len(parts) >= 2:
            pattern, repl = parts[0], parts[1]
            return lambda name: re.sub(pattern, repl, name)

    # Case transformations
    if "lowercase" in expression:
        return lambda name: name.lower()
    if "uppercase" in expression:
        return lambda name: name.upper()
    if "titlecase" in expression:
        return lambda name: name.title()

    # Default: prepend/append
    return lambda name: f"{expression}_{name}"


def rename_file(
    old_path: str, new_name: str, dry_run: bool = False
) -> Optional[str]:
    """Rename a file and return the new path."""
    dirname = os.path.dirname(old_path)
    new_path = os.path.join(dirname, new_name)
    
    if dry_run:
        click.echo(f"[DRY RUN] {old_path} -> {new_path}")
        return new_path
    
    try:
        os.rename(old_path, new_path)
        return new_path
    except OSError as e:
        click.echo(f"Error renaming {old_path}: {e}", err=True)
        return None


@click.command()
@click.argument("expression", type=str)
@click.argument("files", type=click.Path(exists=True), nargs=-1)
@click.option("--dry-run", is_flag=True, help="Show what would be renamed without actually renaming.")
@click.option("--recursive", is_flag=True, help="Rename files in subdirectories recursively.")
def main(expression: str, files: List[str], dry_run: bool, recursive: bool):
    """Rename files using natural language expressions."""
    if not files:
        files = [f for f in os.listdir(".") if os.path.isfile(f)]
    
    if recursive:
        files = [
            os.path.join(root, f)
            for root, _, filenames in os.walk(".")
            for f in filenames
        ]
    
    rename_func = parse_expression(expression)
    
    for file_path in files:
        if not os.path.isfile(file_path):
            continue
        
        dirname, old_name = os.path.split(file_path)
        new_name = rename_func(old_name)
        
        if new_name != old_name:
            rename_file(file_path, new_name, dry_run)


if __name__ == "__main__":
    main()