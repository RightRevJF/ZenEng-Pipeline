#!/bin/bash
# song 45, main, the port with 501 off (where its joins before a line come from)
cd /home/claude/p55; mkdir -p side; out=side/run45_main_off501.txt
[ -s "$out" ] && grep -q "^rerun" "$out" || { ZE_PART=1 ZE_OFF=501 PYTHONHASHSEED=0 timeout 6000 python3 melody_v129_p45.py 1000 main _off501 > $out 2>&1; mv -f melody_v129_p45_main_off501.pkl side/; }
touch side/done
