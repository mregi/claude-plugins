---
description: Zitat oder Notiz zu strukturiertem Memo verarbeiten
---

# Zitat / Notiz → Memo

Verarbeitet ein Zitat, eine Buchnotiz oder einen Artikel-Ausschnitt zu einem strukturierten Memo.

Lies die gemeinsamen Regeln fuer Verarbeitung, Leserprofil und Fremdwoerter:
- [Verarbeitung](${CLAUDE_PLUGIN_ROOT}/skills/_shared/verarbeitung.md)
- [Fremdwoerter](${CLAUDE_PLUGIN_ROOT}/skills/_shared/fremdwoerter.md)

**Fuehre zuerst die Konfiguration (Schritt 1-3) aus `verarbeitung.md` aus.** Daraus ergibt sich `{memo_output_dir}`.

---

## Schritt 1: Input erfassen

Der User pastet Text (z.B. aus Apple Notes, einem Buch, einem Artikel).

Falls kein Text vorhanden: **Frage den User was er verarbeiten moechte.**

## Schritt 2: Kontext erfragen

Frage nach:
- **Quelle?** (Buch, Person, Artikel — wer hat das gesagt/geschrieben?)
- **Kontext?** (Worum ging es, warum relevant?)

Falls der User beides schon mitliefert → nicht nochmal fragen.

## Schritt 3: Memo erstellen

Erstelle das Memo gemaess [Verarbeitung](${CLAUDE_PLUGIN_ROOT}/skills/_shared/verarbeitung.md).

**Wichtig:** Bei kurzen Inputs (< 500 Woerter) die Skalierungstabelle beachten:
- Kernbotschaft: schlank (1 Satz + 2 Unterpunkte)
- Zusammenfassung: 2-3 Saetze
- Zitate: optional (1-2)
- Kontext: kurz
- Denkanstoesse: 1-2

Beachte das [Leserprofil]({memo_output_dir}/leserprofil.md) und die [Fremdwort-Regeln](${CLAUDE_PLUGIN_ROOT}/skills/_shared/fremdwoerter.md).

## Schritt 4: Speichern + Index

1. Memo speichern als `{memo_output_dir}/{YYYY-MM-DD}_{titel-slug}.md`
2. Kein Rohtranskript noetig (Input ist kurz genug fuers Memo)
3. `{memo_output_dir}/_index.md` aktualisieren (neuster Eintrag oben)
