#!/bin/bash
# song 49 on Luthier v6: main and control, once each, same seed and designs
cd /home/claude/p59
for m in main ctl; do PYTHONHASHSEED=0 timeout 6000 python3 melody_l6_p59.py 1000 $m > runl6/run59_$m.txt 2>&1 & done; wait
