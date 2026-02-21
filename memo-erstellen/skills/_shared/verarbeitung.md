# Verarbeitung — Gemeinsame Logik fuer alle Memo-Quellen

Erstelle aus dem Input ein strukturiertes Memo. Sprache = Sprache des Inputs.

## Konfiguration

### config.json

Pruefe ob `${CLAUDE_PLUGIN_ROOT}/config.json` existiert.

**Falls vorhanden →** Lies `memo_output_dir` und mache weiter.

**Falls NICHT vorhanden →** Ersteinrichtung:

1. Zeige dem User:
   > Willkommen bei memo-erstellen! Ich richte das Plugin fuer dich ein.
   >
   > **Wo sollen deine Memos gespeichert werden?**
   > (z.B. `~/Documents/memos` oder `~/Dropbox/workspace/wissen/memos`)

2. Warte auf Antwort des Users.

3. Erstelle `${CLAUDE_PLUGIN_ROOT}/config.json`:
   ```json
   { "memo_output_dir": "{vom-user-angegebener-pfad}" }
   ```

4. Erstelle den Zielordner + `_raw/` Unterordner falls noetig.

5. Erstelle `_index.md` im Zielordner falls nicht vorhanden:
   ```markdown
   # Memo-Index

   | Datum | Titel | Quelle | Labels |
   |-------|-------|--------|--------|
   ```

### leserprofil.md

Pruefe ob `${CLAUDE_PLUGIN_ROOT}/skills/_shared/leserprofil.md` existiert.

**Falls vorhanden →** Weiter.

**Falls NICHT vorhanden →** Kopiere `${CLAUDE_PLUGIN_ROOT}/skills/_shared/leserprofil-template.md` nach `${CLAUDE_PLUGIN_ROOT}/skills/_shared/leserprofil.md` und zeige dem User:
> Leserprofil aus Template erstellt. Memos sind erstmal neutral.
> Du kannst `leserprofil.md` spaeter personalisieren — trage deine Prinzipien und Referenzzitate ein, dann werden Denkanstoesse auf dich zugeschnitten.

### Ausgabepfad

Lies `${CLAUDE_PLUGIN_ROOT}/config.json` fuer den Ausgabepfad. Das Feld `memo_output_dir` bestimmt wo Memos gespeichert werden. Tilde (`~`) am Anfang durch den Home-Pfad des Users ersetzen.

## Frontmatter

```yaml
---
quelle: podcast | youtube | buch | zitat | artikel | eigener-gedanke
titel: {Titel des Memos}
datum: {YYYY-MM-DD des Originals}
labels: [label1, label2, label3]
# — Podcast-spezifisch:
podcast: {Name}
episode: {Titel}
dauer: {HH:MM:SS}
gast: {Name, Rolle — 1-2 Saetze}
track_id: {ID}
# — YouTube-spezifisch:
kanal: {Name}
url: {URL}
# — Zitat-spezifisch:
autor: {Name}
werk: {Buchtitel / Artikel / etc.}
# —
verarbeitet: {YYYY-MM-DD}
---
```

Nur relevante Felder verwenden. Nicht jede Quelle hat alle Felder.

**Labels:** 3-8 passende Labels waehlen, frei mischbar aus zwei Ebenen:

- **Themen-Labels** (breite Kategorien): `politik`, `wirtschaft`, `technologie`, `ai`, `bildung`, `gesellschaft`, `philosophie`, `schweiz`, `europa`, `usa`, `china`, `startup`, `leadership`, `investieren`, `gesundheit`, `recht`, `medien`, `wissenschaft`, `energie`, `verteidigung`
- **Spezifische Labels** (Personen, Vorlagen, Ereignisse): z.B. `boris-zuercher`, `abstimmung-energiegesetz`, `milei`, `lex-fridman`, `svp-initiative-xyz`

Beide Ebenen im gleichen Feld, z.B.:
```yaml
labels: [politik, schweiz, abstimmung-energiegesetz, boris-zuercher]
```

Spezifische Labels: Kleinbuchstaben, Bindestriche, so praezise wie noetig. Neue Labels duerfen jederzeit ergaenzt werden.

## Kernbotschaft

Die EINE zentrale Aussage in 1-2 Saetzen. Darunter 3-5 Unterbotschaften.

```markdown
## Kernbotschaft

{1-2 Saetze: Die zentrale These/Erkenntnis}

1. **{Unterbotschaft 1}** — {1 Satz Erklaerung}
2. **{Unterbotschaft 2}** — {1 Satz Erklaerung}
3. **{Unterbotschaft 3}** — {1 Satz Erklaerung}
```

**Ziel:** Auswendig lernbar. Wer Kernbotschaft + 3 Punkte kennt, kann das Memo in 30 Sekunden wiedergeben.

**Fallback** (wenn kein klares Argument, z.B. Interview mit vielen Themen):
→ **"Wichtigste Erkenntnisse"** als 3-5 eigenstaendige Punkte statt Kernbotschaft.

## Zusammenfassung

5-10 Saetze Fliesstext. Was wurde besprochen, welche Positionen, welche Schluesse. Keine Bullet Points.

Bei kurzen Inputs (Zitate, Gedanken): 2-3 Saetze reichen.

## Top-Zitate

Die 5-10 staerksten Originalzitate. Mit Timestamp falls verfuegbar. Lieber zu viele als zu wenige — Zitate sind das Herzstueck des Memos.

```markdown
## Top-Zitate

> „{Originalzitat}"
> — {Sprecher}, [{MM:SS}]
```

Waehle Zitate die: kraftvoll formuliert sind, eine These auf den Punkt bringen, ueberraschend/provokant sind, oder einen komplexen Sachverhalt elegant zusammenfassen.

Bei kurzen Inputs: Kann auch nur 1-2 Zitate sein.

## Kontext

2-3 Saetze: Wer spricht? Warum ist das Thema jetzt relevant? Welcher groessere Zusammenhang?

## Denkanstoesse

2-3 Fragen oder Impulse. Was sollte man weiterdenken? Was ist kontrovers? Was koennte man selbst anwenden?

Jeder Denkanstoß enthaelt ein **konkretes Beispiel** oder ein **Gedankenexperiment**, das die Frage greifbar macht. Keine abstrakten Fragen ohne Bezug.

**Schlecht:**
> Wie laesst sich Meinungsfreiheit in der digitalen Aera schuetzen?

**Gut:**
> Precht sagt, in den USA kann man jede Position zu Gaza oeffentlich vertreten. Aber gilt das auch fuer einen Google-Mitarbeiter, der intern protestiert und gefeuert wird? Ist "keine staatliche Zensur" genug, wenn private Arbeitgeber die Meinungsfreiheit faktisch einschraenken — und wie vertraegt sich das mit einem negativ-liberalen Freiheitsbegriff, der nur physischen Zwang als Unfreiheit sieht?

**Schlecht:**
> Was bedeutet das fuer die Schweiz?

**Gut:**
> In der Schweiz gibt es kein "umstritten"-Label in dieser Form — aber gibt es ein funktionales Aequivalent? Wer in Zuerich oeffentlich die Zuwanderung kritisiert, bekommt vielleicht kein Etikett, aber einen leeren Stuhl am naechsten Dinner. Ist sozialer Druck ohne physischen Zwang ein Freiheitsproblem — oder genau das, was eine liberale Gesellschaft aushalten muss?

## Datei speichern

```
{memo_output_dir}/{YYYY-MM-DD}_{titel-slug}.md
```

`{memo_output_dir}` = Wert aus `config.json`.

Dateiname: Kleinbuchstaben, Bindestriche, max 120 Zeichen. Datum = Datum des Originals.

## Rohtranskript ablegen (nur bei Podcast/YouTube)

Das Rohtranskript wird **nicht** ins Memo kopiert sondern als separate Datei abgelegt:

1. **Verschiebe** (nicht kopieren) das Transkript nach `{memo_output_dir}/_raw/{gleicher-dateiname-wie-memo}.txt`
2. Im Memo am Ende relativ verlinken:

```markdown
---
Rohtranskript: [_raw/{dateiname}.txt](_raw/{dateiname}.txt)
```

Bei kurzen Inputs (Zitate, Gedanken) entfaellt dieser Abschnitt.

## Cache-Verhalten

- **`_cache/episode-index.json`** — bleibt bestehen. Ist das Verzeichnis aller verfuegbaren Episoden. Wird bei jedem `podcast-sync.py`-Lauf aktualisiert.
- **`_cache/transcripts/{ID}.txt`** — wird nach Verarbeitung ins Memo verschoben. Bereits verarbeitete Episoden haben kein Transkript mehr im Cache.
- Wenn der User eine Episode nochmal verarbeiten will: erneut `podcast-sync.py` laufen lassen.

## Index aktualisieren

Nach jedem Memo: Zeile in `{memo_output_dir}/_index.md` ergaenzen:

```markdown
| {YYYY-MM-DD} | [{Titel}]({dateiname}.md) | {quelle} | {labels kommasepariert} |
```

Neuste Eintraege oben.

## Skalierung nach Input-Groesse

| Input | Kernbotschaft | Zusammenfassung | Zitate | Kontext | Denkanstoesse |
|-------|:---:|:---:|:---:|:---:|:---:|
| Podcast (30min+) | voll | 5-10 Saetze | 5-10 | ja | ja |
| YouTube (10-30min) | voll | 5-10 Saetze | 5-10 | ja | ja |
| Artikel / Buchkapitel | voll | 3-5 Saetze | 3-5 | ja | ja |
| Zitat / kurze Notiz | schlank (1+2) | 2-3 Saetze | optional | kurz | 1-2 |
| Eigener Gedanke | optional | 2-3 Saetze | — | optional | 1-2 |

## Hinweise

- Lange Transkripte (>1h): Trotzdem komplett verarbeiten.
- Mehrsprachig: Memo in der Hauptsprache des Inputs.
- Schlechte Transkriptqualitaet: Kurz am Anfang erwaehnen.
- Bei Unsicherheit lieber weniger Abschnitte als schlechte Qualitaet.
