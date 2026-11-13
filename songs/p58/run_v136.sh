#!/bin/bash
# song 48 on v136 (573, 577, 578, 579): main and control, once each, same seed and designs
cd /home/claude/p58
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_v136_p58.py 1000 $m > run136/run58_$m.txt 2>&1 & done; wait
