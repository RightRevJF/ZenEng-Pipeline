#!/bin/bash
cd /home/claude/atlas
for job in "6/8 instrumental 800" "9/8 instrumental" "2/4 instrumental 800" "3/4 instrumental 600" "4/4 instrumental 800" "2/2 instrumental 800" "3/8 instrumental"; do echo $job; done | xargs -P 2 -L 1 bash -c 'timeout 3000 python3 atlas_build.py $0 $1 $2 >> run_inst.log 2>&1'
echo DONE >> run_inst.log
