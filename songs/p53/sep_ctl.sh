#!/bin/bash
cd /home/claude/p53
one() { k=$1; P=/home/claude/p53/ctlsep/$k/m; timeout 3000 python3 sep_v127.py ctlsep/sep_$k.json 40=${P}_p40 42=${P}_p42 43=${P}_p43 44=${P}_p44 45=${P}_p45 > ctlsep/sep_$k.txt 2>&1; }
export -f one; printf "run1\npart1\npart2\npart3\n" | xargs -P 2 -I{} bash -c 'one {}'; touch ctlsep/done
