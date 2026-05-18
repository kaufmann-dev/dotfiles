---
name: md-table-formatter
description: "Use this skill when the user asks to format Markdown tables, or when Markdown tables you are editing or generating need aligned columns while preserving their content and alignment markers."
---

# Markdown Table Formatter

## Purpose

Format Markdown tables with consistent spacing, alignment markers, and display-width-aware padding.

## Workflow

1. Locate the skill directory and bundled script.
2. Run the formatter against a file or input text:

```bash
python path/to/md-table-formatter/format-table.py file.md
```

The script prints formatted Markdown to stdout. For tracked files, inspect the output and apply the resulting edit through the normal file-editing workflow.

## Behavior

- Formats only pipe tables with a separator row.
- Preserves left, center, and right alignment.
- Uses Unicode-aware display widths.
- Calculates width from visible Markdown text where possible.
- Leaves invalid or uneven tables unchanged.

## Output

Aligned Markdown tables with the same content and structure.

## Completion Rules

Finish only after confirming the table still has the intended rows, columns, and alignment.
