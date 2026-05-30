# Design Document: Natural Language File Renamer (`nlrename`)

## Overview
`nlrename` is a CLI tool that translates natural language commands into file renaming operations. It is designed for users who want to rename files without memorizing `mv` flags or writing regex.

## Goals
- **Simplicity**: Use plain English to describe renaming operations.
- **Flexibility**: Support common use cases (case transformations, date patterns, string replacements).
- **Safety**: Provide a dry-run mode to preview changes.

## Architecture
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User     │ →  │  CLI       │ →  │  Renamer   │
└─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Pattern    │    │  File      │    │  OS        │
│  Parser     │    │  System    │    │  Rename    │
└─────────────┘    └─────────────┘    └─────────────┘
```

### Components
1. **CLI**: Uses `click` for argument parsing and help text.
2. **Pattern Parser**: Translates natural language into file operations.
3. **File System**: Uses `os` and `os.path` for file operations.
4. **OS Rename**: Uses `os.rename` to apply changes.

## Pattern Matching Logic
The tool uses keyword matching to identify the user's intent:

| Keyword | Action |
|---------|--------|
| `lowercase` | Convert filename to lowercase |
| `uppercase` | Convert filename to uppercase |
| `title case` | Convert filename to title case |
| `today's date` | Prepend/append today's date |
| `replace X with Y` | Replace `X` with `Y` in the filename |
| `regex "X" with "Y"` | Replace regex `X` with `Y` |
| `append X` | Append `X` to the filename |
| `prepend X` | Prepend `X` to the filename |

## Error Handling
- **File Not Found**: Skip files that do not exist.
- **Permission Denied**: Skip files that cannot be renamed.
- **Invalid Patterns**: Ignore unsupported patterns.

## Testing
- **Unit Tests**: Test individual pattern matching logic.
- **Integration Tests**: Test end-to-end renaming operations.
- **Edge Cases**: Test with special characters, long filenames, and nested directories.

## Future Work
- **Custom Patterns**: Allow users to define their own patterns.
- **Undo Functionality**: Support undoing the last renaming operation.
- **GUI**: Build a graphical interface for non-CLI users.