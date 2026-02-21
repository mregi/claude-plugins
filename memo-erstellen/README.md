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

### Fallback: ZIP-Upload (Cowork)

Falls der GitHub-Marketplace nicht funktioniert:

1. `./build.sh` ausfuehren → erzeugt `_dist/memo-erstellen.zip`
2. In Cowork: `+` → Plugins → Persoenlich → Plugin hochladen → ZIP waehlen
3. Neue Session starten

## Erster Start

Beim ersten Aufruf ermittelt das Plugin den Memos-Ordner automatisch:

1. **config.json** unter `~/.claude/plugin-config/memo-erstellen/` (falls vorhanden)
2. **Auto-Discovery:** Sucht `_index.md` im aktuellen Ordner oder unter `wissen/memos/`
3. **Fallback:** Fragt nach dem Pfad und speichert ihn in `config.json`

Falls kein Leserprofil vorhanden ist (`{memo_output_dir}/_leserprofil.md`), wird einmalig eines der verfuegbaren Profile zur Auswahl angeboten:
- der-liberale, der-linke, der-rechte, der-woke, der-iyi, template

Das Leserprofil liegt im Memos-Ordner — einmal gewaehlt, funktioniert es ueberall (CLI, Cowork).

## Commands

| Command | Beschreibung |
|---------|-------------|
| `/memo-erstellen:podcast` | Podcast-Episode verarbeiten |
| `/memo-erstellen:youtube [url]` | YouTube-Video verarbeiten |
| `/memo-erstellen:zitat` | Zitat oder Notiz verarbeiten |
| `/memo-erstellen:gedanke` | Eigenen Gedanken festhalten |

## Was funktioniert wo?

| Command | Code-Tab / CLI | Cowork |
|---------|----------------|--------|
| Podcast (Sync) | ja (braucht macOS) | Terminal-Befehl wird angezeigt |
| Podcast (Memo) | ja | ja (Cache muss vorhanden sein) |
| YouTube | ja | ja (Allowlist noetig) |
| Zitat | ja | ja |
| Gedanke | ja | ja |

## Ordnerstruktur

```
{memo_output_dir}/                 z.B. ~/Dropbox/workspace/wissen/memos/
├── _index.md                      Inhaltsverzeichnis
├── _raw/                          Rohtranskripte
├── _cache/                        Transkript-Cache (via Dropbox geteilt)
│   ├── episode-index.json
│   ├── youtube-index.json
│   └── transcripts/
├── _leserprofil.md                 Persoenliche Perspektive
└── *.md                           Memos
```

## Voraussetzungen

- Python 3 (fuer Podcast-Sync und YouTube-Transkripte)
- `pip3 install youtube-transcript-api` (fuer YouTube)
- Apple Podcasts auf dem Mac (fuer Podcast-Sync)

Zitat und Gedanke brauchen keine Voraussetzungen.

## Deinstallation

```bash
claude plugin uninstall memo-erstellen@mregi-plugins
claude plugin marketplace remove mregi-plugins
```

## Version

1.2.2
