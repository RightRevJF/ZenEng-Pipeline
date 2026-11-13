#!/bin/bash
# song 48 on v134: main and control, each made twice (the second as _r), two at a time
cd /home/claude/p58
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_v134_p58.py 1000 $m > run/run58_$m.txt 2>&1 & done; wait
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_v134_p58.py 1000 $m _r > run/run58_${m}_r.txt 2>&1 & done; wait
touch run/done
