#!/bin/bash
# Song 43: 1000 main + 1000 control, each twice (seed 20261553), one at a time
cd "$(dirname "$0")"
for m in main ctl; do
  for t in "" _r; do
    out=run43_${m}${t}.txt
    [ -s "$out" ] && grep -q "^rerun" "$out" && continue
    PYTHONHASHSEED=0 timeout 590 python3 melody_p43.py 1000 $m $t > $out 2>&1
  done
done
touch run43.done
