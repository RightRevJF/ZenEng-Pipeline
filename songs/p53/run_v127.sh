#!/bin/bash
# v127 Run 2, one part: songs 40, 42, 43, 44 and 45, 1000 main + 1000 control, each made twice, same seeds, ZE_PART=$1; two runs at a time.
# The runs of the part are moved to part$1/ when done.
cd "$(dirname "$0")"; PART=$1; mkdir -p part$PART
run1() { song=$1; m=$2; t=$3; [ "$t" = "-" ] && t=""; out=part$PART/run${song}_${m}${t}.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && return 0
  ZE_PART=$PART PYTHONHASHSEED=0 timeout 6000 python3 melody_v127_p${song}.py 1000 $m $t > $out 2>&1
  mv -f melody_v127_p${song}_${m}${t}.pkl part$PART/; }
export -f run1; export PART
for song in 45 40 42 43 44; do for m in main ctl; do for t in - _r; do echo "$song $m $t"; done; done; done | xargs -P 2 -L 1 bash -c 'run1 "$0" "$1" "$2"'
touch part$PART/done
