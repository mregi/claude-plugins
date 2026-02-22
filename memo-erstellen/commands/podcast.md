---
description: Podcast-Episode zu strukturiertem Memo verarbeiten
argument-hint: "[episode-nummer]"
---

# Podcast → Memo

Verarbeitet eine Podcast-Episode aus Apple Podcasts zu einem strukturierten Memo.

Lies die gemeinsamen Regeln fuer Verarbeitung, Leserprofil und Fremdwoerter:
- [Verarbeitung](${CLAUDE_PLUGIN_ROOT}/skills/_shared/verarbeitung.md)
- [Fremdwoerter](${CLAUDE_PLUGIN_ROOT}/skills/_shared/fremdwoerter.md)

**Fuehre zuerst die Konfiguration (Schritt 1-3) aus `verarbeitung.md` aus.** Daraus ergibt sich `{memo_output_dir}`.

---

## Schritt 1: Index pruefen

Pruefe ob `{memo_output_dir}/_cache/episode-index.json` existiert und lies das Aenderungsdatum.

- **Nicht vorhanden →** Zeige:
  > Kein Podcast-Index vorhanden. Bitte im Mac-Terminal ausfuehren:
  > ```
  > podcast-sync
  > ```
  > Falls kein Alias eingerichtet:
  > ```
  > python3 "$(ls -1d ~/.claude/plugins/cache/mregi-plugins/memo-erstellen/*/scripts/podcast-sync.py | tail -1)"
  > ```
  > Bescheid geben wenn fertig.

  ⛔ **STOPP — NICHT weitermachen bis User "fertig" sagt.**

- **Vorhanden →** Frage:
  > Podcast-Index vom {Datum}. {N} Episoden. Aktualisieren?

  **Falls User ja sagt:**

  ⛔ **STOPP — NICHT weitermachen bis User "fertig" sagt.**

  Zeige dem User:
  > Bitte im Mac-Terminal ausfuehren:
  > ```
  > podcast-sync
  > ```
  > Falls kein Alias eingerichtet:
  > ```
  > python3 "$(ls -1d ~/.claude/plugins/cache/mregi-plugins/memo-erstellen/*/scripts/podcast-sync.py | tail -1)"
  > ```
  > Bescheid geben wenn fertig.

  Warte auf Bestaetigung. Dann `episode-index.json` **neu einlesen**. Weiter zu Schritt 2.

  **Falls User nein sagt** oder direkt eine Episode waehlt → weiter zu Schritt 2.

## Schritt 2: Episoden auflisten

Lies `{memo_output_dir}/_cache/episode-index.json`. Zeige dem User die Liste:
- Nummer, Datum, Podcast, Episode, Dauer

Falls $ARGUMENTS eine Nummer enthaelt → direkt diese Episode waehlen.

Frage: **Welche Episode?**

## Schritt 3: Transkript laden

Lies `{memo_output_dir}/_cache/transcripts/{TRACK_ID}.txt`.

**Falls die Datei nicht existiert:**
> Das Transkript fuer diese Episode fehlt im Cache. Ich fuehre den Sync nochmal aus.

Dann Sync wie in Schritt 1 ausfuehren.

**Niemals** auf `podcast-export.py` ausweichen. Alles laeuft ueber den einen Sync-Befehl.

## Schritt 4: Metadaten

Aus `episode-index.json` uebernehmen: podcast, episode, datum, dauer, author.

## Schritt 5: Memo erstellen

Erstelle das Memo gemaess [Verarbeitung](${CLAUDE_PLUGIN_ROOT}/skills/_shared/verarbeitung.md).

Beachte das [Leserprofil]({memo_output_dir}/_leserprofil.md) fuer Denkanstoesse und Zitatauswahl.

Beachte die [Fremdwort-Regeln](${CLAUDE_PLUGIN_ROOT}/skills/_shared/fremdwoerter.md).

## Schritt 6: Speichern + Index

1. Memo speichern als `{memo_output_dir}/{YYYY-MM-DD}_{titel-slug}.md`
2. Rohtranskript verschieben: `{memo_output_dir}/_cache/transcripts/{TRACK_ID}.txt` → `{memo_output_dir}/_raw/{gleicher-dateiname}.txt`
3. `{memo_output_dir}/_index.md` aktualisieren (neuster Eintrag oben)
