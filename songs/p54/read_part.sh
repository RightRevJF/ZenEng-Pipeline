#!/bin/bash
# readings of one part: tests per song, separation (main and control), and the reread of every run so far
cd /home/claude/p54; K=$1; PREV=$2; SONGS=${3:-"40 42 43 44 45"}   # PREV: prefix of the run before (e.g. /home/claude/p53/part3/melody_v127)
rd() { s=$1; [ -s part$K/readings_v128_p${s}_table.json ] && return 0; timeout 3000 python3 readings_v128.py melody_v128_p$s /home/claude/p54/part$K/melody_v128_p$s part$K/readings_v128_p$s ${PREV}_p$s /home/claude/p50/melody_v118_p$s > part$K/rd$s.txt 2>&1; }
export -f rd; export K PREV
printf "%s\n" $SONGS | xargs -P 2 -I{} bash -c 'rd {}'
ARGS=""; for s in 40 42 43 44 45; do [ -f part$K/melody_v128_p${s}_main.pkl ] && ARGS="$ARGS $s=/home/claude/p54/part$K/melody_v128_p$s"; done
[ -s part$K/sep.json ] || timeout 3000 python3 sep_v128.py part$K/sep.json $ARGS > part$K/sep.txt 2>&1
# the control runs, read the same way (sep_v128.py reads _main.pkl: the control pkls linked under ctlsep/part$K)
mkdir -p ctlsep/part$K; CARGS=""; for s in 40 42 43 44 45; do [ -f part$K/melody_v128_p${s}_ctl.pkl ] && ln -sf /home/claude/p54/part$K/melody_v128_p${s}_ctl.pkl ctlsep/part$K/m_p${s}_main.pkl && CARGS="$CARGS $s=/home/claude/p54/ctlsep/part$K/m_p$s"; done
[ -s part$K/sep_ctl.json ] || timeout 3000 python3 sep_v128.py part$K/sep_ctl.json $CARGS > part$K/sep_ctl.txt 2>&1
touch part$K/read.done
