#!/bin/bash
cd /home/claude/p52
for s in "$@"; do timeout 2400 python3 readings_v124.py melody_v124_p$s /home/claude/p52/melody_v124_p$s readings_v124_p$s /home/claude/p51/melody_v119_p$s /home/claude/p50/melody_v118_p$s > rd$s.txt 2>&1; done
