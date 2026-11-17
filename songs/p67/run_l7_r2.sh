#!/bin/bash
# song 57: the reproduction pass (the frozen orders must reproduce)
cd /home/claude/p67
for m in main ctl; do PYTHONHASHSEED=0 timeout 3000 python3 melody_l7_p67.py 1000 $m r2 > runl7/run67_${m}_r2.txt 2>&1 & done; wait
echo done > runl7/DONE2
