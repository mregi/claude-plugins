#!/usr/bin/env python3
"""
Helper: Exportiert Podcast-Metadaten + TTML-Pfade als JSON.
Einmal laufen lassen, danach kann Claude/Cowork alles lesen.

Usage:
    python3 scripts/podcast-sync.py
    python3 scripts/podcast-sync.py --cache-dir ~/Dropbox/workspace/wissen/memos/_cache
"""

import argparse
import glob
import json
import os
import re
import shutil
import sqlite3
import tempfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from html import unescape

PODCASTS_CONTAINER = os.path.expanduser(
    "~/Library/Group Containers/243LU875E5.groups.com.apple.podcasts"
)
TTML_BASE = os.path.join(PODCASTS_CONTAINER, "Library/Cache/Assets/TTML")
SQLITE_DB = os.path.join(PODCASTS_CONTAINER, "Documents/MTLibrary.sqlite")
SQLITE_WAL = SQLITE_DB + "-wal"
SQLITE_SHM = SQLITE_DB + "-shm"

# Plugin-Root automatisch relativ zum Script-Standort finden
PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_JSON = os.path.join(PLUGIN_DIR, "_cache", "episode-index.json")

CORE_DATA_EPOCH = datetime(2001, 1, 1, tzinfo=timezone.utc)

NS = {
    "tt": "http://www.w3.org/ns/ttml",
    "ttm": "http://www.w3.org/ns/ttml#metadata",
    "podcasts": "http://podcasts.apple.com/transcript-ttml-internal",
}


def parse_time(value):
    """Parse TTML timestamp to seconds. Handles: '12.345', '1:17.410', '1:02:17.410'"""
    parts = value.split(":")
    if len(parts) == 1:
        return float(parts[0])
    elif len(parts) == 2:
        return float(parts[0]) * 60 + float(parts[1])
    elif len(parts) == 3:
        return float(parts[0]) * 3600 + float(parts[1]) * 60 + float(parts[2])
    return 0.0


def format_timestamp(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"[{m:02d}:{s:02d}]"


def parse_ttml_to_text(filepath):
    """Parse TTML to readable text with timestamps and speakers."""
    tree = ET.parse(filepath)
    root = tree.getroot()
    lines = []
    current_speaker = None

    for p in root.iter(f"{{{NS['tt']}}}p"):
        speaker = p.get(f"{{{NS['ttm']}}}agent", "")
        begin = parse_time(p.get("begin", "0"))

        sentences = []
        for sent in p.findall(f".//{{{NS['tt']}}}span[@{{{NS['podcasts']}}}unit='sentence']"):
            words = []
            for w in sent.findall(f"{{{NS['tt']}}}span[@{{{NS['podcasts']}}}unit='word']"):
                if w.text:
                    words.append(unescape(w.text))
            if words:
                sentences.append(" ".join(words))

        if not sentences:
            words = []
            for w in p.findall(f".//{{{NS['tt']}}}span[@{{{NS['podcasts']}}}unit='word']"):
                if w.text:
                    words.append(unescape(w.text))
            if words:
                sentences.append(" ".join(words))

        text = " ".join(sentences).strip()
        if not text:
            continue

        parts = [format_timestamp(begin)]
        if speaker != current_speaker:
            current_speaker = speaker
            parts.append(f"**{speaker.replace('SPEAKER_', 'Sprecher ')}:**")
        parts.append(text)
        lines.append(" ".join(parts))

    return "\n\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Podcast-Sync: Apple Podcasts → Cache")
    parser.add_argument("--cache-dir", type=str, default=None,
                        help="Cache-Verzeichnis (default: {PLUGIN_DIR}/_cache)")
    args = parser.parse_args()

    global OUTPUT_JSON
    if args.cache_dir:
        cache_base = os.path.expanduser(args.cache_dir)
        OUTPUT_JSON = os.path.join(cache_base, "episode-index.json")
    else:
        cache_base = os.path.join(PLUGIN_DIR, "_cache")

    # 1. Load existing index (to preserve entries when Apple cleans up TTMLs)
    existing_index = {}
    if os.path.exists(OUTPUT_JSON):
        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            for entry in json.load(f):
                existing_index[entry["track_id"]] = entry
        print(f"📂 Bestehender Index: {len(existing_index)} Episoden")

    # 2. Find TTML files
    ttml_files = {}
    for path in glob.glob(os.path.join(TTML_BASE, "**/transcript_*.ttml"), recursive=True):
        match = re.search(r"transcript_(\d+)\.ttml", path)
        if match:
            ttml_files[match.group(1)] = path

    print(f"🔍 {len(ttml_files)} TTML-Transkripte in Apple Podcasts")

    # 3. Query SQLite for all track IDs (new from TTML + existing from index)
    all_track_ids = list(set(list(ttml_files.keys()) + list(existing_index.keys())))

    tmp_dir = tempfile.mkdtemp(prefix="podcast_sync_")
    try:
        tmp_db = os.path.join(tmp_dir, "MTLibrary.sqlite")
        shutil.copy2(SQLITE_DB, tmp_db)
        if os.path.exists(SQLITE_WAL):
            shutil.copy2(SQLITE_WAL, os.path.join(tmp_dir, "MTLibrary.sqlite-wal"))
        if os.path.exists(SQLITE_SHM):
            shutil.copy2(SQLITE_SHM, os.path.join(tmp_dir, "MTLibrary.sqlite-shm"))

        conn = sqlite3.connect(tmp_db)
        conn.row_factory = sqlite3.Row

        placeholders = ",".join(["?" for _ in all_track_ids])

        rows = conn.execute(f"""
            SELECT
                e.ZSTORETRACKID as track_id,
                e.ZTITLE as episode_title,
                e.ZAUTHOR as author,
                e.ZDURATION as duration,
                e.ZPUBDATE as pub_date,
                e.ZITEMDESCRIPTION as description,
                e.ZWEBPAGEURL as web_url,
                p.ZTITLE as podcast_title,
                p.ZAUTHOR as podcast_author
            FROM ZMTEPISODE e
            LEFT JOIN ZMTPODCAST p ON e.ZPODCAST = p.Z_PK
            WHERE e.ZSTORETRACKID IN ({placeholders})
        """, all_track_ids).fetchall()

        conn.close()
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # 4. Build index from SQLite results
    episodes = []
    for row in rows:
        tid = str(row["track_id"])
        pub_ts = row["pub_date"]
        pub_date = (CORE_DATA_EPOCH + timedelta(seconds=pub_ts)).strftime("%Y-%m-%d") if pub_ts else None

        dur = row["duration"]
        if dur:
            h, m, s = int(dur // 3600), int((dur % 3600) // 60), int(dur % 60)
            duration_str = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
        else:
            duration_str = None

        episodes.append({
            "track_id": tid,
            "ttml_path": ttml_files.get(tid, ""),
            "podcast": row["podcast_title"] or "?",
            "episode": row["episode_title"] or f"Track {tid}",
            "author": row["author"] or row["podcast_author"] or "?",
            "date": pub_date,
            "duration": duration_str,
            "description": (row["description"] or "").strip(),
            "web_url": row["web_url"] or "",
        })

    # Add TTML files without metadata
    found_ids = {e["track_id"] for e in episodes}
    for tid, path in ttml_files.items():
        if tid not in found_ids:
            episodes.append({
                "track_id": tid,
                "ttml_path": path,
                "podcast": "?",
                "episode": f"Track {tid}",
                "author": "?",
                "date": None,
                "duration": None,
                "description": "",
                "web_url": "",
            })
            found_ids.add(tid)

    # 5. Merge: keep existing entries that still have .txt in cache
    cache_dir = os.path.join(cache_base, "transcripts")
    os.makedirs(cache_dir, exist_ok=True)
    merged_count = 0

    for tid, entry in existing_index.items():
        if tid not in found_ids:
            cache_file = os.path.join(cache_dir, f"{tid}.txt")
            if os.path.exists(cache_file):
                episodes.append(entry)
                found_ids.add(tid)
                merged_count += 1

    if merged_count:
        print(f"🔄 {merged_count} Episoden aus bestehendem Cache uebernommen")

    # Sort by date descending
    episodes.sort(key=lambda e: e.get("date") or "0000", reverse=True)

    # 6. Parse and cache transcripts as plain text (only new TTMLs)
    for ep in episodes:
        tid = ep["track_id"]
        ttml_path = ep.get("ttml_path", "")
        cache_file = os.path.join(cache_dir, f"{tid}.txt")

        if not ttml_path or not os.path.exists(ttml_path):
            continue
        if os.path.exists(cache_file):
            # Skip if already cached and TTML hasn't changed
            if os.path.getmtime(cache_file) >= os.path.getmtime(ttml_path):
                continue

        print(f"   📝 Transkript parsen: {ep['episode'][:50]}...")
        try:
            text = parse_ttml_to_text(ttml_path)
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(text)
        except Exception as e:
            print(f"   ⚠️  Fehler bei {tid}: {e}")

    # 7. Write JSON
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    # Remove ttml_path from JSON (not needed, we have cached text)
    for ep in episodes:
        ep.pop("ttml_path", None)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(episodes, f, ensure_ascii=False, indent=2)

    print(f"\n✅ {len(episodes)} Episoden → {OUTPUT_JSON}")
    print(f"   Transkripte → {cache_dir}/")
    for ep in episodes:
        print(f"   {ep['date'] or '???'} | {ep['podcast'][:30]:<30} | {ep['episode'][:50]}")


if __name__ == "__main__":
    main()
