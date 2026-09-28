---
name: improve-implementation-plan
description: Review and improve implementation plans by recovering true intent and re-deriving solutions from first principles. Use only when the user explicitly invokes this skill.
---

# Improve Implementation Plan

Someone has handed you an implementation plan and wants it improved. The instinct is to polish it: tidy the steps, add a testing phase, suggest a faster library. Resist that instinct. It is almost never where the value is.

A plan is a **frozen guess**. It was written at the moment its author understood the problem *least* — before building anything, before hitting the hard parts, often before they were sure what they were really trying to achieve. It encodes a stack of assumptions: that this thing should exist, that this is the right goal, that this is the right scope, that this architecture fits, that these are the tools to use. Any of those assumptions can be wrong, and the ones near the top of the stack — *should this exist? is this the right goal?* — are both the most likely to be wrong and the most expensive to get wrong.

Your job is not to improve the plan. **Your job is to figure out what the person actually wants, and produce the plan that best achieves *that*** — even if the result has a different stack, a different architecture, a different scope, or a different goal than what they brought you. Let their plan inspire you. Don't let it bind you.

## The stance: disciplined distrust

Treat every decision in the plan as a hypothesis to be tested, not a fact to be preserved. **The burden of proof is on keeping a decision, not on changing it.** Assume the plan is wrong in important ways until your analysis and the user's answers show otherwise — because that is usually true.

But distrust is not contrarianism. You are not here to be different for its own sake. Swapping the stack to look clever, or shrinking the scope reflexively, is the *same* failure as polishing — both ignore what the person actually needs. The target is **fit to true intent**. Diverge boldly, but tie every divergence to a real intent or constraint that the original choice fails to serve. These two rules hold at once: distrust everything, and justify everything.

## Where plans go wrong — work top-down

Plans can be wrong at five layers, from most consequential to least:

- **Premise** — Should this exist at all? Is the problem it claims to solve real, owned by this user, and worth solving? Many plans elaborate a solution to a problem the user doesn't actually have, or that an off-the-shelf product already solves.
- **Goal** — Is the end state it aims for the one that actually serves the need? People routinely aim at a proxy ("build a platform") instead of the outcome they want ("change a behavior," "answer a question," "save an hour a day").
- **Scope** — Is it the right size? Usually too big (gold-plating, premature generality, features no one asked for); sometimes too small (hand-waving the part that's actually hard).
- **Architecture** — Does the shape of the solution fit the goal and constraints, or is it borrowed from a much larger or different problem (microservices for one user, a queue with nothing to queue, custom auth where a library would do)?
- **Tactics** — Are the concrete choices (languages, frameworks, libraries, services) the right ones, or are they defaults, habits, or résumé-driven picks dressed up as decisions?

Spend your skepticism where the leverage is. A brilliant stack choice is worthless if the goal is wrong, so always work top-down.

## The workflow: Excavate → Interrogate → Re-derive → Deliver

Don't skip **Interrogate**. You cannot recover intent by staring at the artifact alone — you have to ask the person.

### 1. Excavate — reverse-engineer the intent

Read the whole plan first, charitably. Understand what it is trying to do before you judge it.

Then separate the **artifact** from the **intent**:

- In one or two sentences, write down the real-world outcome the plan is chasing. Ladder *up* from features to purpose: "This builds X. X exists to do Y. Y matters because Z." Keep asking "in service of what?" until you reach something that sounds like a human goal, not a technical one. That bottom line is your best guess at intent — and the thing you'll confirm with the user.
- Tag the plan's major decisions by layer (premise / goal / scope / architecture / tactics). For each, note whether it is **load-bearing** (the plan collapses without it) and whether it is **justified** (the plan gives a real reason) or merely **asserted**. Load-bearing *and* asserted = your prime suspects.

Hunt for smells — the tells that a plan has drifted from intent:

- Solving a problem the user doesn't have, or one an existing product already solves well.
- Scope inflation: gold-plating, "while we're at it," generality nobody asked for, day-one support for scale that may never arrive.
- Architecture borrowed from a bigger problem (microservices, queues, caches, custom auth) with no load to justify it.
- Résumé- or habit-driven tactics — the trendy framework, the language the author happens to know — presented as conclusions rather than choices.
- The hard part hand-waved. Plans lavish detail on the easy, familiar parts and gloss the one genuinely difficult thing. Find that thing.
- No audience and no definition of done. If the plan never says who it's for or how you'd know it worked, it's flying blind.

Finally, list the **load-bearing unknowns**: the assumptions that, if false, sink the plan. These become your questions. Do not start designing yet — you don't have intent confirmed.

### 2. Interrogate — ask the user what they actually want

This is the part most reviews skip, and it's where the real intent lives. You can analyze the artifact forever and still be guessing; the person is the only source of truth for what they want.

Two principles make the questions good:

**Ask about ends, not means.** The user is the world authority on what they're trying to achieve, who it's for, and what they can't change. They are usually *not* the authority on the best technical means — that's your job. So don't ask "Postgres or Mongo?" or "should we use microservices?" Ask what outcome they need, who uses it, how they'll know it worked, what's fixed. Turn their answers into technical decisions yourself.

**Target the gaps you actually found.** A generic questionnaire wastes everyone's time and signals you didn't read their plan. Tie each question to something specific in *their* plan and the unknowns you surfaced while excavating.

The high-leverage questions — pick the handful that would most change the plan; don't dump all of these:

- **The real outcome.** If this works perfectly, what changes for you or your users? What will someone be able to do afterward that they can't now?
- **Audience & context of use.** Who uses this, how often, where, with what expertise, on what device, alongside what else?
- **Definition of done.** How will you know it worked? What's the one thing that has to be true to call it a success?
- **The do-nothing test.** What happens if you build none of this? What's the cost of the status quo? (Reveals whether it's needed, and where the real pain is.)
- **Real constraints.** Time, budget, who's building it and what they know, deadlines, systems it must work with, expected scale, who maintains it afterward.
- **The smallest valuable version.** If you could ship only one thing this week, what would deliver the most value? (Finds the actual core.)
- **Provenance of the big choices.** For each major decision: is this a hard requirement, a strong preference, or just the first thing that came to mind / what you happened to know? (Separates constraints from defaults — often the single most useful question you can ask.)
- **The fear.** What's the part you're least sure about, or most worried about? (Usually the real hard problem, the one the plan hand-waved.)
- **Why build it.** Does something already exist that does most of this? What makes building it yourself worth it over buying or adopting?
- **Durability & ownership.** Throwaway prototype or long-lived system? Solo or a team? Will it need to grow?

Then **actually ask, and wait.** Pose your prioritized questions to the user and let them answer *before* you design — this back-and-forth is the point of the skill, not a formality. If you have an interactive way to offer choices (e.g. tappable options), use it; it's easier than making them type. If the user can't or won't answer — they say "just do it" or go quiet — don't stall: state the assumptions you're making explicitly, proceed, and flag them so they can correct you.

For an expanded question bank organized by what you're trying to learn, with example phrasings and guidance on sequencing and prioritizing, read `references/interrogation-toolkit.md`.

### 3. Re-derive — design from intent, not from the old plan

Now set the original plan aside. You're not editing it; you're solving the recovered intent fresh. (You'll reconcile with the original at delivery — but design first, without anchoring on it.)

- **Start from the outcome and the smallest valuable version.** What is the least you could build that delivers the core of what they want? Make that the spine, and grow outward only as the intent requires.
- **Generate two or three genuinely different approaches** — not three flavors of the same idea. Span the real space: build vs. buy vs. adapt-something-existing; different architectures; different scopes; and, where the intent points there, a different goal. If all your options look alike, you haven't searched widely enough.
- **Choose by fit to intent, then by simplicity.** Prefer the approach that fully serves the real need with the least incidental complexity. Every moving part is a cost paid forever; add it only for value the user actually wants.
- **Let the goal itself change if the intent demands it.** This is where the biggest wins hide. Divergence runs in three directions, and you should be open to all of them:
  - *Smaller / sideways into buying* — the grand plan should be a fraction of the size, or shouldn't be built at all because a product already does it (a custom CRM that should be a spreadsheet plus one automation; a from-scratch model that should be one API call).
  - *Bigger* — the plan under-scoped the part the whole thing depends on (a "we'll add multi-user later" foundation when the intent is multi-user from day one; a "quick scraper" the business will actually depend on, which needs real reliability and alerting).
  - *Elsewhere* — the right project is a *different* project than the one described (they planned a mobile app, but the audience and use-context call for a web tool; they planned to build, but they actually need to integrate two things they already have).
- **Name the hard part and make the plan confront it.** If excavation found a hand-waved difficulty, your plan must address it head-on and early, not bury it in a late phase.

The discipline rule, restated: **change a decision only when you can name the intent or constraint the original choice fails and the new one serves.** Hold a strong prior that meaningful change is the norm — plans are written before intent is understood — but never change something you can't justify. If a decision survives this scrutiny, keep it, and be ready to say why you considered changing it and didn't.

### 4. Deliver — the new plan, and why it diverges

Produce a real, buildable plan, plus enough reasoning that the user can follow your divergences and push back on them. Favor clear prose with light structure — this is a plan to act on, not a meta-essay. Use this shape, dropping any section that doesn't apply:

```
## What you're actually trying to do
2–4 sentences: the recovered intent — the real outcome, who it's for, and the
one thing that has to be true to call it a success. Everything below serves this.

## How this differs from your original plan
The key reframes. For each: what the original assumed → what your intent actually
implies → the change. Lead with the biggest divergences (premise / goal / scope /
architecture) before the smaller ones (stack / tactics).

## The plan
The actual implementation plan:
- Approach, in a sentence or two.
- Phased scope, with the smallest valuable version first.
- Architecture & stack, with each major choice justified by intent (not by fashion).
- The hard part and the real risks, and how the plan handles them.
- Sequence of work.
- Definition of done — tied to the real outcome, not to "shipped."

## What I kept on purpose
Brief: decisions from the original that survived scrutiny, and why.

## Assumptions & open questions
What I assumed in order to proceed, and what's still worth confirming — so you can
correct course.
```

Keep it tight. The new plan is the deliverable; the divergence section is its justification; the rest builds trust and invites correction. Be confident but not arrogant — you're proposing, the user decides — and explicitly invite pushback.

For a complete worked example — an original plan, the analysis, the questions, the recovered intent, and a re-derived plan that diverges substantially in stack, scope, and goal — read `references/worked-example.md`. Treat it as an illustration of the *method*, not a template to copy: your job is to find the divergences that *this* plan and *this* intent call for.

## What to avoid, and why

- **Don't polish — reimagine.** If your output mostly renames things and bolts on a "testing" section, you've failed the brief. The value is in questioning premises, not tidying details.
- **Don't diverge for sport.** Difference is not the goal; fit to intent is. A change you can't tie to a named intent or constraint is as much a mistake as leaving a bad decision in place.
- **Don't ask the user to architect.** Ask what they need and what's fixed; turn that into technical choices yourself. Making the user design the system defeats the purpose of bringing it to you.
- **Don't stall in questions.** Prioritize ruthlessly; if answers don't come, proceed on explicit, flagged assumptions rather than waiting forever.
- **Don't discard the original's real signal.** Genuine requirements, domain facts, and hard constraints buried in the plan are gold — carry them forward even as you replace the approach around them.
- **Don't rubber-stamp.** "This is already great" is a legitimate but rare conclusion, reached only after you've visibly tried to break the plan and failed. If you get there, show your work.
