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

## Podcast-Sync

### Wie funktioniert es?

1. **Apple Podcasts** cacht Transkripte als TTML-Dateien (nur wenn der Transkript-Tab geoeffnet wird)
2. **`podcast-sync.py`** liest die Apple Podcasts-Datenbank + TTMLs, konvertiert zu Klartext und speichert alles im `_cache/`-Ordner
3. **Das Plugin** liest den Cache und erstellt daraus strukturierte Memos

Der Cache wird via Dropbox geteilt — einmal auf dem Mac synchronisiert, ueberall verfuegbar.

### Shell-Alias einrichten

In `~/.zshrc` einfuegen:

```bash
alias podcast-sync='python3 "$(ls -1d ~/.claude/plugins/cache/mregi-plugins/memo-erstellen/*/scripts/podcast-sync.py | tail -1)"'
```

Danach reicht im Terminal: `podcast-sync` — das Script liest den Memos-Ordner aus `config.json` automatisch.

### Podcast-Sync in Cowork

Cowork laeuft auf einem Linux-Server und hat keinen Zugriff auf die Apple Podcasts-Datenbank. Das Plugin erkennt das und zeigt stattdessen den Terminal-Befehl an, den man auf dem Mac ausfuehren soll. Danach kann Cowork das Memo aus dem synchronisierten Cache erstellen.

## Update

```bash
# CLI
claude plugin update memo-erstellen@mregi-plugins
```

In Cowork: Plugin aktualisieren → neue Session starten.

> **Tipp:** Nach einem Update alte Plugin-Cache-Versionen unter `~/.claude/plugins/cache/mregi-plugins/memo-erstellen/` loeschen. Es sollte nur die aktuelle Version dort liegen.

## Troubleshooting

| Problem | Loesung |
|---------|---------|
| Kein Transkript fuer eine Episode | In Apple Podcasts die Episode oeffnen → Transkript-Tab anklicken → warten bis es geladen ist. Dann `podcast-sync` erneut ausfuehren. |
| `podcast-sync` findet keinen Memos-Ordner | `config.json` unter `~/.claude/plugin-config/memo-erstellen/` pruefen. Inhalt: `{ "memo_output_dir": "~/pfad/zu/memos" }` |
| YouTube in Cowork blockiert | Unter claude.ai → Settings → Capabilities → "Additional allowed domains" freischalten: `youtube.com`, `www.youtube.com`, `*.youtube.com`, `*.googlevideo.com` |
| Plugin-Commands erscheinen nicht | Neue Session in Cowork starten. In CLI: `claude plugin install memo-erstellen@mregi-plugins` |
| Falsches Script wird ausgefuehrt | Alte Plugin-Versionen im Cache loeschen (siehe Update-Tipp oben) |

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

## Changelog

| Version | Datum | Aenderung |
|---------|-------|-----------|
| 1.2.7 | 2026-02-22 | podcast-sync.py Auto-Detect aus config.json. Shell-Alias. Cowork: STOPP-Marker fuer Sync-Flow. Wildcard-Bug gefixt. |
| 1.2.0 | 2026-02-21 | Leserprofil + Cache in Memos-Ordner. Auto-Discovery. Zentrale Config. GitHub-Marketplace. |
| 1.1.0 | 2026-02-20 | Offizielles Plugin-Format (`commands/`). Frontmatter-Fix. |
| 1.0.0 | 2026-02-18 | Erster Release: 4 Commands, Podcast-Sync, Label-System. |
