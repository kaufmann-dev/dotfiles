#!/usr/bin/env python3
"""Portable markdown table formatter. No dependencies beyond stdlib.

Usage:
    python format-table.py < input.md > output.md
    python format-table.py file.md
    echo "|a|b|" | python format-table.py
"""

import re
import sys
import unicodedata


def char_width(ch: str) -> int:
    """Return display width: 2 for CJK/wide chars, 1 otherwise."""
    code = ord(ch)
    if code < 0x20:
        return 0
    if code < 0x7F:
        return 1
    ea = unicodedata.east_asian_width(ch)
    if ea in ("F", "W"):
        return 2
    return 1


def display_width(text: str) -> int:
    return sum(char_width(ch) for ch in text)


def strip_markdown(text: str) -> str:
    """Strip markdown formatting for width calculation, preserving inline code content."""
    code_blocks = []

    def save_code(m):
        code_blocks.append(m.group(1))
        return f"\x00CODE{len(code_blocks) - 1}\x00"

    text = re.sub(r"`(.+?)`", save_code, text)

    prev = None
    while text != prev:
        prev = text
        text = re.sub(r"\*\*\*(.+?)\*\*\*", r"\1", text)
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
        text = re.sub(r"\*(.+?)\*", r"\1", text)
        text = re.sub(r"~~(.+?)~~", r"\1", text)
        text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)

    def restore_code(m):
        idx = int(m.group(1))
        return code_blocks[idx] if idx < len(code_blocks) else m.group(0)

    text = re.sub(r"\x00CODE(\d+)\x00", restore_code, text)
    return text


def is_table_row(line: str) -> bool:
    trimmed = line.strip()
    if not trimmed.startswith("|") or not trimmed.endswith("|"):
        return False
    return len(trimmed.split("|")) > 2


def is_separator_row(line: str) -> bool:
    trimmed = line.strip()
    if not trimmed.startswith("|") or not trimmed.endswith("|"):
        return False
    cells = trimmed.split("|")[1:-1]
    return len(cells) > 0 and all(re.match(r"^\s*:?-+:?\s*$", c) for c in cells)


def get_alignment(cell: str) -> str:
    cell = cell.strip()
    left = cell.startswith(":")
    right = cell.endswith(":")
    if left and right:
        return "center"
    if right:
        return "right"
    return "left"


def format_table(lines: list[str]) -> list[str]:
    sep_indices = {i for i, line in enumerate(lines) if is_separator_row(line)}

    rows = [line.strip().split("|")[1:-1] for line in lines]
    if not rows:
        return lines

    col_count = max(len(r) for r in rows)
    aligns = ["left"] * col_count

    for i in sep_indices:
        for j, cell in enumerate(rows[i]):
            if j < col_count:
                aligns[j] = get_alignment(cell)

    col_widths = [3] * col_count
    for i, row in enumerate(rows):
        if i in sep_indices:
            continue
        for j, cell in enumerate(row):
            w = display_width(strip_markdown(cell.strip()))
            col_widths[j] = max(col_widths[j], w)

    result = []
    for i, row in enumerate(rows):
        cells = []
        for j in range(col_count):
            raw = row[j].strip() if j < len(row) else ""
            align = aligns[j]
            w = col_widths[j]

            if i in sep_indices:
                cells.append(format_sep_cell(w, align))
            else:
                cells.append(pad_cell(raw, w, align))
        result.append("| " + " | ".join(cells) + " |")

    return result


def pad_cell(text: str, width: int, align: str) -> str:
    dw = display_width(strip_markdown(text))
    padding = max(0, width - dw)
    if align == "center":
        left = padding // 2
        right = padding - left
        return " " * left + text + " " * right
    elif align == "right":
        return " " * padding + text
    return text + " " * padding


def format_sep_cell(width: int, align: str) -> str:
    if align == "center":
        return ":" + "-" * max(1, width - 2) + ":"
    if align == "right":
        return "-" * max(1, width - 1) + ":"
    return "-" * width


def format_markdown_tables(text: str) -> str:
    lines = text.split("\n")
    result = []
    i = 0

    while i < len(lines):
        line = lines[i]
        if is_table_row(line):
            table_lines = [line]
            i += 1
            while i < len(lines) and is_table_row(lines[i]):
                table_lines.append(lines[i])
                i += 1

            if len(table_lines) >= 2 and any(is_separator_row(l) for l in table_lines):
                rows_split = [l.strip().split("|")[1:-1] for l in table_lines]
                col_count = len(rows_split[0])
                if all(len(r) == col_count for r in rows_split):
                    result.extend(format_table(table_lines))
                else:
                    result.extend(table_lines)
            else:
                result.extend(table_lines)
        else:
            result.append(line)
            i += 1

    return "\n".join(result)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    formatted = format_markdown_tables(content)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.stdout.write(formatted)


if __name__ == "__main__":
    main()
