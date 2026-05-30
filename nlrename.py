#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)

Rename files using natural language instructions:
- "add today's date to all PDFs"
- "replace 'draft' with 'final'"
- "all files to lowercase"
- "append '_backup' to all files"

Usage:
  python nlrename.py "<instruction>" <directory> [--dry-run] [--force]
"""

import os
import re
import fnmatch
import click
from datetime import datetime


def parse_instruction(instruction):
    """Parse natural language instruction into a renaming rule."""
    instruction = instruction.lower().strip()
    rule = {
        "action": None,
        "pattern": None,
        "replacement": None,
        "file_filter": None,
        "date_format": None,
        "case_action": None,
    }

    # Date-based instructions
    if "today's date" in instruction:
        rule["date_format"] = "%Y-%m-%d"
        if "add" in instruction:
            rule["action"] = "prepend_date"
        elif "append" in instruction:
            rule["action"] = "append_date"

    # Replace instructions
    if "replace" in instruction:
        rule["action"] = "replace"
        match = re.search(r'replace ["]?([^"\s]+)["]? with ["]?([^"\s]+)["]?', instruction)
        if match:
            rule["pattern"] = match.group(1).strip("'")
            rule["replacement"] = match.group(2).strip("'")
        return rule  # Early return for replace

    # Case instructions
    if "lowercase" in instruction:
        rule["action"] = "lowercase"
        return rule  # Early return for case instructions
    elif "uppercase" in instruction:
        rule["action"] = "uppercase"
        return rule

    # Append/prepend instructions
    if "append" in instruction and "date" not in instruction:
        rule["action"] = "append"
        match = re.search(r'append ["]?([^"\s]+)["]?', instruction)
        if match:
            rule["replacement"] = match.group(1)
    elif "prepend" in instruction and "date" not in instruction:
        rule["action"] = "prepend"
        match = re.search(r'prepend ["]?([^"\s]+)["]?', instruction)
        if match:
            rule["replacement"] = match.group(1)

    # File filters (e.g., "all PDFs", "files named 'draft'")
    if "all" in instruction:
        match = re.search(r'all (\w+)s?', instruction)
        if match:
            rule["file_filter"] = f"*.{match.group(1)}"
    elif "named" in instruction:
        match = re.search(r'named ["]?([^"\s]+)["]?', instruction)
        if match:
            rule["file_filter"] = f"*{match.group(1)}*"
    elif "replace" in instruction:
        rule["file_filter"] = "*"  # Force filter for replace

    return rule


def apply_rule(filename, rule):
    """Apply renaming rule to a filename."""
    name, ext = os.path.splitext(filename)
    new_name = name
    new_ext = ext.lower() if ext else ext

    click.echo(f"DEBUG: Processing {filename} (name: {name}, ext: {ext})")
    click.echo(f"DEBUG: Rule - {rule}")

    if rule["action"] == "prepend_date":
        today = datetime.now().strftime(rule["date_format"])
        new_name = f"{today}_{name}"
    elif rule["action"] == "append_date":
        today = datetime.now().strftime(rule["date_format"])
        new_name = f"{name}_{today}"
    elif rule["action"] == "replace":
        new_name = re.sub(re.escape(rule["pattern"]), rule["replacement"], name)
    elif rule["action"] == "lowercase":
        new_name = name.lower()
        new_ext = ext.lower()
    elif rule["action"] == "uppercase":
        new_name = name.upper()
    elif rule["action"] == "append":
        new_name = f"{name}{rule['replacement']}"
    elif rule["action"] == "prepend":
        new_name = f"{rule['replacement']}{name}"

    return f"{new_name}{new_ext}"


def rename_files(directory, rule, dry_run=False, force=False):
    """Rename files in directory based on rule."""
    renamed = []
    skipped = []

    for root, _, files in os.walk(directory):
        for filename in files:
            if rule["file_filter"]:
                if not fnmatch.fnmatch(filename, rule["file_filter"]):
                    continue

            old_path = os.path.join(root, filename)
            new_filename = apply_rule(filename, rule)
            new_path = os.path.join(root, new_filename)

            if old_path == new_path:
                skipped.append((filename, "No change"))
                continue

            if not force and os.path.exists(new_path):
                skipped.append((filename, "Target exists"))
                continue

            if dry_run:
                renamed.append((filename, new_filename))
                click.echo(f"DEBUG: Would rename {filename} → {new_filename}")
            else:
                os.rename(old_path, new_path)
                renamed.append((filename, new_filename))

    return renamed, skipped


@click.command()
@click.argument("instruction", type=str)
@click.argument("directory", type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True, help="Preview changes without renaming.")
@click.option("--force", is_flag=True, help="Overwrite existing files.")
def main(instruction, directory, dry_run, force):
    """Main CLI entrypoint."""
    rule = parse_instruction(instruction)
    if not rule["action"]:
        click.echo(f"Error: Could not parse instruction '{instruction}'.")
        return

    renamed, skipped = rename_files(directory, rule, dry_run, force)

    click.echo(f"\nInstruction: {instruction}")
    click.echo(f"Directory: {directory}")
    click.echo(f"Dry Run: {'Yes' if dry_run else 'No'}")
    click.echo(f"\nRenamed Files:")
    for old, new in renamed:
        click.echo(f"  {old} → {new}")

    if skipped:
        click.echo(f"\nSkipped Files:")
        for filename, reason in skipped:
            click.echo(f"  {filename} ({reason})")


if __name__ == "__main__":
    main()