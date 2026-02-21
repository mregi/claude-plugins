# memo-erstellen Plugin

Wissensquellen (Podcast, YouTube, Zitate, Gedanken) in strukturierte Memos verarbeiten.

## Setup

1. Python 3 installiert
2. `pip3 install youtube-transcript-api` (fuer YouTube-Transkripte)
3. Apple Podcasts auf dem Mac installiert (fuer Podcast-Transkripte)
4. **Ausgabepfad konfigurieren:**
   ```bash
   cp config-template.json config.json
   ```
   In `config.json` den `memo_output_dir` auf deinen Memo-Ordner setzen.

5. **Leserprofil einrichten:**
   ```bash
   cp skills/_shared/leserprofil-template.md skills/_shared/leserprofil.md
   ```
   Dann `leserprofil.md` mit deinen eigenen Prinzipien und Zitaten fuellen.

## Commands

```
/memo-erstellen:podcast              Podcast-Episode verarbeiten
/memo-erstellen:youtube [url]        YouTube-Video verarbeiten
/memo-erstellen:zitat                Zitat oder Notiz verarbeiten
/memo-erstellen:gedanke              Eigenen Gedanken festhalten
```

## Nutzung

Das Plugin laeuft in **Claude Code (Terminal)**. Podcast und YouTube (automatischer Download) brauchen Shell-Zugriff und Internet — das funktioniert nur im Terminal, nicht in Cowork.

Zitat und Gedanke funktionieren auch in Cowork (Desktop App), sofern der Memo-Ordner verlinkt ist.

## Ordner teilen

Der Plugin-Ordner kann via Dropbox/iCloud gesynct werden. Jeder User braucht eigene Dateien:
- `config.json` — eigener Ausgabepfad (aus `config-template.json` kopieren)
- `skills/_shared/leserprofil.md` — eigene Prinzipien (aus `leserprofil-template.md` kopieren)

Diese Dateien sind persoenlich und sollten **nicht** gesynct werden.

## Leserprofil

Das Leserprofil (`skills/_shared/leserprofil.md`) definiert deine persoenliche Perspektive. Es beeinflusst die Denkanstoesse und Zitatauswahl in den Memos — nicht die Zusammenfassung oder Kernbotschaft (die bleiben neutral).

## Version

1.0.0
