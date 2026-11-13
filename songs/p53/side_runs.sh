#!/bin/bash
# song 45, main, Part 2's code, with 406 off and with 457 off (side runs, none a run of record)
cd /home/claude/p53
for o in 406 457; do [ -s side/run45_main_p2off$o.txt ] && grep -q "^rerun" side/run45_main_p2off$o.txt && continue
  (ZE_PART=2 ZE_OFF=$o PYTHONHASHSEED=0 timeout 6000 python3 melody_v127_p45.py 1000 main _p2off$o > side/run45_main_p2off$o.txt 2>&1; mv -f melody_v127_p45_main_p2off$o.pkl side/) & done; wait
touch side/done
