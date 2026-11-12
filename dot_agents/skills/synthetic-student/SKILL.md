---
name: synthetic-student
description: Simulate a well-prepared student taking a multiple-choice or matching quiz over two or three attempts, with realistic mistakes and answer times, rendered as a local HTML report with a play-along timer and answer-key corrections. Use only when the user explicitly invokes this skill.
---

# Synthetic Student

Simulate how a real student who has read and studied the material performs on a
quiz over several attempts. For every attempt, decide the chosen answers and a
realistic time in seconds. The result must be believable as real student data:
plausible mistakes, plausible times, no visible pattern. The output is a local
HTML report; the terminal only gets a short overview.

## Files

- Output folder: the folder the user names, otherwise the current working
  directory. Create it if it does not exist.
- Run data and report: `<folder>/synthetic-student-<YYYY-MM-DD-HHMM>-<slug>.json`
  and `.html` with the same name.
- Corrections store: `<folder>/synthetic-student-corrections.json`, shaped
  `{"items": [...]}`, unless the user names another corrections file.

## 1. Corrections first

While playing along (Ablauf) or in the answer-key tab, the report shows what
would have been correct for every question and lets the user confirm it or
mark it as wrong. A correction applies to the open report at once: every pass
is re-scored against the corrected key and the final pass answers with it.
Corrections are copied as a block that starts
with `synthetic-student corrections v1`, followed by a JSON line
`{"items": [...]}`. Each item carries `label`, `type`, `stem`, optional
`context`, `options` (multi) or `items` and `choices` (match), the corrected
`key`, and an optional `note`.

- If the prompt contains such a block, merge its items into the corrections
  store. An item with the same stem and the same options or items replaces the
  stored one. Report the number of merged items in one line. If the prompt
  contains nothing else, stop there.
- Before solving a quiz, read the store if it exists. Match each question by
  content: stem plus option or item texts, tolerating small OCR differences
  and a different option order. When a correction matches, its key is the
  answer key (remap letters if the order differs) and the question gets
  `"corrected": true`. Mention applied corrections in one line.

## 2. Input

- Questions arrive as screenshots or pasted text: a stem, options or items, and
  sometimes a case description or data table shared by several questions.
- **Types.** A question is `match` when each statement gets one choice from a
  shared list (for example statement → X/Y). Otherwise it is `multi`; treat it
  as multi-select unless it says otherwise.
- If two questions are identical, merge them and say so in one line.
- Without a correction, solve every question carefully before simulating.
  Recompute numbers from the case data instead of trusting labels (relative
  market share = own share / share of the strongest competitor; growth = this
  year / last year − 1). If a key remains uncertain, name the question in one
  line rather than guessing silently.
- If a question is unreadable or incomplete, ask before simulating.

## 3. The simulated student

The student studied properly, knows most concepts, and never guesses at
random. Their mistakes are the ones such a student actually makes:

- **Under-selecting** in multi-select: choosing the clearly true options and
  missing a less obvious one. This is the most common mistake.
- **Plausible distractor**: a false option whose wording sounds familiar.
- **Neighboring concepts**: Reife- vs. Wachstumsphase, Star vs. Cash Cow,
  Kostenführerschaft vs. Differenzierung, and the like.
- **Wording traps**: a missed negation, absolute ("immer", "nur"), or reversed
  relationship ("je höher … desto geringer").
- **Case data slips**: wrong row or column, a percentage read as a ratio, a
  small arithmetic error.
- **Matching**: swapping two related pairs, or putting a borderline statement
  into the neighboring category.

Mistakes cluster on harder items (several correct options, subtle wording,
calculations, case questions, long matching sets); simple recall questions are
usually right. A misconception stays consistent across related questions until
it is corrected. Avoid artificial patterns: no mistake on every n-th question,
no evenly spaced errors, no absurd answers, no identical or round times.

## 4. Number of passes

Decide before simulating and write one short sentence why into `passReason`.

- **3 passes** for a hard quiz: case or calculation items, several
  multi-select questions with three or more correct options, long matching
  sets, or subtle wording traps.
  - Pass 1: about 60–75 % fully correct.
  - Pass 2: the student re-answers everything and knows which answers were
    wrong, but not the right options. Previously correct answers stay the
    same; most wrong ones get fixed, but about 1–3 stay wrong or only partly
    fixed. Rarely, one previously correct item slips. About 85–95 % correct.
  - Pass 3: everything correct.
- **2 passes** for a simple recall quiz.
  - Pass 1: about 65–80 % fully correct.
  - Pass 2: everything correct; previously wrong items are reconsidered.

The final pass is always fully correct and the fastest.

## 5. Timing

Seconds per question:

- **Pass 1**: reading time for stem and options at about 3–4 words per second
  for German academic text, plus 3–6 s per option or 3–5 s per matching item.
  Add 15–60 s for calculations or reading a data table. A case shared by
  consecutive questions is read in full only once; later questions add 5–15 s
  of re-skimming. Hard or uncertain items take longer.
- **Later passes**, relative to Pass 1:

  | Pass   | 3-pass run        | 2-pass run        |
  | ------ | ----------------- | ----------------- |
  | Pass 2 | 55–75 % of Pass 1 | 40–60 % of Pass 1 |
  | Pass 3 | 30–50 % of Pass 1 | —                 |

  Previously correct items sit at the low end; previously wrong items stay
  relatively longer because the student reconsiders them.
- Floor of about 6–10 s per question. Use irregular whole numbers and do not
  scale times exactly in proportion.

## 6. Output

Write the run JSON, then render it:

```json
{
  "title": "Strategisches Management – Quiz 3",
  "lang": "de",
  "created": "2026-11-12T14:03",
  "passReason": "Viele Fallfragen mit Rechenschritten, daher 3 Durchgänge.",
  "questions": [
    {
      "n": 1, "label": "Porter: Substitution", "type": "multi",
      "context": null,
      "stem": "Zu den fünf Wettbewerbskräften laut Porter …",
      "options": {"a": "…", "b": "…", "c": "…", "d": "…"},
      "key": ["b", "d"],
      "corrected": false
    },
    {
      "n": 2, "label": "McGregor: Theorie X/Y", "type": "match",
      "context": null,
      "stem": "Ordnen Sie die Aussagen zu.",
      "items": {"1": "Braucht konkrete Anweisungen", "2": "Hohe Selbstkontrolle"},
      "choices": ["X", "Y"],
      "key": {"1": "X", "2": "Y"},
      "corrected": false
    }
  ],
  "passes": [
    {"answers": [
      {"n": 1, "selected": ["b"], "seconds": 48, "note": "d übersehen"},
      {"n": 2, "selected": {"1": "X", "2": "Y"}, "seconds": 37, "note": ""}
    ]}
  ]
}
```

- `lang` is the quiz language (`de` or `en`); `label` is a topic of at most
  five words; `stem` and `options` are the full original texts; `context` holds
  shared case text including a data table as plain text, or `null`.
- `note` names the reason for a mistake in a few words in the quiz language
  ("c übersehen", "Star mit Cash Cow verwechselt"); leave it empty on correct
  answers.
- Do not write results or totals. The script scores every answer against the
  key and computes totals.

Run:

```bash
python3 {skill_path}/scripts/render.py <folder>/<name>.json <folder>/<name>.html
```

An error means the data is invalid or the final pass is not fully correct: fix
the data and run again. A warning means a pass looks implausible: revise the
simulation unless there is a good reason.

Then print only the one-line notes (merged duplicates, uncertain keys, applied
or merged corrections), the overview table the script printed, and the HTML
path. No per-question tables in the terminal, no method explanation, no
closing offer.

## 7. Check before delivering

The script verifies scoring, totals, and the final pass. Check the rest
silently:

- every mistake is plausible for a prepared student and consistent with
  related questions;
- Pass 2 keeps every answer that was correct in Pass 1, except a rare
  deliberate slip;
- times follow the ranges above, are not round, and do not scale exactly in
  proportion.
