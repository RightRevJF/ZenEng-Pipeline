#!/bin/bash
# song 44: 1000 main + 1000 control, each twice (seed 20261554), one run at a time
cd "$(dirname "$0")"
for m in main ctl; do for t in "" _r; do
  out=run44_${m}${t}.txt; [ -s "$out" ] && grep -q "^rerun" "$out" && continue
  PYTHONHASHSEED=0 timeout 590 python3 melody_p44.py 1000 $m $t > $out 2>&1
done; done
touch run44.done
