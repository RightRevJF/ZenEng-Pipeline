#!/bin/bash
# side run for 610 (not of record): main and control, same seed and designs
cd /home/claude/p58
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_v137s_p58.py 1000 $m > run137s/run58_$m.txt 2>&1 & done; wait
