#!/bin/bash
# song 48 on Luthier v2 (630, 631, 633, 634): main and control, once each, same seed and designs
cd /home/claude/p58
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_l2_p58.py 1000 $m > runl2/run58_$m.txt 2>&1 & done; wait
