---
description: YouTube-Video zu strukturiertem Memo verarbeiten
argument-hint: "[youtube-url]"
---

# YouTube → Memo

Verarbeitet ein YouTube-Video zu einem strukturierten Memo.

Lies die gemeinsamen Regeln fuer Verarbeitung, Leserprofil und Fremdwoerter:
- [Verarbeitung](${CLAUDE_PLUGIN_ROOT}/skills/_shared/verarbeitung.md)
- [Fremdwoerter](${CLAUDE_PLUGIN_ROOT}/skills/_shared/fremdwoerter.md)

**Fuehre zuerst die Konfiguration (Schritt 1-3) aus `verarbeitung.md` aus.** Daraus ergibt sich `{memo_output_dir}`.

---

## Schritt 1: Transkript beschaffen

Drei Wege, in dieser Reihenfolge pruefen:

### 1a. Transkript aus Cache

Video-ID aus $ARGUMENTS oder User-URL extrahieren. Pruefe ob `{memo_output_dir}/_cache/transcripts/yt_{VIDEO_ID}.txt` existiert.

- **Ja →** Transkript laden, Metadaten aus `{memo_output_dir}/_cache/youtube-index.json` holen. Weiter mit Schritt 2.
- **Nein →** Weiter mit 1b.

### 1b. Script ausfuehren

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/youtube-transcript.py --cache-dir "{memo_output_dir}/_cache" "$ARGUMENTS"
```

Falls `youtube-transcript-api` nicht installiert:
```bash
pip3 install youtube-transcript-api
```

Warte auf Abschluss, dann Transkript aus Cache laden.

### 1c. User pastet Transkript direkt

Falls der User das Transkript direkt in den Chat pastet (z.B. von YouTube kopiert), das als Input verwenden. Kein Cache-File, kein Rohtranskript-Ablage noetig.

## Schritt 2: Metadaten

- Aus `{memo_output_dir}/_cache/youtube-index.json` uebernehmen falls vorhanden: title, author.
- Zusaetzlich via Websuche ergaenzen falls noetig: Datum, Kanal, Kontext.
- Falls User das Transkript direkt pastet: User nach Metadaten fragen oder aus Kontext ableiten.

## Schritt 3: Memo erstellen

Erstelle das Memo gemaess [Verarbeitung](${CLAUDE_PLUGIN_ROOT}/skills/_shared/verarbeitung.md).

Beachte das [Leserprofil]({memo_output_dir}/_leserprofil.md) fuer Denkanstoesse und Zitatauswahl.

Beachte die [Fremdwort-Regeln](${CLAUDE_PLUGIN_ROOT}/skills/_shared/fremdwoerter.md).

## Schritt 4: Speichern + Index

1. Memo speichern als `{memo_output_dir}/{YYYY-MM-DD}_{titel-slug}.md`
2. Rohtranskript verschieben (bei Cache-Variante): `{memo_output_dir}/_cache/transcripts/yt_{VIDEO_ID}.txt` → `{memo_output_dir}/_raw/{gleicher-dateiname}.txt`
3. `{memo_output_dir}/_index.md` aktualisieren (neuster Eintrag oben)
