#!/bin/bash
# v132 regression of song 47: main and control, once each, in parallel
cd /home/claude/p57
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_v132_p57.py 1000 $m > run132/run57_$m.txt 2>&1 & done
wait; touch run132/done
