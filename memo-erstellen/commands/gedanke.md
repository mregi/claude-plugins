---
description: Eigenen Gedanken als Memo festhalten
---

# Eigener Gedanke → Memo

Haelt einen eigenen Gedanken, eine Idee oder eine Reflexion als strukturiertes Memo fest.

Lies die gemeinsamen Regeln fuer Verarbeitung, Leserprofil und Fremdwoerter:
- [Verarbeitung](${CLAUDE_PLUGIN_ROOT}/skills/_shared/verarbeitung.md)
- [Leserprofil](~/.claude/plugin-config/memo-erstellen/leserprofil.md)
- [Fremdwoerter](${CLAUDE_PLUGIN_ROOT}/skills/_shared/fremdwoerter.md)

---

## Schritt 1: Gedanken erfassen

Der User tippt seinen Gedanken direkt. Falls nichts da → Frage: **Was geht dir durch den Kopf?**

## Schritt 2: Memo erstellen

Erstelle das Memo gemaess [Verarbeitung](${CLAUDE_PLUGIN_ROOT}/skills/_shared/verarbeitung.md).

**Schlankstes Format** (siehe Skalierungstabelle):
- Kernbotschaft: optional (nur wenn klar formulierbar)
- Zusammenfassung: 2-3 Saetze
- Zitate: entfaellt (ist ja eigener Gedanke)
- Kontext: optional
- Denkanstoesse: 1-2 (was koennte man weiterdenken?)

Frontmatter: `quelle: eigener-gedanke`, `datum: {heute}`.

Beachte das [Leserprofil](~/.claude/plugin-config/memo-erstellen/leserprofil.md) — auch eigene Gedanken duerfen kritisch hinterfragt werden.

## Schritt 3: Speichern + Index

Lies `~/.claude/plugin-config/memo-erstellen/config.json` fuer `memo_output_dir`.

1. Memo speichern als `{memo_output_dir}/{YYYY-MM-DD}_{titel-slug}.md`
2. Kein Rohtranskript noetig
3. `{memo_output_dir}/_index.md` aktualisieren (neuster Eintrag oben)
