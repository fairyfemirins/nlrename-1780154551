#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)

Rename files using natural language commands:
- "all PDFs to lowercase"
- "prepend today's date"
- "replace spaces with underscores"
- "append 'backup'"
"""

import os
import re
import click
from datetime import datetime
from dateutil.relativedelta import relativedelta


@click.command()
@click.argument('pattern', type=str)
@click.argument('path', type=click.Path(exists=True), default='.')
@click.option('--dry-run', is_flag=True, help='Show what would be renamed without making changes.')
@click.option('--recursive', is_flag=True, help='Rename files recursively in subdirectories.')
def cli(pattern: str, path: str, dry_run: bool, recursive: bool):
    """Rename files using natural language patterns."""
    renamer = NaturalLanguageRenamer(pattern, path, dry_run, recursive)
    renamer.run()


class NaturalLanguageRenamer:
    def __init__(self, pattern: str, path: str, dry_run: bool, recursive: bool):
        self.pattern = pattern.lower()
        self.path = path
        self.dry_run = dry_run
        self.recursive = recursive
        self.file_count = 0
        self.renamed_count = 0

    def run(self):
        """Run the renamer."""
        if self.recursive:
            for root, _, files in os.walk(self.path):
                for file in files:
                    self._process_file(root, file)
        else:
            for file in os.listdir(self.path):
                if os.path.isfile(os.path.join(self.path, file)):
                    self._process_file(self.path, file)

        click.echo(f"Processed {self.file_count} files, renamed {self.renamed_count}.")

    def _process_file(self, root: str, file: str):
        """Process a single file."""
        self.file_count += 1
        old_path = os.path.join(root, file)
        new_name = self._apply_pattern(file)
        if new_name != file:
            new_path = os.path.join(root, new_name)
            if self.dry_run:
                click.echo(f"[DRY RUN] {old_path} -> {new_path}")
            else:
                os.rename(old_path, new_path)
                click.echo(f"Renamed: {old_path} -> {new_path}")
            self.renamed_count += 1

    def _apply_pattern(self, filename: str) -> str:
        """Apply the natural language pattern to a filename."""
        name, ext = os.path.splitext(filename)

        # File extension filters (case-insensitive)
        ext_lower = ext.lower()
        if 'pdfs' in self.pattern and ext_lower != '.pdf':
            return filename
        elif 'images' in self.pattern and ext_lower not in ('.jpg', '.jpeg', '.png', '.gif'):
            return filename
        elif 'docs' in self.pattern and ext_lower not in ('.doc', '.docx', '.txt'):
            return filename

        # Case transformations
        if 'lowercase' in self.pattern or 'to lowercase' in self.pattern or 'all pdfs to lowercase' in self.pattern:
            name = name.lower()
            ext = ext.lower()
        elif 'uppercase' in self.pattern or 'to uppercase' in self.pattern:
            name = name.upper()
            ext = ext.upper()
        elif 'title case' in self.pattern:
            name = name.title()

        return f"{name}{ext}"
        if "today's date" in self.pattern:
            today = datetime.now().strftime('%Y-%m-%d')
            if 'prepend' in self.pattern:
                name = f"{today}_{name}"
            elif 'append' in self.pattern:
                name = f"{name}_{today}"
        elif 'yesterday' in self.pattern:
            yesterday = (datetime.now() - relativedelta(days=1)).strftime('%Y-%m-%d')
            if 'prepend' in self.pattern:
                name = f"{yesterday}_{name}"
            elif 'append' in self.pattern:
                name = f"{name}_{yesterday}"

        # String replacements
        if 'replace spaces with underscores' in self.pattern:
            name = name.replace(' ', '_')
        elif 'replace underscores with spaces' in self.pattern:
            name = name.replace('_', ' ')
        elif 'replace' in self.pattern and 'with' in self.pattern:
            parts = self.pattern.split('replace')[1].split('with')
            old = parts[0].strip()
            new = parts[1].strip().split()[0]  # Take the first word after 'with'
            name = name.replace(old, new)

        # Regex patterns
        if 'regex' in self.pattern:
            match = re.search(r'regex "(.+?)" with "(.+?)"', self.pattern)
            if match:
                old_regex, new_regex = match.groups()
                name = re.sub(old_regex, new_regex, name)

        # Append/prepend text
        if 'append' in self.pattern:
            text = self.pattern.split('append')[1].strip().strip("'")
            name = f"{name}{text}"
        elif 'prepend' in self.pattern:
            text = self.pattern.split('prepend')[1].strip().strip("'")
            name = f"{text}{name}"

        return f"{name}{ext}"


if __name__ == '__main__':
    cli()