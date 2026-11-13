#!/bin/bash
# readings of the v129 port (part1/): tests per song against Run 3's runs of record (songs 40, 42, 43: Part 2; 44, 45: Part 1), separation on both draws
cd /home/claude/p55; K=1
rd() { s=$1; [ -s part$K/readings_v129_p${s}_table.json ] && return 0; case $s in 40|42|43) PREV=/home/claude/p54/part2/melody_v128;; *) PREV=/home/claude/p54/part1/melody_v128;; esac
  ZE_PART=$K timeout 3000 python3 readings_v129.py melody_v129_p$s /home/claude/p55/part$K/melody_v129_p$s part$K/readings_v129_p$s ${PREV}_p$s /home/claude/p50/melody_v118_p$s > part$K/rd$s.txt 2>&1; }
export -f rd; export K
printf "40\n42\n43\n44\n45\n" | xargs -P 2 -I{} bash -c 'rd {}'
ARGS=""; for s in 40 42 43 44 45; do ARGS="$ARGS $s=/home/claude/p55/part$K/melody_v129_p$s"; done
[ -s part$K/sep.json ] || timeout 3000 python3 sep_v129.py part$K/sep.json $ARGS > part$K/sep.txt 2>&1
mkdir -p ctlsep; CARGS=""; for s in 40 42 43 44 45; do ln -sf /home/claude/p55/part$K/melody_v129_p${s}_ctl.pkl ctlsep/m_p${s}_main.pkl; CARGS="$CARGS $s=/home/claude/p55/ctlsep/m_p$s"; done
[ -s part$K/sep_ctl.json ] || timeout 3000 python3 sep_v129.py part$K/sep_ctl.json $CARGS > part$K/sep_ctl.txt 2>&1
# Run 3's five songs as a single prefix set (40, 42, 43 from Part 2; 44, 45 from Part 1), for the reread
mkdir -p run3; for s in 40 42 43; do for m in main ctl; do ln -sf /home/claude/p54/part2/melody_v128_p${s}_$m.pkl run3/melody_v128_p${s}_$m.pkl; done; done
for s in 44 45; do for m in main ctl; do ln -sf /home/claude/p54/part1/melody_v128_p${s}_$m.pkl run3/melody_v128_p${s}_$m.pkl; done; done
for m in main ctl; do RR_MODE=$m timeout 3000 python3 reread_v129.py reread_v129_$m.json run3=/home/claude/p55/run3/melody_v128 v129=/home/claude/p55/part1/melody_v129 > reread_$m.txt 2>&1 & done; wait
touch part$K/read.done
