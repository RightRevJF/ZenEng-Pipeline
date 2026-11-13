#!/bin/bash
# Part 1 reproduces from the final files: song 43, main, ZE_PART=1 (order of record 911539fed64d)
cd /home/claude/p54; mkdir -p check
ZE_PART=1 PYTHONHASHSEED=0 timeout 6000 python3 melody_v128_p43.py 1000 main _p1check > check/run43_main_p1check.txt 2>&1; mv -f melody_v128_p43_main_p1check.pkl check/
