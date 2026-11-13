#!/bin/bash
# 494: song 45's joins, main, Part 1's code, with 452 off and with 455 off (side runs only)
cd /home/claude/p54; mkdir -p side
one() { o=$1; out=side/run45_main_p1off$o.txt; [ -s "$out" ] && grep -q "^rerun" "$out" && return 0
  ZE_PART=1 ZE_OFF=$o PYTHONHASHSEED=0 timeout 6000 python3 melody_v128_p45.py 1000 main _p1off$o > $out 2>&1; mv -f melody_v128_p45_main_p1off$o.pkl side/; }
export -f one; printf "452\n455\n" | xargs -P 2 -I{} bash -c 'one {}'
touch side/done
