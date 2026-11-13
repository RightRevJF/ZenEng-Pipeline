#!/bin/bash
# the rest of the regression (songs 42-46), two at a time; song 40 ctl finishes from the first script's run.
reg1() { s=$1; m=$2; out=/home/claude/p57/regress/run${s}_${m}.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && return 0
  if [ "$s" = "46" ]; then cd /home/claude/p56 && PYTHONHASHSEED=0 timeout 6000 python3 melody_v130_p56.py 1000 $m _reg > $out 2>&1; rm -f melody_v130_p56_${m}_reg.pkl
  else cd /home/claude/p55 && ZE_PART=1 PYTHONHASHSEED=0 timeout 6000 python3 melody_v129_p${s}.py 1000 $m _reg > $out 2>&1; rm -f melody_v129_p${s}_${m}_reg.pkl; fi; }
export -f reg1
for s in 46 45 44 43 42; do for m in main ctl; do echo "$s $m"; done; done | xargs -P 2 -L 1 bash -c 'reg1 "$0" "$1"'
touch /home/claude/p57/regress/done2
