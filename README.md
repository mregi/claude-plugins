# claude-plugins

Personal Claude Code plugin marketplace.

## Installation

```bash
claude plugin marketplace add github:mregi/claude-plugins
claude plugin install memo-erstellen@mregi-plugins
```

## Plugins

### memo-erstellen
Wissensquellen (Podcast, YouTube, Zitate, Gedanken) in strukturierte Memos verarbeiten.

Commands:
- `/memo-erstellen:podcast` — Podcast-Episode zu Memo
- `/memo-erstellen:youtube` — YouTube-Video zu Memo
- `/memo-erstellen:zitat` — Zitat/Notiz zu Memo
- `/memo-erstellen:gedanke` — Eigener Gedanke als Memo

## Setup (nach Installation)

1. `config-template.json` kopieren nach `config.json`
2. `memo_output_dir` anpassen (Pfad wo Memos gespeichert werden)
3. Optional: `leserprofil-template.md` kopieren nach `leserprofil.md` und anpassen
