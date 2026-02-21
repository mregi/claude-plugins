# memo-erstellen Plugin

Wissensquellen (Podcast, YouTube, Zitate, Gedanken) in strukturierte Memos verarbeiten.

## Installation

### Cowork (claude.ai)

1. In Cowork: `+` → Plugins → Persoenlich → **"Marketplace per URL hinzufuegen"**
2. URL eingeben: `https://github.com/mregi/claude-plugins.git`
3. Plugin `memo-erstellen` aktivieren/installieren
4. Neue Session starten — Commands erscheinen unter `/memo-erstellen:*`

> **Wichtig:** Die Option heisst "Marketplace **per URL** hinzufuegen" — nicht "von GitHub hinzufuegen". Letztere funktioniert nicht.

**YouTube in Cowork:** Unter claude.ai → Settings → Capabilities → "Additional allowed domains" diese Domains freischalten: `youtube.com`, `www.youtube.com`, `*.youtube.com`, `*.googlevideo.com`.

### CLI (Terminal)

```bash
# Marketplace hinzufuegen (einmalig)
claude plugin marketplace add mregi/claude-plugins

# Plugin installieren
claude plugin install memo-erstellen@mregi-plugins
```

> **Format:** `owner/repo` — nicht `github:owner/repo` (das gibt einen Fehler).

### Code-Tab / Chat-Tab (Desktop App)

Funktioniert automatisch wenn der Workspace-Ordner geoeffnet ist (`.claude/skills/` Wrapper). Commands heissen hier `/memo-podcast`, `/memo-youtube`, etc.

### Fallback: ZIP-Upload (Cowork)

Falls der GitHub-Marketplace nicht funktioniert:

1. `./build.sh` ausfuehren → erzeugt `_dist/memo-erstellen.zip`
2. In Cowork: `+` → Plugins → Persoenlich → Plugin hochladen → ZIP waehlen
3. Neue Session starten

## Erster Start — Wizard

Beim ersten Aufruf eines Commands fragt der Wizard:

1. **Memo-Pfad:** Wo sollen Memos gespeichert werden? (z.B. `~/Documents/memos`)
2. **Leserprofil:** Hast du ein bestehendes Profil? Pfad angeben oder Template verwenden.

Die persoenlichen Einstellungen werden unter `~/.claude/plugin-config/memo-erstellen/` gespeichert:
- `config.json` — Ausgabepfad
- `leserprofil.md` — Prinzipien und Referenzzitate

## Commands

| Command | Beschreibung |
|---------|-------------|
| `/memo-erstellen:podcast` | Podcast-Episode verarbeiten |
| `/memo-erstellen:youtube [url]` | YouTube-Video verarbeiten |
| `/memo-erstellen:zitat` | Zitat oder Notiz verarbeiten |
| `/memo-erstellen:gedanke` | Eigenen Gedanken festhalten |

## Was funktioniert wo?

| Command | Chat | Code-Tab / CLI | Cowork |
|---------|------|----------------|--------|
| Podcast (Sync) | — | ✅ (braucht macOS) | — |
| Podcast (Memo) | — | ✅ | ✅ |
| YouTube | — | ✅ | ✅ (Allowlist noetig) |
| Zitat | ✅ | ✅ | ✅ |
| Gedanke | ✅ | ✅ | ✅ |

## Voraussetzungen

- Python 3 (fuer Podcast-Sync und YouTube-Transkripte)
- `pip3 install youtube-transcript-api` (fuer YouTube)
- Apple Podcasts auf dem Mac (fuer Podcast-Sync)

Zitat und Gedanke brauchen keine Voraussetzungen.

## Leserprofil

Das Leserprofil definiert deine persoenliche Perspektive. Es beeinflusst die Denkanstoesse und Zitatauswahl — nicht die Zusammenfassung oder Kernbotschaft (die bleiben neutral).

Bearbeiten: `~/.claude/plugin-config/memo-erstellen/leserprofil.md`

## Deinstallation

```bash
claude plugin uninstall memo-erstellen@mregi-plugins
claude plugin marketplace remove mregi-plugins
```

Persoenliche Einstellungen bleiben unter `~/.claude/plugin-config/memo-erstellen/` erhalten.

## Version

1.1.0
