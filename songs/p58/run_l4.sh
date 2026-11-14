#!/bin/bash
# song 48 on Luthier v4 (680-683 on v3's run B): main and control, once each, same seed and designs
cd /home/claude/p58
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_l4_p58.py 1000 $m > runl4/run58_$m.txt 2>&1 & done; wait
