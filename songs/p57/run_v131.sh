#!/bin/bash
# v131, song 47 (The Singer Doesn't Stop): 1000 main + 1000 control, each made twice, same seeds; two runs at a time. Runs go to run/.
cd "$(dirname "$0")"; mkdir -p run
run1() { m=$1; t=$2; [ "$t" = "-" ] && t=""; out=run/run57_${m}${t}.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && return 0
  PYTHONHASHSEED=0 timeout 6000 python3 melody_v131_p57.py 1000 $m $t > $out 2>&1
  mv -f melody_v131_p57_${m}${t}.pkl run/; }
export -f run1
for m in main ctl; do for t in - _r; do echo "$m $t"; done; done | xargs -P 2 -L 1 bash -c 'run1 "$0" "$1"'
touch run/done
