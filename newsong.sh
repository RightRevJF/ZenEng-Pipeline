#!/usr/bin/env bash
# Start song NN from the template (the latest finished song): bash newsong.sh 26
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"; N="$1"; [ -z "$N" ] && { echo "usage: bash newsong.sh NN"; exit 1; }
DST="/home/claude/p$N"; [ -e "$DST" ] && { echo "$DST already exists"; exit 1; }
TPL=$(cat "$REPO/template/TEMPLATE_SONG")
mkdir -p "$DST/out" "$DST/src"; cp "$REPO"/template/*.py "$REPO"/template/*.md "$DST/"
cd "$DST"
for f in *_p$TPL.py; do mv "$f" "${f/_p$TPL/_p$N}"; done
sed -i "s#/home/claude/p$TPL#/home/claude/p$N#g; s/_p$TPL\b/_p$N/g; s/engine_p$TPL/engine_p$N/g" *.py
echo "started $DST from song $TPL. Every song-specific part (intake LOG, lyric, FORM, designed notes, arrangement, docs text) must be rewritten for the new song."
