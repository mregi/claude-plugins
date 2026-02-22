# Claude Instructions — memo-erstellen Plugin

Plugin zur Verarbeitung von Wissensquellen (Podcast, YouTube, Zitate, Gedanken) in strukturierte Memos.

**GitHub-Repo:** `mregi/claude-plugins` (public)

---

## Architektur (Single-Path via Plugin-System)

```
projects/plugins/privat/memo-erstellen/   ← Source of Truth → GitHub mregi/claude-plugins
├── .claude-plugin/plugin.json            ← Plugin-Manifest
├── commands/                             ← Slash-Commands
│   ├── podcast.md                        → /memo-erstellen:podcast
│   ├── youtube.md                        → /memo-erstellen:youtube
│   ├── zitat.md                          → /memo-erstellen:zitat
│   └── gedanke.md                        → /memo-erstellen:gedanke
├── skills/_shared/                       ← Gemeinsame Logik (verarbeitung, fremdwoerter, leserprofile)
├── scripts/                              ← Python-Hilfsskripte
└── README.md

{memo_output_dir}/                        ← Memos-Ordner (z.B. ~/Dropbox/workspace/wissen/memos/)
├── _index.md                             ← Inhaltsverzeichnis aller Memos
├── _raw/                                 ← Rohtranskripte zu Memos
├── _cache/                               ← Transkripte, Indices (via Dropbox geteilt)
│   ├── episode-index.json
│   ├── youtube-index.json
│   └── transcripts/
├── _leserprofil.md                        ← Persoenliche Perspektive (einmal gewaehlt)
└── *.md                                  ← Memos

~/.claude/plugin-config/memo-erstellen/   ← Konfiguration (CLI + podcast-sync.py)
└── config.json                           ← memo_output_dir (von Plugin + Scripts gelesen)
```

**Ein Pfad fuer alle Umgebungen:** Alles laeuft ueber das Plugin-System (GitHub → Plugin-Cache). `${CLAUDE_PLUGIN_ROOT}` wird vom Plugin-System aufgeloest.

**Leserprofil + Cache im Memos-Ordner:** Beides liegt direkt im Output-Ordner. Damit funktioniert alles in Cowork (via gemounteten Ordner) ohne Setup-Wizard.

---

## Memos-Ordner finden (Auto-Discovery)

Das Plugin sucht den Memos-Ordner in dieser Reihenfolge:

1. **config.json** unter `~/.claude/plugin-config/memo-erstellen/` → `memo_output_dir` (CLI-Fall, persistent)
2. **Auto-Discovery:** `_index.md` im aktuellen Ordner → aktueller Ordner. Oder `wissen/memos/_index.md` → `./wissen/memos/` (Cowork-Fall)
3. **User fragen:** Einmalig nach Pfad fragen → config.json erstellen

---

## Learnings (Stand 2026-02-22)

Ueber 5 Sessions (18.–22. Feb) haben wir das Plugin in allen Claude-Umgebungen zum Laufen gebracht.

**v1.2.0:** Leserprofil und Cache in den Memos-Ordner verschoben. Auto-Discovery statt Wizard. Cowork braucht kein Setup mehr.

**v1.2.3–v1.2.6:** Wildcard-Bug gefixt (`| tail -1` waehlt neueste Plugin-Version). Cowork-Sync-Flow vereinfacht: einfache "Aktualisieren?"-Frage + ⛔ STOPP-Marker. Cowork AI respektiert den STOPP und wartet auf User-Bestaetigung.

**v1.2.7:** `podcast-sync.py` liest `config.json` automatisch — kein `--cache-dir` mehr noetig. Plugin ist plug-and-play auf jedem Mac. Shell-Alias `podcast-sync` in README dokumentiert.

---

### Kurz-Glossar

| Begriff | Bedeutung |
|---------|-----------|
| **Chat** | Der einfache Chat-Tab in der Claude Desktop App. Kann Dateien lesen/schreiben, aber KEINE Scripts ausfuehren. |
| **Code-Tab** | Der Code-Tab in der Claude Desktop App. Kann alles — Scripts, Internet, Dateien. Entspricht dem Terminal. |
| **Cowork** | Claudes kollaborative Umgebung (claude.ai/cowork). Laeuft auf einem Linux-Server, NICHT auf deinem Mac. |
| **CLI** | Claude Code im Terminal (`claude` Befehl). Gleiche Faehigkeiten wie Code-Tab. |
| **Plugin** | Ein Paket mit Commands, Scripts und einer Manifest-Datei (`plugin.json`). |
| **Command** | Ein Slash-Befehl wie `/memo-erstellen:podcast`. Wird durch Plugins bereitgestellt. |
| **Marketplace** | Ein Verzeichnis (lokal oder online) das Plugins auflistet. |

---

### Was funktioniert wo?

| Command | Code-Tab / CLI | Cowork |
|---------|----------------|--------|
| `/memo-erstellen:podcast` (Sync) | ja (nur hier — braucht macOS) | --- (Terminal-Befehl wird angezeigt) |
| `/memo-erstellen:podcast` (Memo) | ja | ja (Cache muss via Sync vorhanden sein) |
| `/memo-erstellen:youtube` | ja | ja (Allowlist noetig) |
| `/memo-erstellen:zitat` | ja | ja |
| `/memo-erstellen:gedanke` | ja | ja |

**Chat-Tab:** Nicht unterstuetzt (hat kein Plugin-System).

**Warum kann Cowork keinen Podcast-Sync?** Cowork laeuft auf einem Linux-Server. Der Sync liest die Apple Podcasts-Datenbank, die nur auf deinem Mac existiert. Loesung: Sync vorher auf dem Mac ausfuehren (Cache landet in Dropbox), danach kann Cowork das Memo erstellen.

**Warum braucht YouTube in Cowork eine Allowlist?** Cowork blockiert Internet-Zugriff standardmaessig. YouTube muss freigeschaltet werden unter claude.ai → Settings → Capabilities → "Additional allowed domains": `youtube.com`, `www.youtube.com`, `*.youtube.com`, `*.googlevideo.com`.

---

### Wie kommt das Plugin in jede Umgebung?

**Code-Tab + CLI: ueber GitHub-Marketplace**
- Plugin ist ueber GitHub-Repo `mregi/claude-plugins` installiert (public)
- Installation (einmalig): `claude plugin marketplace add mregi/claude-plugins` dann `claude plugin install memo-erstellen@mregi-plugins`
- Format fuer GitHub-Repos: `owner/repo` (NICHT `github:owner/repo`!)

**Cowork: ueber GitHub-Marketplace per URL**
- Weg: `+` → Plugins → Persoenlich → **"Marketplace per URL hinzufuegen"**
- URL: `https://github.com/mregi/claude-plugins.git`
- Plugin `memo-erstellen` aktivieren → neue Session starten
- **Wichtig:** Die Option heisst "per URL" — NICHT "von GitHub" (letztere funktioniert nicht)

---

### Wichtige Regeln fuer die Zukunft

**Source of Truth:** Immer nur hier editieren. Nach Aenderungen nach GitHub pushen.

**Nach Aenderungen am Plugin:**
1. Im Code-Tab/CLI: `claude plugin update memo-erstellen@mregi-plugins`
2. In Cowork: Plugin aktualisieren → neue Session starten
