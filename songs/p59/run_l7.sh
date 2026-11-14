#!/bin/bash
# Luthier v7: main and control, once each, same seed and designs
cd /home/claude/p59
for m in main ctl; do PYTHONHASHSEED=0 timeout 7000 python3 melody_l7_p59.py 1000 $m > runl7/run_$m.txt 2>&1 & done; wait
