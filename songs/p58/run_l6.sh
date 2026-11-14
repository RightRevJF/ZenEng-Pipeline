#!/bin/bash
# song 48 on Luthier v6 (711-715, 717 on v4): main and control, once each, same seed and designs
cd /home/claude/p58
for m in main ctl; do PYTHONHASHSEED=0 timeout 6000 python3 melody_l6_p58.py 1000 $m > runl6/run58_$m.txt 2>&1 & done; wait
