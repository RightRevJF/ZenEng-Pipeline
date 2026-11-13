#!/bin/bash
# 523: songs 40-45 closed; rerun only as a regression, which they must reproduce: each song's v129 file (songs/p55), ZE_PART=1, main and control,
# against the orders of record (v129, part1/). Two at a time.
cd /home/claude/p55
reg1() { s=$1; m=$2; out=/home/claude/p56/regress/run${s}_${m}.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && return 0
  ZE_PART=1 PYTHONHASHSEED=0 timeout 6000 python3 melody_v129_p${s}.py 1000 $m _reg > $out 2>&1
  mv -f melody_v129_p${s}_${m}_reg.pkl /home/claude/p56/regress/; }
export -f reg1
for s in 40 42 43 44 45; do for m in main ctl; do echo "$s $m"; done; done | xargs -P 2 -L 1 bash -c 'reg1 "$0" "$1"'
touch /home/claude/p56/regress/done
