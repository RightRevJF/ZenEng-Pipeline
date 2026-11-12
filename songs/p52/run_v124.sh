#!/bin/bash
# v124 Run 1: songs 40, 42, 43, 44 and 45, 1000 main + 1000 control, each made twice, same seeds; then the side runs
# (416: song 43 with 386 off and with 389 off; range: each song's main with 398 off and with 400 off; 450: song 45 with 267 read before the raise).
# Two runs at a time (two cores).
cd "$(dirname "$0")"
run1() { song=$1; m=$2; t=$3; off=$4; [ "$t" = "-" ] && t=""; [ "$off" = "-" ] && off=""; out=run${song}_${m}${t}.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && return 0
  if [ "$off" = "diag450" ]; then ZE_DIAG450=1 PYTHONHASHSEED=0 timeout 5000 python3 melody_v124_p${song}.py 1000 $m $t > $out 2>&1
  else ZE_OFF=$off PYTHONHASHSEED=0 timeout 5000 python3 melody_v124_p${song}.py 1000 $m $t > $out 2>&1; fi; }
export -f run1
{ for song in 45 40 42 43 44; do for m in main ctl; do for t in - _r; do echo "$song $m $t -"; done; done; done
  echo "45 main _diag450 diag450"; echo "43 main _off386 386"; echo "43 main _off389 389"
  for song in 45 40 42 43 44; do echo "$song main _off398 398"; echo "$song main _off400 400"; done; } | xargs -P 2 -L 1 bash -c 'run1 "$0" "$1" "$2" "$3"'
touch v124.done
