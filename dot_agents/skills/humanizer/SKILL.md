---
name: humanizer
description: Rewrite English and German text to sound natural and purposeful, removing formulaic AI phrasing while preserving substance and the author's voice. Use only when the user explicitly invokes this skill.
---

# Humanizer

Rewrite English and German prose so it sounds like someone has something to say
and has chosen how to say it. Improve the writing as a whole: its focus, order,
rhythm, and phrasing. Removing a few conspicuous words is rarely enough.

Work as an editor. These patterns are reasons to examine a passage, not evidence
of who wrote it. Do not label text as AI-generated, assign detection scores, or
promise to evade detectors.

## Establish the editorial brief

Use the user's instructions, the supplied text, and any writing sample to infer
the purpose, audience, genre, register, and intended voice. Ask only when a
material ambiguity cannot be resolved from that context. If no text or source
is available, ask for it rather than producing a demonstration.

Preserve the input language unless translation is requested. Edit mixed-language
text in place, keeping each passage in its original language. Read the relevant
language guidance before rewriting:

- [English](references/english.md) for English passages.
- [German](references/german.md) for German passages.
- Both for mixed English/German text.

Follow explicit user choices first, then a supplied writing sample, then the
voice and conventions already present in the source. Match a sample's diction,
rhythm, directness, and level of formality; do not import its facts or copy its
distinctive phrases into unrelated material. Correct accidental errors without
erasing deliberate stylistic choices.

Without a sample, strengthen the source's existing voice. A technical explanation
can stay dry, a formal letter courteous, and an opinion piece opinionated. Do
not manufacture a more casual or more neutral persona. Preserve grounded humor,
asides, and mixed feelings; do not insert jokes, slang, first-person experiences,
opinions, or deliberate mistakes to simulate humanity.

## Preserve substance, reshape the writing

Before drafting, identify the distinct claims, relevant details, evidence,
qualifications, and relationships that must survive. Keep this inventory internal.

- Preserve names, numbers, dates, units, citations, attribution, negation, and
  degree of certainty. Possibility stays possibility, plans stay plans, and
  correlation does not become causation.
- Keep the author's position and substantive evaluations, promises, and
  limitations. Stronger prose must not make a stronger factual claim.
- Do not invent an actor for a passive sentence, a source for a vague attribution,
  a concrete example for an abstraction, or a benefit for a promotional claim.
  When combining clauses, keep each actor attached to the action the source
  assigns them; a nearby actor is not automatically responsible for an unstated
  one. Use only information supplied for this text. Editing does not imply
  fact-checking.
- If a claim lacks support or is ambiguous, preserve its attribution and
  uncertainty. Do not silently delete it, strengthen it, or replace it with a
  plausible fact. If the ambiguity prevents a faithful rewrite, ask a focused
  question; if it can remain unresolved in the text, add a brief note only when
  the reader needs to know.
- Protect exact quotations, citations, code, URLs, identifiers, and formatting
  with functional meaning. Edit surrounding prose rather than altering protected
  content to satisfy a style preference.

Rewrite as substantially as needed. Move the useful point forward, reorder
paragraphs, combine overlapping explanations, split overloaded sentences, and
replace a template structure with the order the argument actually needs.
Preserve logical and chronological relationships when moving material.

Cut repetition, empty rhetoric, and sentences that merely announce the next
sentence. Keep every distinct substantive point. There is no paragraph-count or
sentence-length target, and this is not a summarization task. Leave effective
passages alone; a rewrite does not need to change every line.

## Make each passage earn its place

Look for problems in the passage's effect, including clusters of formulaic
phrasing. An isolated weakness can still deserve an edit; a familiar word alone
does not.

- Inflated significance and abstract praise: replace them with an existing
  concrete action or consequence. If none is supplied, simplify the wording
  without inventing specificity or losing a substantive claim.
- Repeated framing and synthetic emphasis: remove ceremonial introductions,
  forced contrasts, artificial triplets, and generic conclusions when they add
  no meaning. Keep real contrasts, three-part lists, and useful summaries.
- Vague verbs and stacked abstractions: clarify who does what when the source
  supplies that information. Prefer precise verbs over corporate filler.
- Monotonous rhythm and synonym cycling: let emphasis and relationships shape
  sentence length. Repeat the right technical term rather than rotating through
  approximate synonyms. Do not replace a stock phrase with a new stock phrase.
- Unnecessary scaffolding: remove chatbot wrappers from standalone content.
  Preserve greetings and sign-offs that belong to an actual message or letter.
  Retain headings, lists, and tables when they help readers navigate, act, or
  compare; combine them when they merely decorate a short passage.
- Excessive hedging: remove redundant qualifiers while preserving the actual
  uncertainty. Keep necessary passive voice, specialist vocabulary, and formal
  constructions when they are accurate and appropriate for the audience.

## Apply the style constraints

These are output preferences, not tests of AI authorship. Apply them to editable
prose in both languages, subject to explicit user instructions:

- Do not use em dashes or en dashes as sentence punctuation, or substitute spaced
  hyphens or double hyphens for them. Use a period, comma, colon, parentheses, or
  a rewritten sentence that preserves the relationship. Avoid comma splices.
- Preserve range notation, minus signs, and correct word hyphenation. A blanket
  character replacement would damage valid uses and protected content.
- Remove decorative emoji and bold used only to add emphasis. Preserve symbols
  and formatting that convey functional meaning, such as status indicators,
  literal syntax, and document hierarchy. Keep inline code for a literal, but
  remove surrounding bold if it adds only emphasis.
- Keep language-appropriate quotation marks and capitalization. Do not flatten
  typography into English ASCII conventions or break compound spelling.

## Review and deliver

Read the draft for flow, then compare it against the source. Check that every
distinct point and relevant detail survived, evidence still supports the same
claims, and restructuring introduced no new implication. Check voice and idiom
against the brief and language guidance. Finally check the style constraints
outside protected content, distinguishing rhetorical dashes from valid notation.

Return only the finished text by default, in its intended format. Do not prepend
an acknowledgment or append an offer to keep editing. Show analysis, drafts,
comparisons, or a change explanation only when requested. Keep any necessary
note about unresolved substance brief and separate from the rewritten text.
