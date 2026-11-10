---
name: humanizer
description: Rewrite English and German text so it does not read as AI-written, removing the patterns readers recognize as machine prose while preserving substance and the author's voice. Use only when the user explicitly invokes this skill.
---

# Humanizer

Rewrite English and German text so that a reader who knows what LLM prose looks
like finishes it without suspecting a machine wrote it. That is the goal. Clarity,
concision, and good structure matter here because they serve it, and substance
and voice are limits on how you reach it. A rewrite that is cleaner but still
reads as generated has failed.

The target is human readers. Do not judge who wrote the source, assign detection
scores, or promise a result from automated detectors.

## Know what gives text away

LLM prose is recognizable because it takes the most probable route at every
level. It picks the expected word, keeps sentences at an even middle length,
pads claims with significance, balances every paragraph, and closes on a tidy
summary. Readers notice the accumulation long before they can name a single
cause, so swapping out a few flagged words changes nothing. The tells sit at
five levels, and all five need attention:

- **Content.** Claims of importance, legacy, or broader trends with nothing
  concrete behind them. Promotional adjectives. Opinions attributed to unnamed
  experts, observers, or studies. Talk about where a subject was covered or
  listed in place of what the sources say. Stock sections on challenges and
  future outlook. Conclusions that restate the text. Disclaimers about limited
  information followed by plausible guesses, and coaching on how a claim
  should be read.
- **Construction.** Contrast framing that denies something nobody claimed ("not
  just X, but Y" and "Y rather than X"). Groups of three by reflex. Ranges whose endpoints share no
  scale. Clauses tacked on to interpret the sentence they end. Rhetorical
  questions answered at once. Reveals staged with a colon. Elaborate verbs where
  "is" or "has" would do. Announcements of what the text is about to say.
  Phrases that claim to reach a deeper truth and then restate the obvious.
- **Rhythm.** Sentences of similar length and shape, including the newer habit
  of short declarative sentences punctuated only by commas and periods.
  Paragraphs of equal size that each end on a quotable line. The same point
  made twice in different words. Self-contained paragraphs with no thread
  between them. The same idea named with a rotating set of synonyms. A
  transition word opening every other sentence.
- **Format.** Em dashes. Bold scattered for emphasis. Bullets that open with a
  bold label and a colon. Headings over single sentences. Title case. Decorative
  emoji. Lists where a paragraph would carry the reasoning.
- **Residue.** Anything addressed to the person who prompted the text: openers
  such as "Certainly!", praise for the question, offers to expand, and closing
  hopes that this helps.

The language references list the specific words, phrases, and examples. Read the
one that applies before rewriting, and both for mixed text:

- [English](references/english.md)
- [German](references/german.md)

## Set up the rewrite

Infer purpose, audience, genre, and register from the request, the text, and any
writing sample. Ask only when a material ambiguity cannot be resolved from that
context. If no text is supplied, ask for it.

Keep the input language unless translation is requested, and edit mixed-language
text in place. Follow explicit user choices first, then a supplied writing
sample, then the voice already present in the source. From a sample, take the
diction, rhythm, directness, and formality. Leave its facts and signature
phrases where they are.

List for yourself the claims, details, evidence, and qualifications the source
contains. That inventory is what must survive.

## Rewrite

Remove every tell, then fix what removing them exposes. A sentence built around
a tell rarely survives with the tell deleted: once "plays a pivotal role in the
evolving landscape" is gone, usually nothing is left, and the honest fix is to
state the concrete fact the source supplies or to cut the sentence. Rewrite as
deeply as that requires. Reorder paragraphs, merge overlapping ones, turn
decorative lists into prose, and drop template sections that say nothing.

Then give the text what generated prose lacks:

- Use the plain word. Repeat the right term instead of rotating synonyms.
- Let sentence length follow the content, so that short facts get short
  sentences and a real chain of reasoning gets a long one. Uneven is normal.
- Say a thing once, where it belongs, and stop when the content ends. Paragraphs
  may end on an ordinary sentence.
- Keep the specifics the source has: names, numbers, odd details, grounded
  asides, mixed feelings. Models round these off, and readers trust them.
- Connect sentences through their content. Use a transition word only where the
  relationship would otherwise be unclear.

### Do not trade one tell for another

Rewrites fail in predictable ways. Check for each:

- A stock phrase replaced with a different stock phrase.
- Em dashes replaced mechanically with semicolons or colons, so the same
  sentence shape survives under new punctuation.
- "It's not X, it's Y" split into "It's not X. It's Y."
- Rhythm varied by formula: two long sentences, then a three-word fragment for
  punch. Staccato fragments are as recognizable as the even cadence.
- Faked humanity. Do not insert slang, jokes, opinions, first-person anecdotes,
  rhetorical asides, modal particles, or deliberate mistakes that the source
  gives no basis for. A manufactured casual voice is itself a familiar machine
  register. In technical, legal, and reference writing, plain and dry is how
  people write.
- Compression into telegraphic notes with dropped subjects and articles.
- Over-polishing. Qualifiers such as "very" and "perhaps," flat superlatives,
  an occasional wordy phrase, and plain "is" and "has" sentences are more
  common in human writing than in generated text. Leave them unless they are
  wrong.

### Fixed rules

These apply to all editable prose unless the user says otherwise:

- No em dashes or en dashes as sentence punctuation, and no spaced hyphens or
  double hyphens standing in for them. Rebuild the sentence with a period,
  comma, colon, or parentheses, and avoid comma splices. Ranges ("2019–2024"),
  minus signs, and word hyphens stay.
- No decorative emoji and no bold used only for emphasis. Keep formatting that
  carries function: status symbols, literal syntax, document hierarchy, and
  headings, lists, or tables that readers navigate or compare with.
- Leave exact quotations, citations, code, URLs, and identifiers untouched.

## Stay inside the source

- Preserve names, numbers, dates, units, citations, attribution, negation, and
  degree of certainty. Possibility stays possibility and plans stay plans. A
  more direct sentence must not make a stronger claim.
- Use only what the source supplies. Do not invent an actor for a passive
  sentence, a source for a vague attribution, an example for an abstraction, or
  a fact to replace an empty claim. When the source offers nothing concrete,
  state the claim plainly with its attribution and uncertainty, or cut a
  sentence that carried no content.
- Keep every distinct substantive point. Cutting padding is expected.
  Summarizing is a different task.
- Keep the author's position, regional spelling, and deliberate stylistic
  choices. Passages that already read as written by a person stay as they are.
- If an ambiguity blocks a faithful rewrite, ask one focused question.

## Audit before delivering

Reread the draft as a skeptical reader and ask: what here would still make
someone think a model wrote it? Name the remaining tells, including any from the
list of rewrite failures, and revise. Repeat until the honest answer is nothing.
Then scan for `—` and `–` outside protected content, and compare the draft with
your inventory to confirm that nothing substantive was lost, added, or
strengthened.

Do this silently. Return only the finished text, in its intended format, without
an acknowledgment before it or an offer after it. Show the audit, drafts, or a
change summary only on request. If a point of substance could not be resolved,
say so in one short note separate from the text.
