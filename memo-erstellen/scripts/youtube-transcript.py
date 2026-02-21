#!/usr/bin/env python3
"""
Holt YouTube-Transkripte und legt sie im Memo-Cache ab.

Usage:
    python3 scripts/youtube-transcript.py URL [URL ...]
    python3 scripts/youtube-transcript.py --cache-dir ~/memos/_cache URL [URL ...]

Beispiele:
    # Einzelnes Video
    python3 scripts/youtube-transcript.py "https://www.youtube.com/watch?v=wTfejWX6DbA"

    # Mehrere Videos
    python3 scripts/youtube-transcript.py "https://youtu.be/abc" "https://youtu.be/def"

    # Ganze Playlist
    python3 scripts/youtube-transcript.py "https://www.youtube.com/playlist?list=PLu5tKfQq0iybAoqpQcrA2QDUGAGnigaCM"

    # Mit explizitem Cache-Verzeichnis
    python3 scripts/youtube-transcript.py --cache-dir ~/Dropbox/workspace/wissen/memos/_cache "URL"

Benötigt: pip3 install youtube-transcript-api
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone

# Plugin-Root automatisch relativ zum Script-Standort finden
PLUGIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(PLUGIN_DIR, "_cache", "transcripts")
INDEX_FILE = os.path.join(PLUGIN_DIR, "_cache", "youtube-index.json")

# Sprach-Präferenzen: zuerst manuell, dann auto-generiert
LANGUAGE_PREFS = ["de", "en", "fr", "it"]


def check_dependencies():
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        return True
    except ImportError:
        print("❌ youtube-transcript-api nicht installiert.")
        print("   Bitte ausführen: pip3 install youtube-transcript-api")
        return False


def extract_video_id(url):
    """Extrahiert die Video-ID aus verschiedenen YouTube-URL-Formaten."""
    patterns = [
        r"(?:v=|/v/)([a-zA-Z0-9_-]{11})",       # youtube.com/watch?v=ID
        r"(?:youtu\.be/)([a-zA-Z0-9_-]{11})",     # youtu.be/ID
        r"(?:embed/)([a-zA-Z0-9_-]{11})",          # youtube.com/embed/ID
        r"(?:shorts/)([a-zA-Z0-9_-]{11})",         # youtube.com/shorts/ID
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    # Vielleicht ist es schon eine nackte ID
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url):
        return url

    return None


def is_playlist_url(url):
    """Prüft ob die URL eine Playlist ist."""
    return "list=" in url and ("playlist?" in url or "watch?" in url)


def extract_playlist_id(url):
    """Extrahiert die Playlist-ID aus einer YouTube-URL."""
    match = re.search(r"list=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None


def fetch_playlist_video_ids(playlist_id):
    """
    Holt alle Video-IDs einer Playlist.
    Nutzt die YouTube-Seite direkt und parst die Video-IDs aus dem HTML.
    Kein API-Key nötig.
    """
    print(f"📋 Lade Playlist {playlist_id}...")
    url = f"https://www.youtube.com/playlist?list={playlist_id}"

    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8")
    except Exception as e:
        print(f"❌ Playlist konnte nicht geladen werden: {e}")
        return []

    # Video-IDs aus dem HTML extrahieren (sie erscheinen in "videoId":"..." Mustern)
    video_ids = []
    seen = set()
    for match in re.finditer(r'"videoId"\s*:\s*"([a-zA-Z0-9_-]{11})"', html):
        vid = match.group(1)
        if vid not in seen:
            seen.add(vid)
            video_ids.append(vid)

    print(f"   Gefunden: {len(video_ids)} Videos in der Playlist")
    return video_ids


def format_timestamp(seconds):
    """Sekunden → [MM:SS] Format."""
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"[{m:02d}:{s:02d}]"


def fetch_transcript(video_id):
    """Holt das Transkript und gibt (text, language) zurück."""
    from youtube_transcript_api import YouTubeTranscriptApi

    ytt_api = YouTubeTranscriptApi()

    # Versuch 1: Bevorzugte Sprachen
    for lang in LANGUAGE_PREFS:
        try:
            transcript = ytt_api.fetch(video_id, languages=[lang])
            return transcript, lang
        except Exception:
            continue

    # Versuch 2: Was auch immer verfügbar ist
    try:
        transcript = ytt_api.fetch(video_id)
        detected_lang = "?"
        return transcript, detected_lang
    except Exception as e:
        print(f"❌ Kein Transkript verfügbar für {video_id}: {e}")
        return None, None


def transcript_to_text(transcript):
    """Konvertiert Transkript-Segmente in lesbaren Text mit Timestamps."""
    lines = []
    current_line_words = []
    current_line_start = 0
    last_end = 0

    for segment in transcript:
        text = segment.text.strip()
        start = segment.start
        duration = segment.duration

        if not text:
            continue

        # Neuer Absatz bei Pause > 2 Sekunden
        if current_line_words and (start - last_end) > 2.0:
            timestamp = format_timestamp(current_line_start)
            lines.append(f"{timestamp} {' '.join(current_line_words)}")
            current_line_words = []

        if not current_line_words:
            current_line_start = start

        current_line_words.append(text)
        last_end = start + duration

        # Absatz nach ~200 Zeichen
        if len(" ".join(current_line_words)) > 200:
            timestamp = format_timestamp(current_line_start)
            lines.append(f"{timestamp} {' '.join(current_line_words)}")
            current_line_words = []

    # Rest
    if current_line_words:
        timestamp = format_timestamp(current_line_start)
        lines.append(f"{timestamp} {' '.join(current_line_words)}")

    return "\n\n".join(lines)


def fetch_video_metadata(video_id):
    """Versucht Basis-Metadaten via oembed zu holen (kein API-Key nötig)."""
    try:
        url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "title": data.get("title", "?"),
                "author": data.get("author_name", "?"),
            }
    except Exception:
        return {"title": "?", "author": "?"}


def load_index():
    """Lädt den bestehenden YouTube-Index."""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_index(index):
    """Speichert den YouTube-Index."""
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)


def collect_video_ids(args):
    """Sammelt alle Video-IDs aus den Argumenten (einzelne URLs + Playlists)."""
    video_ids = []

    for url in args:
        playlist_id = extract_playlist_id(url)

        # Wenn es eine reine Playlist-URL ist (kein einzelnes Video)
        if playlist_id and "playlist?" in url:
            ids = fetch_playlist_video_ids(playlist_id)
            video_ids.extend(ids)
        # Wenn es eine Video-URL mit Playlist ist (z.B. watch?v=X&list=Y)
        elif playlist_id and "watch?" in url:
            # Einzelnes Video extrahieren
            vid = extract_video_id(url)
            if vid:
                video_ids.append(vid)
        else:
            # Normales einzelnes Video
            vid = extract_video_id(url)
            if vid:
                video_ids.append(vid)
            else:
                print(f"⚠️  Konnte keine Video-ID extrahieren aus: {url}")

    return video_ids


def main():
    global CACHE_DIR, INDEX_FILE

    parser = argparse.ArgumentParser(description="YouTube-Transkript → Cache")
    parser.add_argument("--cache-dir", type=str, default=None,
                        help="Cache-Verzeichnis (default: {PLUGIN_DIR}/_cache)")
    parser.add_argument("urls", nargs="*", help="YouTube URLs oder Video-IDs")
    args = parser.parse_args()

    if not args.urls:
        parser.print_help()
        sys.exit(1)

    if args.cache_dir:
        cache_base = os.path.expanduser(args.cache_dir)
        CACHE_DIR = os.path.join(cache_base, "transcripts")
        INDEX_FILE = os.path.join(cache_base, "youtube-index.json")

    if not check_dependencies():
        sys.exit(1)

    os.makedirs(CACHE_DIR, exist_ok=True)
    index = load_index()
    existing_ids = {entry["video_id"] for entry in index}

    # Video-IDs sammeln (einzelne + Playlists)
    video_ids = collect_video_ids(args.urls)

    if not video_ids:
        print("❌ Keine Videos gefunden.")
        sys.exit(1)

    print(f"\n🎬 {len(video_ids)} Videos zu verarbeiten\n")

    success = 0
    skipped = 0
    failed = 0

    for i, video_id in enumerate(video_ids, 1):
        cache_file = os.path.join(CACHE_DIR, f"yt_{video_id}.txt")

        if os.path.exists(cache_file):
            print(f"⏭️  [{i}/{len(video_ids)}] Bereits gecacht: {video_id}")
            skipped += 1
            continue

        print(f"🔍 [{i}/{len(video_ids)}] Lade Transkript für {video_id}...")
        transcript, lang = fetch_transcript(video_id)

        if transcript is None:
            failed += 1
            continue

        # Zu Text konvertieren
        text = transcript_to_text(transcript)

        # Speichern
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"   ✅ Transkript gespeichert ({lang}): yt_{video_id}.txt")

        # Metadaten holen
        meta = fetch_video_metadata(video_id)
        print(f"   📋 {meta['author']}: {meta['title']}")

        # Index updaten
        if video_id not in existing_ids:
            index.append({
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "title": meta["title"],
                "author": meta["author"],
                "language": lang,
                "fetched": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            })
            existing_ids.add(video_id)

        success += 1

    # Index speichern
    save_index(index)
    print(f"\n📚 YouTube-Index: {len(index)} Videos → {INDEX_FILE}")
    print(f"   ✅ {success} neu  ⏭️ {skipped} übersprungen  ❌ {failed} fehlgeschlagen")


if __name__ == "__main__":
    main()
