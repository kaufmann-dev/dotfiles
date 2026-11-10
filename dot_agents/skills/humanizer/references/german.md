# German tells

German machine prose has two layers of tells: the general LLM patterns, and
English sentence habits carried into German. Readers notice the second layer
first, because the text sounds translated. Remove both wherever they appear in
editable text. The phrase lists help you find the patterns, and the sentence
around a listed phrase usually has to change as well.

## Translated English

**Calqued formulas.** „Am Ende des Tages“, „Lass uns eintauchen“, „Tauchen wir
ein“, „In der heutigen schnelllebigen Welt“, „In einer Welt, in der …“, „Es ist
wichtig zu beachten, dass“, „Es ist erwähnenswert“, „Wenn es um … geht“, „macht
den Unterschied“, „Das macht Sinn“, „Hier ist der Punkt“, „eine Reise“ for any
process. Say it the way German does, which is usually shorter.

Before:
> Am Ende des Tages ist es die klare Zuständigkeit, die den Unterschied macht:
> Sie verhindert doppelte Arbeit.

After:
> Klare Zuständigkeiten verhindern doppelte Arbeit.

**English commas.** A comma after a sentence-initial adverbial is wrong in
German and an immediate sign of translation: „Darüber hinaus, bietet das Tool
…“, „Im Jahr 2020, wurde …“. Remove it and check the verb position.

**Cleft sentences.** „Es ist X, das …“ and „Was wirklich zählt, ist …“ copy
English emphasis. Put the stressed element first and use normal word order.

**Participle chains.** English "-ing" clauses rebuilt with the Partizip I:
„den Austausch fördernd“, „die Bedeutung unterstreichend“. Use finite verbs.
Ordinary attributive forms such as „die geltenden Regeln“ and „steigende
Preise“ are fine.

Before:
> Das Programm bringt die Beteiligten zusammen, den Austausch fördernd und die
> gemeinsame Planung erleichternd.

After:
> Das Programm bringt die Beteiligten zusammen, fördert den Austausch und
> erleichtert die gemeinsame Planung.

**Denglisch.** „Learnings“, „Pain Points“, „Key Takeaways“, „Insights“,
„challengen“, „leveragen“, „Impact generieren“, „adressieren“ for problems.
Replace them with the German word for what is meant. Keep established technical
terms, product names, and loanwords the audience uses: „Repository“, „Deploy“,
and „Stakeholder“ can be correct.

Before:
> Unsere wichtigsten Learnings aus den Interviews sind, dass Nutzer den Export
> nicht finden und die Fehlermeldungen nicht verstehen.

After:
> Die Interviews zeigen: Nutzer finden den Export nicht und verstehen die
> Fehlermeldungen nicht.

**Title case and English hyphenation.** German headings use sentence
capitalization. Compounds are written together or hyphenated by German rules,
so „Nutzer Erlebnis“ and „Daten-getrieben“ are errors.

## Vocabulary

**Inflated significance:** „entscheidender Meilenstein“, „von zentraler
Bedeutung“, „spielt eine entscheidende Rolle“, „unterstreicht eindrucksvoll“,
„steht sinnbildlich für“, „prägt nachhaltig“, „in einer sich stetig wandelnden
Welt“, „die Landschaft“ of any field.

**Promotional adjectives:** „einzigartig“, „innovativ“, „zukunftsweisend“,
„beeindruckend“, „facettenreich“, „vielfältig“, „nahtlos“, „maßgeschneidert“,
„ganzheitlich“, „umfassend“, „spannend“, „setzt neue Maßstäbe“.

**Transitions and frames:** „Darüber hinaus“, „Des Weiteren“, „Zudem“,
„Zugleich“, „Nicht zuletzt“, „In diesem Zusammenhang“, „Vor diesem
Hintergrund“, „Zusammenfassend lässt sich sagen“, „Abschließend lässt sich
festhalten“, „Insgesamt zeigt sich“.

**Intensifiers and hedges:** „äußerst“, „zweifellos“, „besonders
hervorzuheben“, „grundsätzlich lässt sich sagen“, „möglicherweise potenziell“.

State the concrete property or consequence the source gives, and drop the rest.
A transition stays only where the relationship would be unclear without it.

Before:
> Die Eröffnung markiert einen bedeutenden Meilenstein für die kulturelle
> Landschaft der Region. Die innovative Plattform bietet zudem ein nahtloses
> Nutzererlebnis.

After:
> Mit der Eröffnung bekommt die Region ein Theater. Über die Plattform lassen
> sich Karten buchen.

(The after version assumes the source supplies those facts. If it does not,
state the claim plainly without the adjectives.)

## Content and construction

**Vague authority.** „Experten sind sich einig“, „Studien zeigen“, „Beobachter
betonen“, „allgemein gilt“. Name the source the text supplies. If there is
none, keep the claim as uncertain as it was. Never invent a source.

**Negative parallelism.** „Nicht nur X, sondern auch Y“ by reflex. „Es geht
nicht um X. Es geht um Y.“ „Kein X. Kein Y. Nur Z.“ Say the positive claim.

**Triplets and false ranges.** „Schnell, einfach und zuverlässig.“ „Von der
Planung bis zur Umsetzung, von Start-ups bis zu Konzernen.“ Keep three items
only when there are three things, and list what is actually covered.

**Staged reveals and questions.** „Das Ergebnis? Mehr Effizienz.“ „Und genau
hier liegt der Schlüssel.“ „Kurz gesagt:“ State the point in a normal sentence.

**Template sections.** „Chancen und Herausforderungen“, „Ausblick“, „Fazit“ on
a short text, and endings such as „Trotz bestehender Herausforderungen blickt
das Unternehmen einer vielversprechenden Zukunft entgegen.“ Keep any concrete
fact inside and delete the frame.

**Serial sentence openings.** „Dies zeigt … Dies verdeutlicht … Dies
unterstreicht …“ Replace the series with what is actually shown.

**Synonym cycling.** „das Unternehmen … der Konzern … die Firma … der
Marktführer“ for the same company. Pick the term and repeat it, especially for
technical terms.

**Nominal style and Funktionsverbgefüge.** „zur Durchführung bringen“, „eine
Bewertung vornehmen“, „im Rahmen der Umsetzung“, „erfolgt“. Models overproduce
these. Use the verb when the source says who acts. Keep nominal constructions
that the genre needs, such as legal or administrative precision, and never
invent an actor.

Before:
> Nach Durchführung der Prüfung nimmt das Team eine Bewertung der Ergebnisse
> vor. Anschließend trifft das Team eine Entscheidung über eine Wiederholung
> des Tests.

After:
> Nach der Prüfung bewertet das Team die Ergebnisse und entscheidet, ob der
> Test wiederholt werden soll.

**Faked informality.** Do not add „halt“, „eben“, „ja“, „mal“, or a chummy „du“
to sound human. Keep the address form the source uses.

## Format

- **Gedankenstriche.** The spaced dash („ – “) is the German counterpart of the
  em dash tell. Rewrite every one used as sentence punctuation with a period,
  comma, colon, or parentheses. Dashes in ranges and exact quotations stay.
- **Bold-label bullets, emoji, headings over single sentences.** Handle them as
  the main workflow describes.
- **Quotation marks.** Keep the document's convention, such as „…“ or «…».
  Typographic quotes are normal German punctuation.
- **Regional forms.** Keep German, Austrian, or Swiss spelling and vocabulary
  („Grüsse“, „Jänner“) and the source's gender convention („Mitarbeiter:innen“,
  Paarform, generic masculine). Normalizing them erases the author.
- **Ellipses in interface text.** Labels such as „Datei auswählen“ stay short.

## Residue

Delete conversation with the prompter: „Gerne!“, „Natürlich!“, „Gute Frage!“,
„Hier ist ein Überblick“, „Ich hoffe, das hilft“, „Lass mich wissen, wenn …“,
„Möchten Sie mehr erfahren?“ Greetings and closings that belong to a real
letter or e-mail stay.

## Certainty survives the rewrite

Keep the distinctions between „kann“, „könnte“, „soll“, „muss“, and „wird“,
together with their attribution. Plans do not become guarantees, and reported
claims do not become the narrator's own.

Before:
> Laut dem internen Bericht könnte die Maßnahme möglicherweise zu einer
> Verkürzung der Wartezeit um bis zu zwei Tage führen. Daten aus dem Winter
> liegen allerdings noch nicht vor.

After:
> Laut dem internen Bericht könnte die Maßnahme die Wartezeit um bis zu zwei
> Tage verkürzen. Daten aus dem Winter fehlen noch.
