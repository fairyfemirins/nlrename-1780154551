# Natural Language File Renamer (`nlrename`)

A CLI tool to rename files using natural language instructions. No more wrestling with `rename`, `sed`, or manual bulk edits!

## Features
- **Natural Language Instructions**:
  - `"add today's date to all PDFs"`
  - `"replace 'draft' with 'final'"`
  - `"all files to lowercase"`
  - `"append '_backup' to all files"`
  - `"prepend '2026-' to all TXT files"`
- **Dry Run Mode**: Preview changes before applying.
- **Force Mode**: Overwrite existing files.
- **Bulk Operations**: Recursively rename files in directories.

## Installation
```bash
pip install --break-system-packages click python-dateutil regex
```

## Usage
```bash
python nlrename.py "<instruction>" <directory> [--dry-run] [--force]
```

### Examples
```bash
# Preview renaming all files to lowercase
python nlrename.py "all files to lowercase" ~/Downloads --dry-run

# Replace 'draft' with 'final' in all filenames
python nlrename.py "replace 'draft' with 'final'" ~/projects --force

# Append '_backup' to all files
python nlrename.py "append '_backup'" ~/documents
```

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).