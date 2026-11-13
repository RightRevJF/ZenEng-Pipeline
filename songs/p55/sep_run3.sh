#!/bin/bash
cd /home/claude/p55
A=""; C=""; for s in 40 42 43 44 45; do A="$A $s=/home/claude/p55/run3/melody_v128_p$s"; C="$C $s=/home/claude/p55/run3ctl/m_p$s"; done
python3 sep_v129.py run3_sep.json $A > run3_sep.txt 2>&1 & python3 sep_v129.py run3_sep_ctl.json $C > run3_sep_ctl.txt 2>&1; wait
