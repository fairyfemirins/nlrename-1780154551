# Natural Language File Renamer (`nlrename`)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI tool to rename files using natural language (e.g., `nlrename "all PDFs to lowercase"`, `nlrename "prepend today's date"`).

## Features
- **Case Transformation**: `lowercase`, `uppercase`, `titlecase`.
- **Date Patterns**: Prepend `today's date` or `yesterday's date`.
- **Regex Replace**: Replace text in filenames (e.g., `replace foo with bar`).
- **Extension Filters**: Target specific file types (e.g., `all PDFs`).
- **Dry Run**: Preview changes with `--dry-run`.
- **Recursive**: Rename files in subdirectories with `--recursive`.

## Installation
```bash
pip install click python-dateutil regex
```

## Usage
```bash
# Rename all PDFs to lowercase
nlrename "all PDFs to lowercase"

# Prepend today's date to all files
nlrename "prepend today's date"

# Replace "foo" with "bar" in all filenames
nlrename "replace foo with bar"

# Preview changes without renaming
nlrename "all PDFs to lowercase" --dry-run

# Rename files in subdirectories
nlrename "all PDFs to lowercase" --recursive
```

## Examples
| Pattern                          | Before          | After               |
|---------------------------------|-----------------|---------------------|
| `all PDFs to lowercase`         | `Document.PDF`  | `document.pdf`      |
| `prepend today's date`          | `notes.txt`     | `2026-05-30_notes.txt` |
| `replace foo with bar`          | `foo.txt`       | `bar.txt`           |

## Technical Architecture
- **Language**: Python 3.8+
- **Dependencies**: `click`, `python-dateutil`, `regex`
- **Pattern Parser**: Regex-based natural language parser
- **File System**: Uses `os.rename` for atomic operations

## Limitations
- **Case Sensitivity**: Filters are case-insensitive (e.g., `.PDF` matches `.pdf`).
- **No Undo**: Use `--dry-run` before live renames.
- **No Wildcards**: Use regex or filters instead.

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).

## License
MIT# Note

This repository is published under `fairyfemirins` due to GitHub namespace restrictions. A transfer to `Femirins` is pending.

## Transfer Instructions

To request a transfer:
1. Open an issue in this repository.
2. Contact `@Femirins` on GitHub.

### Manual Transfer Process
1. Navigate to: [https://github.com/fairyfemirins/nlrename/settings](https://github.com/fairyfemirins/nlrename/settings)
2. Under "Danger Zone", select "Transfer ownership".
3. Enter the target namespace (`Femirins`) and confirm.
