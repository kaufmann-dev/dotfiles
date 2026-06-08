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


def split_row(line: str) -> list[str] | None:
    """Split a pipe-table row while preserving escaped pipe characters."""
    trimmed = line.strip()
    if not trimmed.startswith("|") or not trimmed.endswith("|"):
        return None

    cells = []
    current = []
    backslashes = 0

    for ch in trimmed[1:-1]:
        if ch == "|" and backslashes % 2 == 0:
            cells.append("".join(current))
            current = []
        else:
            current.append(ch)

        if ch == "\\":
            backslashes += 1
        else:
            backslashes = 0

    cells.append("".join(current))
    return cells


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


def is_table_row(line: str) -> bool:
    cells = split_row(line)
    return cells is not None and len(cells) > 0


def is_separator_row(line: str) -> bool:
    cells = split_row(line)
    return cells is not None and len(cells) > 0 and all(
        re.fullmatch(r"\s*:?-+:?\s*", cell) for cell in cells
    )


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

    rows = [split_row(line) for line in lines]
    if any(row is None for row in rows):
        return lines
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
            w = display_width(cell.strip())
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
    dw = display_width(text)
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
    fence = None

    while i < len(lines):
        line = lines[i]
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            marker = fence_match.group(1)
            if fence is None:
                fence = (marker[0], len(marker))
            elif marker[0] == fence[0] and len(marker) >= fence[1]:
                fence = None
            result.append(line)
            i += 1
            continue

        if fence is not None:
            result.append(line)
            i += 1
            continue

        if is_table_row(line):
            table_lines = [line]
            i += 1
            while i < len(lines) and is_table_row(lines[i]):
                table_lines.append(lines[i])
                i += 1

            separator_count = sum(is_separator_row(l) for l in table_lines)
            if len(table_lines) >= 2 and separator_count == 1:
                rows_split = [split_row(l) for l in table_lines]
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
