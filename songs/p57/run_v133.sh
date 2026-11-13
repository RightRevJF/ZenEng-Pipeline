#!/bin/bash
# v133 regression of song 47: main and control, once each, in parallel
cd /home/claude/p57
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_v133_p57.py 1000 $m > run133/run57_$m.txt 2>&1 & done
wait; touch run133/done
