#!/bin/bash
# v118: songs 40, 42, 43, 44 and 45 again, each 1000 main + 1000 control, made twice (seeds 20261511, 20261552, 20261553, 20261554, 20261555),
# one run at a time; then 368's two diagnostic runs on song 43 (main, 1000): fix 358 off, and fix 361 off
cd "$(dirname "$0")"
for song in p40 p42 p43 p44 p45; do
  for m in main ctl; do
    for t in "" _r; do
      out=run${song#p}_${m}${t}.txt
      [ -s "$out" ] && grep -q "^rerun" "$out" && continue
      PYTHONHASHSEED=0 timeout 2400 python3 melody_v118_${song}.py 1000 $m $t > $out 2>&1
    done
  done
done
for o in 358 361; do
  out=run43_main_off$o.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && continue
  ZE_OFF=$o PYTHONHASHSEED=0 timeout 2400 python3 melody_v118_p43.py 1000 main _off$o > $out 2>&1
done
touch v118.done
