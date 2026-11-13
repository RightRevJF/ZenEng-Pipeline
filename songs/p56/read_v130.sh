#!/bin/bash
# Song 46 read beside songs 40, 42 and 43 (their v129 runs of record), on both draws: separation on the agreed 30 (sep_v129.py) and
# Window 147's measures with the engine's window (reread_v130.py).
cd /home/claude/p56
A=""; for s in 46 40 42 43; do A="$A $s=/home/claude/p56/rr/m_p$s"; done
[ -s read/sep.json ] || nice -n 10 timeout 5000 python3 /home/claude/p55/sep_v129.py read/sep.json $A > read/sep.txt 2>&1
C=""; for s in 46 40 42 43; do C="$C $s=/home/claude/p56/ctlsep/m_p$s"; done
[ -s read/sep_ctl.json ] || nice -n 10 timeout 5000 python3 /home/claude/p55/sep_v129.py read/sep_ctl.json $C > read/sep_ctl.txt 2>&1
for m in main ctl; do RR_MODE=$m RR_SONGS=40,42,43,46 nice -n 10 timeout 5000 python3 reread_v130.py read/reread_v130_$m.json v130=/home/claude/p56/rr/m > read/reread_$m.txt 2>&1; done
touch read/read.done
