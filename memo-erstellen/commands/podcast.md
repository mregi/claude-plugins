---
description: Podcast-Episode zu strukturiertem Memo verarbeiten
argument-hint: "[episode-nummer]"
---

# Podcast → Memo

Verarbeitet eine Podcast-Episode aus Apple Podcasts zu einem strukturierten Memo.

Lies die gemeinsamen Regeln fuer Verarbeitung, Leserprofil und Fremdwoerter:
- [Verarbeitung](${CLAUDE_PLUGIN_ROOT}/skills/_shared/verarbeitung.md)
- [Leserprofil](${CLAUDE_PLUGIN_ROOT}/skills/_shared/leserprofil.md)
- [Fremdwoerter](${CLAUDE_PLUGIN_ROOT}/skills/_shared/fremdwoerter.md)

---

## Schritt 1: Sync pruefen

Pruefe ob `${CLAUDE_PLUGIN_ROOT}/_cache/episode-index.json` existiert.

- **Nicht vorhanden →** Automatisch ausfuehren:
  ```bash
  python3 ${CLAUDE_PLUGIN_ROOT}/scripts/podcast-sync.py
  ```
  Warte auf Abschluss, dann weiter.

- **Vorhanden →** Pruefe das Aenderungsdatum. Zeige dem User:
  > Podcast-Index vom {Datum}. {N} Episoden verfuegbar.

  Falls aelter als 7 Tage, zusaetzlich fragen:
  > Der Index ist {X} Tage alt. Neue Episoden gehoert? Soll ich den Sync ausfuehren?

  Falls User "ja" → Sync ausfuehren. Falls "passt" → weiter.

## Schritt 2: Episoden auflisten

Lies `${CLAUDE_PLUGIN_ROOT}/_cache/episode-index.json`. Zeige dem User die Liste:
- Nummer, Datum, Podcast, Episode, Dauer

Falls $ARGUMENTS eine Nummer enthaelt → direkt diese Episode waehlen.

Frage: **Welche Episode?**

## Schritt 3: Transkript laden

Lies `${CLAUDE_PLUGIN_ROOT}/_cache/transcripts/{TRACK_ID}.txt`.

**Falls die Datei nicht existiert:**
> Das Transkript fuer diese Episode fehlt im Cache. Ich fuehre den Sync nochmal aus.

Dann automatisch `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/podcast-sync.py` ausfuehren.

**Niemals** auf `podcast-export.py` ausweichen. Alles laeuft ueber den einen Sync-Befehl.

## Schritt 4: Metadaten

Aus `episode-index.json` uebernehmen: podcast, episode, datum, dauer, author.

## Schritt 5: Memo erstellen

Erstelle das Memo gemaess [Verarbeitung](${CLAUDE_PLUGIN_ROOT}/skills/_shared/verarbeitung.md).

Beachte das [Leserprofil](${CLAUDE_PLUGIN_ROOT}/skills/_shared/leserprofil.md) fuer Denkanstoesse und Zitatauswahl.

Beachte die [Fremdwort-Regeln](${CLAUDE_PLUGIN_ROOT}/skills/_shared/fremdwoerter.md).

## Schritt 6: Speichern + Index

Lies `${CLAUDE_PLUGIN_ROOT}/config.json` fuer `memo_output_dir`.

1. Memo speichern als `{memo_output_dir}/{YYYY-MM-DD}_{titel-slug}.md`
2. Rohtranskript verschieben: `_cache/transcripts/{TRACK_ID}.txt` → `{memo_output_dir}/_raw/{gleicher-dateiname}.txt`
3. `{memo_output_dir}/_index.md` aktualisieren (neuster Eintrag oben)
