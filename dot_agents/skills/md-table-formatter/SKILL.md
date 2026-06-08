---
name: md-table-formatter
description: Run every time a markdown table is created or modified in any file.
---

# Markdown Table Formatter

Formats valid pipe tables with consistent spacing while preserving content,
column count, and left/center/right alignment markers. Padding is
Unicode/display-width aware and based on the Markdown source text. Escaped pipe
characters inside cells are preserved, and tables inside fenced code blocks are
left unchanged.

```bash
python {skill_path}/format-table.py file.md
```

Pipe mode:
```bash
cat file.md | python {skill_path}/format-table.py
```

The formatter prints Markdown to stdout; for tracked files, inspect the output
and apply edits through the normal file-editing workflow.

Valid tables only: 2+ rows, one separator row (`|---|---|`), equal column counts.
Invalid/uneven tables are left unchanged.

Finish only after confirming the table still has the intended rows, columns,
content, and alignment.
