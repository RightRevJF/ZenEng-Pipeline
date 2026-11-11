# ZenEng v112: songs 40 and 42 once more (fixes 330-336 ported; findings from 337)

No new song, as v112 asked. The same lyrics, intakes, designs and seeds.

    python3 gen_v112_p40.py            # writes melody_v112_p40.py from songs/p43/melody_v111_p40.py (fixes 330-333)
    python3 gen_p42_v112.py            # writes melody_v112_p42.py on it (song 42's constants and 325's design condition, as in songs/p43)
    bash run_v112.sh                   # each song 1000 main + 1000 control, each twice, one at a time
                                       # song 40 (seed 20261511): main 544, order 3f8eb6067d67; control 544, order 26f80e5f1a5f
                                       # song 42 (seed 20261552): main 747, order daa4d9492f81; control 738, order 7e63192665fb
    python3 readings_v112.py melody_v112_p40 /home/claude/p44/melody_v112_p40 readings_v112_p40 /home/claude/p43/melody_v111_p40
    python3 readings_v112.py melody_v112_p42 /home/claude/p44/melody_v112_p42 readings_v112_p42 /home/claude/p43/melody_v111_p42
                                       # 321/335/336: the tables of tests of 310-336, each named against its kept figure
    python3 make_report_v112.py        # test_report_v112.md; fixlist_v112.md: findings 337-338
    diag40_off329.txt, diag40_off322.txt   # diagnostics for 337 (ZE_OFF=329 / 322; never runs of record)
    reads_v112_p40.txt, reads_v112_p42.txt # 309: every file each search reads (all committed)
