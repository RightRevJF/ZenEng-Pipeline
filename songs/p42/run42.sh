#!/bin/bash
# Song 42: 1000 main + 1000 control, each twice (seed 20261552)
cd "$(dirname "$0")"
for m in main ctl; do
  PYTHONHASHSEED=0 timeout 590 python3 melody_p42.py 1000 $m    > run42_$m.txt
  PYTHONHASHSEED=0 timeout 590 python3 melody_p42.py 1000 $m _r > run42_${m}_r.txt
done
