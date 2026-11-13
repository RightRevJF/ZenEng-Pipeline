#!/bin/bash
# 531's check: song 46 with 501 off (ZE_OFF=501), main and control, against the runs of record. One at a time.
cd /home/claude/p56
for m in main ctl; do out=side/run56_${m}_off501.txt
  [ -s "$out" ] && grep -q "^rerun" "$out" && continue
  ZE_OFF=501 PYTHONHASHSEED=0 timeout 6000 python3 melody_v130_p56.py 1000 $m _off501 > $out 2>&1
  mv -f melody_v130_p56_${m}_off501.pkl side/; done
touch side/done
