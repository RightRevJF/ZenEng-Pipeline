# v115: songs 40, 42 and 43 again (fixes 348–354 ported; findings from 355)

Words and music of all three songs: Jason Bryant. Same lyrics, intakes and seeds as their last runs (songs/p44 for 40 and 42, songs/p45 for 43). No new song.
The writer's choice on the port (Q1 A: 348's "unless there is no room" also covers drawn lines) is in log_v115.py.

    python3 gen_v115_p40.py            # melody_v115_p40.py: v115's 348-354 on songs/p45/melody_v114_p40.py
    python3 gen_p42_v115.py            # melody_v115_p42.py: song 42's constants on it (seed 20261552)
    python3 gen_p43_v115.py            # melody_v115_p43.py: song 43's constants on it, read on A (353; seed 20261553)
    bash run_v115.sh                   # each song 1000 main + 1000 control, each twice; all six orders reproduced
                                       # 40: 602 / 663, 2a9550248f1b / c5344a86edce
                                       # 42: 767 / 782, 03a4f13efa50 / 1c46ba2167ca
                                       # 43: 722 / 803, 97c7c92a9619 / 4f2f64f2a00e
    python3 readings_v115.py melody_v115_p40 /home/claude/p46/melody_v115_p40 readings_v115_p40 /home/claude/p44/melody_v112_p40
    python3 readings_v115.py melody_v115_p42 /home/claude/p46/melody_v115_p42 readings_v115_p42 /home/claude/p44/melody_v112_p42
    python3 readings_v115.py melody_v115_p43 /home/claude/p46/melody_v115_p43 readings_v115_p43 /home/claude/p45/melody_p43
    python3 make_report_v115.py        # test_report_v115.md (findings 355-363 appended); fixlist_v115.md
    reads_v115.txt                     # 309: every file the three searches read (all committed)
