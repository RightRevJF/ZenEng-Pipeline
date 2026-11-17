#!/bin/bash
# song 57 on Luthier v7: main and control, 1,000 each (pass 1; the reproduction pass r2 follows)
cd /home/claude/p67
for m in main ctl; do PYTHONHASHSEED=0 timeout 10000 python3 melody_l7_p67.py 1000 $m > runl7/run67_$m.txt 2>&1 & done; wait
echo done > runl7/DONE1
