#!/bin/bash
# v124 Run 1, side runs added after the first counts (none a run of record): song 45 main with 392 off (its range, from the step-3 diagnostics),
# and with 414 off and with 413 off (to name the source of song 45's new align and join deaths). Waits for run_v124.sh.
cd "$(dirname "$0")"
while [ ! -f v124.done ]; do sleep 30; done
run1() { song=$1; m=$2; t=$3; off=$4; out=run${song}_${m}${t}.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && return 0
  ZE_OFF=$off PYTHONHASHSEED=0 timeout 5000 python3 melody_v124_p${song}.py 1000 $m $t > $out 2>&1; }
export -f run1
{ echo "45 main _off392 392"; echo "45 main _off414 414"; echo "45 main _off413 413"; } | xargs -P 2 -L 1 bash -c 'run1 "$0" "$1" "$2" "$3"'
touch v124b.done
