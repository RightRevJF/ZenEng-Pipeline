#!/usr/bin/env bash
# The corpora the other-metres studies read, fetched outside the repository (a fresh workspace has none of them). bash studies/other_metres/fetch.sh
set -e
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; mkdir -p /home/claude/corpus "$REPO/corpora"
pip install -q --break-system-packages numpy scipy pandas lxml music21 pronouncing cmudict statsmodels 2>&1 | tail -1
[ -d "$REPO/corpora/CoCoPops" ] || git clone -q --depth 1 https://github.com/Computational-Cognitive-Musicology-Lab/CoCoPops "$REPO/corpora/CoCoPops"
[ -f "$REPO/corpora/cocopops_notes.csv.gz" ] || python3 "$REPO/lib/luthier/cocopops_parse.py" "$REPO/corpora/CoCoPops/Billboard/Data" | tail -1
[ -d /home/claude/corpus/OpenEWLD ] || git clone -q --depth 1 https://github.com/00sapo/OpenEWLD /home/claude/corpus/OpenEWLD
if [ ! -d /home/claude/corpus/choco/partitions/wikifonia/raw ]; then git clone -q --depth 1 --filter=blob:none --sparse https://github.com/smashub/choco /home/claude/corpus/choco; (cd /home/claude/corpus/choco && git sparse-checkout set partitions/wikifonia); fi
echo "CoCoPops $(ls "$REPO/corpora/CoCoPops/Billboard/Data" | wc -l) files; OpenEWLD $(find /home/claude/corpus/OpenEWLD -name '*.mxl' | wc -l) mxl; Wikifonia $(ls /home/claude/corpus/choco/partitions/wikifonia/raw | wc -l) mxl"
