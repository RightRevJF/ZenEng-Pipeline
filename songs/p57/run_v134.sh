#!/bin/bash
# v134: song 47's last run (571), main and control, once each; then the side run 569 asks for (558 off, the calibration on), main
cd /home/claude/p57
for m in main ctl; do PYTHONHASHSEED=0 timeout 5000 python3 melody_v134_p57.py 1000 $m > run134/run57_$m.txt 2>&1 & done
wait
ZE_OFF=558 PYTHONHASHSEED=0 timeout 5000 python3 melody_v134_p57.py 1000 main _off558 > run134/run57_main_off558.txt 2>&1
touch run134/done
