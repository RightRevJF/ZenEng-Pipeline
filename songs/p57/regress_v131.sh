#!/bin/bash
# 523: songs 40-46 closed; rerun once as a regression against their orders of record (40-45: v129, songs/p55 part1; 46: v130, songs/p56 run). One at a time.
reg1() { s=$1; m=$2; out=/home/claude/p57/regress/run${s}_${m}.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && return 0
  if [ "$s" = "46" ]; then cd /home/claude/p56 && PYTHONHASHSEED=0 timeout 6000 python3 melody_v130_p56.py 1000 $m _reg > $out 2>&1; rm -f melody_v130_p56_${m}_reg.pkl
  else cd /home/claude/p55 && ZE_PART=1 PYTHONHASHSEED=0 timeout 6000 python3 melody_v129_p${s}.py 1000 $m _reg > $out 2>&1; rm -f melody_v129_p${s}_${m}_reg.pkl; fi; }
for s in 40 42 43 44 45 46; do for m in main ctl; do reg1 $s $m; done; done
touch /home/claude/p57/regress/done
