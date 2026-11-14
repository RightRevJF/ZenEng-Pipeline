#!/bin/bash
# song 48 on Luthier v3: run A (rhythm: 652-656) then run B (and pitch: 650, 651); main and control, same seed and designs
cd /home/claude/p58
P=${1:-1}
for m in main ctl; do ZE_PART_L3=$P PYTHONHASHSEED=0 timeout 5000 python3 melody_l3_p58.py 1000 $m > runl3/run58_p${P}_$m.txt 2>&1 & done; wait
