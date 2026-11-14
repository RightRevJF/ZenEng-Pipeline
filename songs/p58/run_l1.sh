#!/bin/bash
# song 48 on Luthier v1 (605, 606; v137 600-603): main and control, once each, same seed and designs
cd /home/claude/p58
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_l1_p58.py 1000 $m > runl1/run58_$m.txt 2>&1 & done; wait
