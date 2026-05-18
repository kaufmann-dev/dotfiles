---
name: md-table-formatter
description: Formats markdown tables to be properly aligned and readable. Use when the user asks to format tables, or when you generate or encounter misaligned markdown tables that need cleanup.
---

# Markdown Table Formatter

Formats markdown tables with proper column alignment, consistent spacing, and separator row formatting.

## When to Use

- User explicitly asks to format a markdown table
- You're about to write a markdown table and want readable output
- An existing table in the codebase or conversation is misaligned
- After generating documentation with tables

## How to Format

Run the bundled script on the file or pipe the table text to it:

```bash
python {skill_path}/format-table.py file.md
```

Or pipe content directly:

```bash
cat << 'EOF' | python {skill_path}/format-table.py
|Name|Age|City|
|---|---|---|
|Alice|30|New York|
|Bob|25|London|
EOF
```

## What It Does

- **Column alignment** — Supports left (`:---`), center (`:---:`), and right (`---:`) alignment from the separator row
- **Consistent spacing** — Pads cells to uniform column widths based on content
- **Unicode-aware** — CJK characters, emojis, and wide Unicode characters are counted with correct display width
- **Markdown stripping** — Bold, italic, strikethrough, links, and images are stripped for width calculation (concealment-mode compatible)
- **Inline code preservation** — Markdown symbols inside backticks are treated as literal text, preserving their width

## Rules

- Only format lines that look like tables: start with `|`, end with `|`, have 3+ pipe-delimited cells
- A valid table must have at least 2 rows including a separator row (`|---|---|`)
- All rows must have the same number of columns
- Invalid tables are left unchanged — no silent corruption

## Edge Cases Handled

| Case | Behavior |
|------|----------|
| Mixed CJK + ASCII | Width calculated correctly per character |
| Nested markdown (`**bold _italic_**`) | Multi-pass stripping |
| Inline code (`\`**not bold**\``) | Preserved as-is |
| Empty cells | Padded to column width |
| Links `[text](url)` | Width from text only |
| Images `![alt](url)` | Width from alt text only |
