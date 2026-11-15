#!/bin/bash
cd /home/claude/atlas
for job in "2/4 sung 1200" "3/4 sung 1200" "4/4 sung 1200" "6/8 sung 1200" "3/8 sung" "6/4 sung" "3/2 sung" "2/2 sung" "4/2 sung" "5/8 sung" "5/4 sung" "7/8 sung" "9/8 sung" \
           "6/8 instrumental 1000" "9/8 instrumental" "2/4 instrumental 1000" "3/4 instrumental 600" "4/4 instrumental 1000" "2/2 instrumental 1000" "12/8 instrumental" "3/8 instrumental"; do
  echo $job
done | xargs -P 4 -L 1 bash -c 'timeout 3000 python3 atlas_build.py $0 $1 $2 >> run.log 2>&1'
echo DONE >> run.log
