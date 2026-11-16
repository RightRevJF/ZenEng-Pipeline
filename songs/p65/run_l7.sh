#!/bin/bash
# song 55 on Luthier v7: main and control, each made twice (the frozen orders must reproduce)
cd /home/claude/p65
for m in main ctl; do PYTHONHASHSEED=0 timeout 7000 python3 melody_l7_p65.py 1000 $m > runl7/run65_$m.txt 2>&1 & done; wait
for m in main ctl; do PYTHONHASHSEED=0 timeout 7000 python3 melody_l7_p65.py 1000 $m r2 > runl7/run65_${m}_r2.txt 2>&1 & done; wait
echo done > runl7/DONE
