# NL Rename: Natural Language File Renamer

Rename files using natural language expressions:
- `nlrename "today's date + original name"`
- `nlrename "s/IMG/DSC/"`
- `nlrename "lowercase all"`
- `nlrename "uppercase all"`

![Demo](https://via.placeholder.com/600x150?text=NL+Rename+Demo)

## Features
- **Natural Language**: Rename files using intuitive expressions (e.g., `"today's date + original name"`).
- **Regex Support**: Use `s/pattern/replacement/` to rename files with regex.
- **Case Transformations**: Convert filenames to `lowercase`, `UPPERCASE`, or `TitleCase`.
- **Dry Run**: Preview changes with `--dry-run`.
- **Recursive**: Rename files in subdirectories with `--recursive`.

## Installation
```bash
pip install click python-dateutil
```

## Usage
```bash
# Rename all files in the current directory
nlrename "today's date + original name"

# Rename specific files
nlrename "s/IMG/DSC/" IMG_123.jpg IMG_456.jpg

# Dry run (preview changes)
nlrename --dry-run "lowercase all"

# Recursive rename
nlrename --recursive "uppercase all"
```

## Examples
| Expression                  | Before       | After               |
|----------------------------|--------------|---------------------|
| `"today's date + original name"` | `notes.txt`  | `2026-05-30_notes.txt` |
| `"s/IMG/DSC/"`            | `IMG_123.jpg`| `DSC_123.jpg`       |
| `"lowercase all"`         | `TEST.TXT`   | `test.txt`          |
| `"uppercase all"`         | `test.txt`   | `TEST.TXT`          |

## Technical Architecture
- **Language**: Python 3.11+
- **Dependencies**: `click`, `python-dateutil`
- **Entry Point**: `nlrename.py` (single-file CLI tool)
- **Testing**: `unittest` (see `test_nlrename.py`)

## Limitations
- **No Undo**: Always use `--dry-run` before applying changes.
- **No Conflict Handling**: Overwrites existing files if names collide.

## Note
This repository was published under `fairyfemirins/nlrename-1780119157` due to namespace restrictions in cron mode.
To transfer to `femirins/nlrename`:
1. Go to: [https://github.com/fairyfemirins/nlrename-1780119157/settings](https://github.com/fairyfemirins/nlrename-1780119157/settings)
2. Under "Danger Zone", select "Transfer repository".
3. Enter `femirins/nlrename` as the new owner.