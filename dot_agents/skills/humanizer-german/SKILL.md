---
name: humanizer-german
description: Remove signs of AI-generated writing from text written in the German language. Use only when the user explicitly invokes this skill or asks to humanize German text.
---

# Humanizer German

Überarbeite deutschsprachige Texte so, dass sie natürlich, präzise und zur
jeweiligen Textsorte passend klingen. Arbeite als Redakteur, nicht als
KI-Detektor: Einzelne Wörter, Satzzeichen oder ein sauberer Stil beweisen
nichts. Entscheidend sind gehäufte Muster und ihre Wirkung im konkreten Text.

Lies bei jeder Überarbeitung
[references/musterkatalog.md](references/musterkatalog.md). Er enthält die
deutschspezifischen Prüfmuster, Gegenbeispiele und Regeln gegen Überkorrektur.

## Grundsätze

- Bewahre Aussage, Fakten, Umfang, Argumentationsgang und wichtige Details.
- Erfinde keine Beispiele, Quellen, Zitate, Zahlen, Erfahrungen oder
  persönlichen Meinungen.
- Bewahre Textsorte und Register. Ein Vertrag, Fachtext oder Lexikonartikel
  darf nüchtern klingen; ein persönlicher Text darf Ecken und Rhythmus haben.
- Bewahre erkennbare deutsche, österreichische oder schweizerische
  Standardvarianten sowie Anrede, Genderstil und Fachterminologie.
- Übernimm eine bereitgestellte Schreibprobe als Stilvorlage. Achte dabei auf
  Satzrhythmus, Wortwahl, Direktheit, Gliederung und Zeichensetzung.
- Entferne kein Merkmal nur deshalb, weil es auf einer Liste steht. Korrigiere
  es nur, wenn es im Kontext gekünstelt, redundant oder unidiomatisch wirkt.
- Versprich weder eine zuverlässige Erkennung von KI-Texten noch die Umgehung
  automatischer Detektoren.

## Arbeitsablauf

1. **Auftrag klären:** Bestimme Textsorte, Zielgruppe, gewünschtes Register und
   erkennbare Sprachvarietät aus dem Ausgangstext und dem Nutzerauftrag.
2. **Musterbündel finden:** Suche anhand des Musterkatalogs nach gehäuften
   Auffälligkeiten. Markiere keine isolierten Treffer als Fehler.
3. **Substanz sichern:** Halte vor dem Umschreiben die Kernaussagen, Belege,
   Einschränkungen und unverzichtbaren Details fest.
4. **Natürlich umschreiben:** Ersetze abstrakte Behauptungen durch vorhandene
   konkrete Aussagen, streiche Redundanz und variiere den Satzbau. Formuliere
   direkt, aber nicht zwanghaft kurz.
5. **Deutsch prüfen:** Entferne unpassende englische Satzmuster und Denglisch,
   ohne etablierte Fachbegriffe einzudeutschen. Prüfe Bezüge, Wortstellung,
   Zusammensetzungen, Anführungszeichen und Zeichensetzung.
6. **Gegenlesen:** Lies die Fassung gedanklich laut. Suche nach gleichförmigem
   Rhythmus, künstlichen Übergängen, unbelegter Sicherheit und neuen
   Bedeutungsverschiebungen.

## Stilkalibrierung

Wenn eine Schreibprobe vorliegt, hat sie Vorrang vor allgemeinen
Natürlichkeitsregeln. Übernimm ihre wiederkehrenden Entscheidungen, aber keine
offensichtlichen Tippfehler. Ohne Schreibprobe gilt:

- Sachtexte: klar, konkret, zurückhaltend und ohne künstliche Dramaturgie.
- Technische Texte: terminologisch stabil, knapp und handlungsorientiert.
- Persönliche oder meinungsstarke Texte: erkennbarer Standpunkt und natürlicher
  Rhythmus, sofern der Ausgangstext dafür eine Grundlage bietet.

Füge nicht künstlich Umgangssprache, Modalpartikeln, Humor, Satzfragmente,
Selbstkorrekturen oder grammatische Fehler ein. Menschlich klingt ein Text
durch passende Entscheidungen, nicht durch absichtliche Unsauberkeit.

## Ausgabe

Gib standardmäßig aus:

1. die fertige überarbeitete Fassung;
2. danach höchstens eine knappe Zusammenfassung der wichtigsten Änderungen,
   wenn sie dem Nutzer hilft.

Zeige Analyse, Fundstellen und Zwischenfassung nur, wenn der Nutzer sie
ausdrücklich verlangt. Weise knapp darauf hin, wenn unklare oder unbelegte
Aussagen nicht seriös konkretisiert werden konnten.

## Abschlussprüfung

- Sind alle Kernaussagen und relevanten Details erhalten?
- Klingt der Text in seiner Textsorte idiomatisch deutsch?
- Wurden regionale Variante, Anrede, Genderstil und Fachbegriffe bewahrt?
- Sind Wiederholungen, Leerformeln und schematische Übergänge reduziert?
- Wurde nichts erfunden und keine legitime Eigenheit glattgebügelt?
