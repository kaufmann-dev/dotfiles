---
name: md-table-formatter
description: Run every time a markdown table is created or modified in any file.
---

# Markdown Table Formatter

```bash
python {skill_path}/format-table.py file.md
```

Pipe mode:
```bash
cat file.md | python {skill_path}/format-table.py
```

Valid tables only: 2+ rows, one must be a separator (`|---|---|`), all rows equal column count.
Invalid tables are left unchanged.