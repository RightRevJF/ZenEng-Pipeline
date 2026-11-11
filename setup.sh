#!/usr/bin/env bash
# Set up the ZenEng song pipeline in a fresh workspace. Run from the repo root: bash setup.sh
set -e
REPO="$(cd "$(dirname "$0")" && pwd)"
if command -v apt-get >/dev/null; then
  (sudo -n true 2>/dev/null && SUDO=sudo) || SUDO=""
  $SUDO apt-get update -qq || true
  $SUDO apt-get install -y -qq lilypond fluidsynth fluid-soundfont-gm pandoc ffmpeg >/dev/null || echo "apt install incomplete: check lilypond, fluidsynth, fluid-soundfont-gm, pandoc, ffmpeg"
fi
pip install -q --break-system-packages numpy scipy mido pyphen spacy pronouncing wordfreq cmudict playwright || pip install -q numpy scipy mido pyphen spacy pronouncing wordfreq cmudict playwright
python3 -m spacy download en_core_web_sm -q || true
python3 -m spacy download en_core_web_md -q || true
python3 -m playwright install chromium >/dev/null 2>&1 || true
# the scripts expect the shared libraries at /home/claude/carol and /home/claude/pop
mkdir -p /home/claude
for d in carol pop; do
  if [ -e "/home/claude/$d" ] && [ ! -L "/home/claude/$d" ]; then echo "/home/claude/$d exists and is not a link: left alone"; else ln -sfn "$REPO/lib/$d" "/home/claude/$d"; fi
done
# 309: the songs' scripts read each other and their tables by absolute path (/home/claude/pNN); link every song folder there
for d in "$REPO"/songs/p*; do
  n=$(basename "$d")
  if [ -e "/home/claude/$n" ] && [ ! -L "/home/claude/$n" ]; then :; else ln -sfn "$d" "/home/claude/$n"; fi
done
echo "checks:"; lilypond --version | head -1; fluidsynth --version 2>&1 | head -1; pandoc --version | head -1
ls /usr/share/sounds/sf2/FluidR3_GM.sf2 >/dev/null && echo "soundfont ok"
python3 -c "import sys; sys.path[:0]=['/home/claude/carol','/home/claude/pop']; import lily, measures, lyricsearch, popsearch; print('libraries ok')"
