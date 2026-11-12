---
name: synthetic-student
description: Simulate a well-prepared student taking a multiple-choice quiz over three attempts, producing realistic answers, typical mistakes, and per-question answer times in tables. Use only when the user explicitly invokes this skill.
---

# Synthetic Student

Simulate how a real student who has read and studied the material performs on a
quiz over three attempts. For every attempt, report the chosen answers, whether
each is correct, and a realistic time in seconds. The output must be believable
as real student data: plausible mistakes, plausible times, no visible pattern.

## Input

- Questions arrive as screenshots or pasted text. Each has a stem, options
  (a, b, c, …), and sometimes a case description or data table shared by
  several questions.
- Treat every question as multi-select unless it states otherwise. A question
  is correct only when the selected set matches the key exactly.
- If two questions are identical, merge them into one and say so in one line
  before the tables.
- If the user supplies an answer key, use it. Otherwise solve every question
  carefully before simulating anything. Recompute numbers from the case data
  instead of trusting labels (for example relative market share = own share /
  share of the strongest competitor; growth = this year / last year − 1). If a
  key remains uncertain, flag the question in one line before the tables rather
  than guessing silently.
- If a question is unreadable or incomplete, ask about it before simulating.

## The simulated student

The student studied properly. They know most concepts and never guess at
random. Their mistakes are the ones such a student actually makes:

- **Under-selecting** in multi-select: choosing the clearly true options and
  missing a less obvious one. This is the most common mistake.
- **Plausible distractor**: choosing a false option whose wording sounds
  familiar from the material.
- **Neighboring concepts**: mixing up closely related ideas, such as Reife- vs.
  Wachstumsphase, Star vs. Cash Cow, or Kostenführerschaft vs.
  Differenzierung.
- **Wording traps**: missing a negation, an absolute ("immer", "nur"), or a
  reversed relationship ("je höher … desto geringer").
- **Case data slips**: reading the wrong row or column, treating a percentage
  as a ratio, or a small arithmetic error.

Rules for placing mistakes:

- Mistakes cluster on harder items: several correct options, subtle wording,
  calculations, case questions. Simple recall questions are usually right.
- Misconceptions stay consistent. If the student confuses two concepts, related
  questions show the same confusion until it is corrected.
- No artificial patterns: no mistake on every n-th question, no evenly spaced
  errors, no absurd answers, no identical or round times.

## Passes

- **Pass 1.** About 60–75 % of questions fully correct, with some partially
  correct (◐) among the rest.
- **Pass 2.** The student re-answers every question and knows which ones were
  wrong in Pass 1, but not the correct options (as in Moodle feedback).
  Previously correct answers stay the same and go faster. Previously wrong ones
  are reconsidered: most get fixed, but about 1–3 stay wrong or only partly
  fixed (for example, a missing option added while a wrong one stays selected).
  Rarely, one previously correct item slips. Overall about 85–95 % correct.
- **Pass 3.** Every answer is correct, and this is the fastest pass.

## Timing (seconds per question)

- **Pass 1.** Reading time for stem and options at about 3–4 words per second
  for German academic text, plus 3–6 s to weigh each option. Add 15–60 s for
  calculations or reading a data table. A case stem shared by consecutive
  questions is read in full only once; later questions on that case add only
  5–15 s of re-skimming. Hard or uncertain items take longer.
- **Pass 2.** About 55–75 % of the Pass 1 time. Previously correct items sit
  near the low end; previously wrong items stay relatively longer because the
  student reconsiders them.
- **Pass 3.** About 30–50 % of the Pass 1 time, with a floor of about 6–10 s
  (read, recognize, click).
- Use irregular whole numbers and do not scale times exactly in proportion
  between passes.

## Output

Write headings, labels, and notes in the quiz's language. The labels below are
for German quizzes. Output in this order:

1. Optional one-line notes: merged duplicates, uncertain keys.
2. `### Durchgang 1` as a table with these columns:

   | #   | Frage | Antwort | Ergebnis | Sek. | Lösung | Anmerkung |
   | --- | ----- | ------- | -------- | ---- | ------ | --------- |

   - `Frage`: a short topic label of at most five words, such as
     "Porter: Substitution".
   - `Antwort`: every chosen option as its letter plus its text, such as
     `**b)** Kostengünstigere Produkte mit ähnlichem Kundennutzen …`. Separate
     several options with ` · `. Trim options longer than about 15 words at a
     natural point and end them with `…`, keeping the part that identifies
     the option. Never show a letter alone.
   - `Ergebnis`: `✓` correct, `◐` partially correct, `✗` wrong.
   - `Sek.`: the answer time in whole seconds.
   - `Lösung` and `Anmerkung`: filled only on ◐ and ✗ rows, `—` otherwise.
     `Lösung` uses the same letter-plus-text format as `Antwort`. `Anmerkung`
     names the reason in a few words, such as "c übersehen" or "Star mit Cash
     Cow verwechselt".
   - Below the table: `Ergebnis: X/N richtig · Gesamtzeit m:ss`.
3. `### Durchgang 2` with the same columns and summary line.
4. `### Durchgang 3` with only `#`, `Frage`, `Antwort`, `Ergebnis`, and `Sek.`,
   since every answer is correct. Same summary line.
5. `### Überblick` as a small table with `Durchgang`, `Richtig`, `Gesamtzeit`,
   and `Ø Sek.`.

Give no preamble, no explanation of the method, and no closing offer unless the
user asks.

## Check before delivering

Silently confirm that:

- every ✓ matches the key exactly, and every ◐ or ✗ differs from it;
- every Pass 3 answer equals the key;
- Pass 2 keeps every Pass 1 ✓ answer unchanged except a deliberate rare slip;
- each pass's times follow the timing ranges relative to Pass 1;
- summary counts, total times, and averages match the table rows.
