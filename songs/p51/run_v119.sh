#!/bin/bash
# v119 port, step 3 (all fixes ported, 399 and 401 withdrawn by v120, 424 added): songs 40, 42, 43, 44 and 45 again,
# each 1000 main + 1000 control, made twice, same seeds; two runs at a time (two cores)
cd "$(dirname "$0")"
run1() { song=$1; m=$2; t=$3; [ "$t" = "-" ] && t=""; out=run${song}_${m}${t}.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && return 0
  ZE_STEP=3 PYTHONHASHSEED=0 timeout 4000 python3 melody_v119_p${song}.py 1000 $m $t > $out 2>&1; }
export -f run1
for song in 40 42 43 44 45; do for m in main ctl; do for t in - _r; do echo "$song $m $t"; done; done; done | xargs -P 2 -L 1 bash -c 'run1 "$0" "$1" "$2"'
touch v119.done
