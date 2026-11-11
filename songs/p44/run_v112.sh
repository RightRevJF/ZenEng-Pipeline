#!/bin/bash
# v112: songs 40 and 42 again, 1000 main + 1000 control, each twice (seeds 20261511 and 20261552 (v112)), one run at a time
cd "$(dirname "$0")"
for song in p40 p42; do
  for m in main ctl; do
    for t in "" _r; do
      out=run${song#p}_${m}${t}.txt
      [ -s "$out" ] && grep -q "^rerun" "$out" && continue
      PYTHONHASHSEED=0 timeout 590 python3 melody_v112_${song}.py 1000 $m $t > $out 2>&1
    done
  done
done
touch v112.done
