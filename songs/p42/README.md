# ZenEng v110: the port (fixes 310-321), tested on song 40, before song 42

    python3 gen_v110_p40.py                                  # writes melody_v110_p40.py from songs/p41/melody_v109_p40.py
    bash run_port.sh                                         # song 40: 1000 main + 1000 control, each twice (seed 20261511)
                                                             # main 505 survivors, order 3c9c4f2da558; control 537, order 30ba2486b5e4
    python3 readings_v110.py melody_v110_p40 /home/claude/p42/melody_v110_p40 readings_v110_p40 /home/claude/p41/melody_v109_p40
                                                             # 321: the table of tests of 310-321 -> readings_v110_p40_table.json
    reads_v110_p40.txt                                       # 309: every file the search reads (all committed)
