#!/bin/bash
# v116: songs 40, 42 and 43 again, each 1000 main + 1000 control, made twice (seeds 20261511, 20261552, 20261553), one run at a time;
# then 356's two diagnostic runs on song 43 (main, 1000): fix 348 off (with 355, which amends it), and fix 354 off
cd "$(dirname "$0")"
for song in p40 p42 p43; do
  for m in main ctl; do
    for t in "" _r; do
      out=run${song#p}_${m}${t}.txt
      [ -s "$out" ] && grep -q "^rerun" "$out" && continue
      PYTHONHASHSEED=0 timeout 590 python3 melody_v116_${song}.py 1000 $m $t > $out 2>&1
    done
  done
done
for o in 348 354; do
  out=run43_main_off$o.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && continue
  ZE_OFF=$o PYTHONHASHSEED=0 timeout 590 python3 melody_v116_p43.py 1000 main _off$o > $out 2>&1
done
touch v116.done
