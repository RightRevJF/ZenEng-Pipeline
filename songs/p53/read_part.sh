#!/bin/bash
# readings of one part: tests per song, separation (with and without each family), and the reread of every run so far
cd /home/claude/p53; K=$1; PREV=$2   # PREV: prefix of the run before (e.g. /home/claude/p52/melody_v124 or /home/claude/p53/part1/melody_v127)
rd() { s=$1; [ -s part$K/readings_v127_p${s}_table.json ] && return 0; timeout 3000 python3 readings_v127.py melody_v127_p$s /home/claude/p53/part$K/melody_v127_p$s part$K/readings_v127_p$s ${PREV}_p$s /home/claude/p50/melody_v118_p$s > part$K/rd$s.txt 2>&1; }
export -f rd; export K PREV
printf "40\n42\n43\n44\n45\n" | xargs -P 2 -I{} bash -c 'rd {}'
[ -s part$K/sep.json ] || timeout 3000 python3 sep_v127.py part$K/sep.json 40=/home/claude/p53/part$K/melody_v127_p40 42=/home/claude/p53/part$K/melody_v127_p42 43=/home/claude/p53/part$K/melody_v127_p43 44=/home/claude/p53/part$K/melody_v127_p44 45=/home/claude/p53/part$K/melody_v127_p45 > part$K/sep.txt 2>&1
ARGS="run1=/home/claude/p52/melody_v124"; for k in 1 2 3; do [ -f part$k/done ] && [ $k -le $K ] && ARGS="$ARGS part$k=/home/claude/p53/part$k/melody_v127"; done
timeout 3000 python3 reread_v127.py reread_v127.json $ARGS > reread.txt 2>&1
touch part$K/read.done
