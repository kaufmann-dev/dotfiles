#!/usr/bin/env python3
"""Validate and score a synthetic-student run, render the HTML report, print an overview.

Usage: render.py RUN.json OUT.html
"""

import json
import sys
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "report.html"
PLACEHOLDER = '<script type="application/json" id="run-data">null</script>'

LABELS = {
    "de": ("Durchgang", "Richtig", "Zeit", "Ø Sek."),
    "en": ("Pass", "Correct", "Time", "Avg s"),
}


class RunError(Exception):
    pass


def fail(msg):
    raise RunError(msg)


def mmss(seconds):
    return f"{seconds // 60}:{seconds % 60:02d}"


def validate_question(q):
    n = q.get("n")
    if not isinstance(n, int):
        fail(f"question without integer 'n': {q.get('label')!r}")
    for field in ("label", "stem"):
        if not isinstance(q.get(field), str) or not q[field].strip():
            fail(f"question {n}: missing '{field}'")
    qtype = q.get("type")
    if qtype == "multi":
        options = q.get("options")
        if not isinstance(options, dict) or len(options) < 2:
            fail(f"question {n}: 'options' needs at least two entries")
        key = q.get("key")
        if not isinstance(key, list) or not key:
            fail(f"question {n}: 'key' must be a non-empty list of option letters")
        unknown = [k for k in key if k not in options]
        if unknown:
            fail(f"question {n}: key letters {unknown} are not options")
    elif qtype == "match":
        items, choices, key = q.get("items"), q.get("choices"), q.get("key")
        if not isinstance(items, dict) or not items:
            fail(f"question {n}: 'items' must be a non-empty object")
        if not isinstance(choices, list) or len(choices) < 2:
            fail(f"question {n}: 'choices' needs at least two entries")
        if not isinstance(key, dict) or set(key) != set(items):
            fail(f"question {n}: 'key' must map every item id to a choice")
        bad = [v for v in key.values() if v not in choices]
        if bad:
            fail(f"question {n}: key values {bad} are not choices")
    else:
        fail(f"question {n}: 'type' must be 'multi' or 'match'")


def score(q, selected):
    n = q["n"]
    if q["type"] == "multi":
        if not isinstance(selected, list):
            fail(f"question {n}: 'selected' must be a list of option letters")
        unknown = [s for s in selected if s not in q["options"]]
        if unknown:
            fail(f"question {n}: selected letters {unknown} are not options")
        chosen, key = set(selected), set(q["key"])
        if chosen == key:
            return "correct"
        return "partial" if chosen & key else "wrong"
    if not isinstance(selected, dict) or set(selected) != set(q["items"]):
        fail(f"question {n}: 'selected' must map every item id to a choice")
    bad = [v for v in selected.values() if v not in q["choices"]]
    if bad:
        fail(f"question {n}: selected values {bad} are not choices")
    right = sum(selected[i] == q["key"][i] for i in q["items"])
    if right == len(q["items"]):
        return "correct"
    return "partial" if right else "wrong"


def enrich(run):
    questions = run.get("questions")
    if not isinstance(questions, list) or not questions:
        fail("'questions' must be a non-empty list")
    for q in questions:
        validate_question(q)
    by_n = {q["n"]: q for q in questions}
    if len(by_n) != len(questions):
        fail("question numbers 'n' must be unique")

    passes = run.get("passes")
    if not isinstance(passes, list) or not 2 <= len(passes) <= 3:
        fail("'passes' must contain 2 or 3 passes")

    for p_index, p in enumerate(passes, 1):
        answers = p.get("answers")
        if not isinstance(answers, list):
            fail(f"pass {p_index}: 'answers' must be a list")
        seen = [a.get("n") for a in answers]
        if sorted(seen, key=str) != sorted(by_n, key=str):
            missing = sorted(set(by_n) - set(seen), key=str)
            extra = [n for n in seen if n not in by_n or seen.count(n) > 1]
            fail(f"pass {p_index}: must answer every question once (missing {missing}, extra/duplicate {sorted(set(extra), key=str)})")
        answers.sort(key=lambda a: [q["n"] for q in questions].index(a["n"]))
        for a in answers:
            secs = a.get("seconds")
            if not isinstance(secs, int) or isinstance(secs, bool) or secs <= 0:
                fail(f"pass {p_index}, question {a['n']}: 'seconds' must be a positive integer")
            a["result"] = score(by_n[a["n"]], a.get("selected"))
            a.setdefault("note", "")
        p["correct"] = sum(a["result"] == "correct" for a in answers)
        p["total"] = len(answers)
        p["seconds"] = sum(a["seconds"] for a in answers)

    final = passes[-1]
    wrong = [a["n"] for a in final["answers"] if a["result"] != "correct"]
    if wrong:
        fail(f"final pass {len(passes)} must be fully correct; not correct: {wrong}")

    warnings = []
    share = passes[0]["correct"] / passes[0]["total"]
    if not 0.45 <= share <= 0.75:
        warnings.append(f"pass 1 correct share is {share:.0%}, outside 45–75 %")
    if len(passes) == 3 and passes[0]["correct"] == passes[0]["total"]:
        warnings.append("pass 1 of a 3-pass run is already fully correct")
    for i in range(1, len(passes)):
        if passes[i]["seconds"] >= passes[i - 1]["seconds"]:
            warnings.append(f"pass {i + 1} is not faster than pass {i}")
    return warnings


def overview(run, html_path):
    head = LABELS.get(run.get("lang"), LABELS["de"])
    rows = [
        (str(i), f"{p['correct']}/{p['total']}", mmss(p["seconds"]), str(round(p["seconds"] / p["total"])))
        for i, p in enumerate(run["passes"], 1)
    ]
    widths = [max(len(head[c]), *(len(r[c]) for r in rows)) for c in range(4)]
    line = lambda cells: "| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |"
    out = [line(head), "| " + " | ".join("-" * w for w in widths) + " |"]
    out += [line(r) for r in rows]
    out += ["", str(html_path.resolve())]
    return "\n".join(out)


def main(argv):
    if len(argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    run_path, out_path = Path(argv[1]), Path(argv[2])
    try:
        run = json.loads(run_path.read_text(encoding="utf-8"))
        warnings = enrich(run)
    except (OSError, json.JSONDecodeError, RunError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    template = TEMPLATE.read_text(encoding="utf-8")
    if template.count(PLACEHOLDER) != 1:
        print(f"error: template placeholder missing in {TEMPLATE}", file=sys.stderr)
        return 1
    data = json.dumps(run, ensure_ascii=False).replace("<", "\\u003c")
    html = template.replace(PLACEHOLDER, f'<script type="application/json" id="run-data">{data}</script>')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    print(overview(run, out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
