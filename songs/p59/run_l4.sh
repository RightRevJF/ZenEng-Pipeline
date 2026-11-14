#!/bin/bash
# song 49 on Luthier v4: main and control, once each
cd /home/claude/p59
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_l4_p59.py 1000 $m > run/run59_$m.txt 2>&1 & done; wait
