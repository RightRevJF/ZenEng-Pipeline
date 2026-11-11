#!/bin/bash
cd /home/claude/p41
for m in main ctl; do PYTHONHASHSEED=0 timeout 590 python3 melody_p41.py 1000 $m > run_$m.txt 2>&1; done
for m in main ctl; do PYTHONHASHSEED=0 timeout 590 python3 melody_p41.py 1000 $m _r > run_${m}_r.txt 2>&1; done
touch run41.done
