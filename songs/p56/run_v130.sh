#!/bin/bash
# v130, song 46 (Dry Ground): 1000 main + 1000 control, each made twice, same seeds; two runs at a time. Runs go to run/.
cd "$(dirname "$0")"; mkdir -p run
run1() { m=$1; t=$2; [ "$t" = "-" ] && t=""; out=run/run56_${m}${t}.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && return 0
  PYTHONHASHSEED=0 timeout 6000 python3 melody_v130_p56.py 1000 $m $t > $out 2>&1
  mv -f melody_v130_p56_${m}${t}.pkl run/; }
export -f run1
for m in main ctl; do for t in - _r; do echo "$m $t"; done; done | xargs -P 2 -L 1 bash -c 'run1 "$0" "$1"'
touch run/done
