#!/bin/bash
# memo-erstellen Plugin — ZIP fuer Cowork bauen
# Usage: ./build.sh

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$PLUGIN_DIR/_dist"
ZIP_NAME="memo-erstellen.zip"

mkdir -p "$DIST_DIR"

cd "$PLUGIN_DIR"
zip -r "$DIST_DIR/$ZIP_NAME" \
  .claude-plugin/ \
  commands/ \
  skills/_shared/ \
  scripts/ \
  config-template.json \
  README.md \
  -x '*.DS_Store' \
  -x 'skills/_shared/leserprofil.md'

echo ""
echo "✓ ZIP gebaut: $DIST_DIR/$ZIP_NAME"
echo "  $(du -h "$DIST_DIR/$ZIP_NAME" | cut -f1) — $(unzip -l "$DIST_DIR/$ZIP_NAME" | tail -1)"
