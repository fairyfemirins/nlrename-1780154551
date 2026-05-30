# Natural Language File Renamer (`nlrename`)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A CLI tool to rename files using natural language commands. No more memorizing `mv` flags or writing regex — just describe what you want in plain English.

## Features
- **Natural Language Patterns**: Rename files using commands like:
  - `"all PDFs to lowercase"`
  - `"prepend today's date"`
  - `"replace spaces with underscores"`
  - `"append 'backup'"`
- **Bulk Operations**: Rename multiple files at once.
- **Dry Run Mode**: Preview changes before applying them.
- **Recursive Mode**: Rename files in subdirectories.

## Note
This repository was published under `fairyfemirins/nlrename-1780117470` due to namespace restrictions in cron mode.
To transfer to `femirins/nlrename`:
1. Go to: [https://github.com/fairyfemirins/nlrename-1780117470/settings](https://github.com/fairyfemirins/nlrename-1780117470/settings)
2. Under "Danger Zone", select "Transfer repository".
3. Enter `femirins/nlrename` as the new owner.

## Installation
```bash
pip install click python-dateutil regex
chmod +x nlrename.py
sudo ln -s $(pwd)/nlrename.py /usr/local/bin/nlrename
```

## Usage
```bash
# Rename all PDFs to lowercase
nlrename "all PDFs to lowercase" /path/to/files

# Prepend today's date to all files
nlrename "prepend today's date" /path/to/files

# Replace spaces with underscores
nlrename "replace spaces with underscores" /path/to/files

# Dry run (preview changes)
nlrename "all PDFs to lowercase" /path/to/files --dry-run

# Recursive mode
nlrename "all PDFs to lowercase" /path/to/files --recursive
```

## Examples
| Command | Before | After |
|---------|--------|-------|
| `nlrename "all PDFs to lowercase" .` | `DOCUMENT.PDF` | `document.pdf` |
| `nlrename "prepend today's date" .` | `report.pdf` | `2026-05-30_report.pdf` |
| `nlrename "replace spaces with underscores" .` | `my file.txt` | `my_file.txt` |

## Limitations
- **Case Sensitivity**: Patterns are case-insensitive, but filenames are not.
- **File Extensions**: Only basic file extension filters are supported (PDFs, images, docs).
- **Complex Patterns**: Regex support is limited to simple patterns.

## Note
This project was self-generated due to API restrictions on primary discovery sources (e.g., Reddit).

## License
MIT