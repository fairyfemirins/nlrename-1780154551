# DESIGN.md: Natural Language File Renamer

## Overview
`nlrename` is a CLI tool for renaming files using natural language. It parses user input into structured operations (case, date, replace, filter) and applies them to filenames.

## Goals
- **Accessibility**: Enable non-technical users to rename files without learning `mv` or `rename`.
- **Automation**: Support bulk operations (e.g., `all PDFs to lowercase`).
- **Safety**: Provide `--dry-run` to preview changes.

## Architecture
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  User Input │ -> │  Parser     │ -> │  Renamer    │
└─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Examples   │    │  Regex      │    │  os.rename  │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Components
1. **Parser** (`parse_pattern`):
   - Input: Natural language string (e.g., `"all PDFs to lowercase"`).
   - Output: List of operations (e.g., `[('case', 'lower'), ('filter', '.pdf')]`).
   - Uses regex to extract patterns (e.g., `replace (.*?) with (.*?)`).

2. **Renamer** (`apply_rename_ops`):
   - Input: Filename and operations.
   - Output: New filename.
   - Applies operations in sequence (case → prepend → replace → filter).

3. **CLI** (`cli`):
   - Uses `click` for argument parsing and help text.
   - Supports `--dry-run` and `--recursive`.

## Trade-offs
- **Simplicity vs. Power**: Prioritizes simple patterns over complex logic (e.g., no arithmetic).
- **Safety vs. Speed**: `--dry-run` adds an extra step but prevents mistakes.
- **Extensibility**: New patterns can be added to `parse_pattern` without breaking changes.

## Future Work
- **Undo Support**: Track renames in a log file.
- **Interactive Mode**: Prompt for confirmation before renaming.
- **Plugins**: Support custom operations (e.g., `nlrename "hash filenames"`).

## Lessons Learned
- **Case Sensitivity**: Filters must be case-insensitive (e.g., `.PDF` vs `.pdf`).
- **Edge Cases**: Handle files without extensions (e.g., `LICENSE`).
- **Debugging**: Dry-run mode is essential for user trust.