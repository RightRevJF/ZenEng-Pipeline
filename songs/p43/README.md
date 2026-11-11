# ZenEng v111: songs 40 and 42 again (fixes 322-329 ported; findings from 330)

No new song: v111 asked for songs 40 and 42 again, with the same lyrics, intakes and seeds.

    python3 gen_v111_p40.py            # writes melody_v111_p40.py from songs/p42/melody_v110_p40.py (fixes 322-329)
    python3 gen_p42_v111.py            # writes melody_v111_p42.py on it: song 42's constants as songs/p42/gen_p42.py, plus 325's design condition
    bash run_v111.sh                   # each song 1000 main + 1000 control, each twice, one at a time
                                       # song 40 (seed 20261511): main 480, order 7d491acfca47; control 417, order 07a87d6f518f
                                       # song 42 (seed 20261552): main 780, order 08a4b2311f06; control 783, order cf1a424d0021
    python3 readings_v111.py melody_v111_p40 /home/claude/p43/melody_v111_p40 readings_v111_p40 /home/claude/p42/melody_v110_p40
    python3 readings_v111.py melody_v111_p42 /home/claude/p43/melody_v111_p42 readings_v111_p42 /home/claude/p42/melody_p42
                                       # 321: the table of tests of 310-329 for each song, with Table DQ beside v110
    python3 make_report_v111.py        # test_report_v111.md (findings_v111.md appended); fixlist_v111.md: findings 330-334
    reads_v111_p40.txt, reads_v111_p42.txt   # 309: every file each search reads (all committed)
Diagnostics only (never a run of record): ZE_OFF=322 or ZE_OFF=329 switches that fix off.
