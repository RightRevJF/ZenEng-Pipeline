#!/bin/bash
cd /home/claude/p42
for m in main ctl; do PYTHONHASHSEED=0 timeout 590 python3 melody_v110_p40.py 1000 $m > port_$m.txt 2>&1; done
for m in main ctl; do PYTHONHASHSEED=0 timeout 590 python3 melody_v110_p40.py 1000 $m _r > port_${m}_r.txt 2>&1; done
touch port.done
