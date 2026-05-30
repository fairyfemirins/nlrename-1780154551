#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)
Rename files using natural language (e.g., "all PDFs to lowercase", "prepend today's date").
"""

import os
import re
import click
from datetime import datetime
from dateutil.relativedelta import relativedelta


@click.command()
@click.argument('pattern', type=str)
@click.option('--dry-run', is_flag=True, help='Preview changes without renaming.')
@click.option('--recursive', is_flag=True, help='Rename files in subdirectories.')
def cli(pattern: str, dry_run: bool, recursive: bool):
    """Rename files using natural language patterns."""
    # Parse pattern
    rename_ops = parse_pattern(pattern)
    if not rename_ops:
        click.echo("Error: Could not parse pattern. Examples:")
        click.echo("  nlrename 'all PDFs to lowercase'")
        click.echo("  nlrename 'prepend today's date'")
        click.echo("  nlrename 'replace foo with bar'")
        return

    # Collect files
    files = []
    if recursive:
        for root, _, filenames in os.walk('.'):
            for filename in filenames:
                files.append(os.path.join(root, filename))
    else:
        files = [f for f in os.listdir('.') if os.path.isfile(f)]

    # Debug: Print collected files
    click.echo(f"[DEBUG] Collected files: {files}")

    # Apply renames
    for filepath in files:
        dirname, basename = os.path.split(filepath)
        new_name = apply_rename_ops(basename, rename_ops)
        if new_name != basename:
            new_path = os.path.join(dirname, new_name)
            if dry_run:
                click.echo(f"[DRY RUN] {filepath} -> {new_path}")
            else:
                os.rename(filepath, new_path)
                click.echo(f"Renamed: {filepath} -> {new_path}")


def parse_pattern(pattern: str) -> list:
    """Parse natural language pattern into rename operations."""
    pattern = pattern.lower().strip()
    ops = []
    click.echo(f"[DEBUG] Parsing pattern: {pattern}")

    # Case transformations
    if 'lowercase' in pattern:
        ops.append(('case', 'lower'))
    elif 'uppercase' in pattern:
        ops.append(('case', 'upper'))
    elif 'titlecase' in pattern:
        ops.append(('case', 'title'))

    # Date patterns
    if "today's date" in pattern:
        ops.append(('prepend', datetime.now().strftime('%Y-%m-%d')))
    elif "yesterday's date" in pattern:
        ops.append(('prepend', (datetime.now() - relativedelta(days=1)).strftime('%Y-%m-%d')))

    # Regex replace
    if 'replace' in pattern:
        match = re.search(r'replace (.*?) with (.*?)(?:$|\s)', pattern)
        if match:
            ops.append(('replace', (match.group(1), match.group(2))))

    # File extension filters
    if 'pdfs' in pattern:
        ops.append(('filter', '.pdf'))
    elif 'images' in pattern:
        ops.append(('filter', ('.jpg', '.jpeg', '.png', '.gif')))

    return ops


def apply_rename_ops(filename: str, ops: list) -> str:
    """Apply rename operations to a filename."""
    name, ext = os.path.splitext(filename)
    new_name = name
    new_ext = ext
    click.echo(f"[DEBUG] Processing file: {filename}, ops: {ops}")

    for op in ops:
        if op[0] == 'case':
            if op[1] == 'lower':
                new_name = new_name.lower()
                new_ext = new_ext.lower()  # Apply case transform to extension too
            elif op[1] == 'upper':
                new_name = new_name.upper()
                new_ext = new_ext.upper()
            elif op[1] == 'title':
                new_name = new_name.title()
                new_ext = new_ext.title()
        elif op[0] == 'prepend':
            new_name = f"{op[1]}_{new_name}"
        elif op[0] == 'replace':
            new_name = re.sub(re.escape(op[1][0]), op[1][1], new_name)
        elif op[0] == 'filter':
            if isinstance(op[1], str) and new_ext.lower() != op[1].lower():
                click.echo(f"[DEBUG] Skipping {filename}: extension {new_ext} does not match {op[1]}")
                return filename  # Skip if extension doesn't match
            elif isinstance(op[1], tuple) and new_ext.lower() not in [e.lower() for e in op[1]]:
                click.echo(f"[DEBUG] Skipping {filename}: extension {new_ext} not in {op[1]}")
                return filename  # Skip if extension not in tuple

    return f"{new_name}{new_ext}"


if __name__ == '__main__':
    cli()