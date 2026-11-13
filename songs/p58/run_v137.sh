#!/bin/bash
# song 48 on v137 (600, 601, 602, 603): main and control, once each, same seed and designs
cd /home/claude/p58
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_v137_p58.py 1000 $m > run137/run58_$m.txt 2>&1 & done; wait
