# ZenEng v109: the port (fixes 298–309), tested on song 40, before song 41

    python3 limits_v109.py                                   # 300/301: realness out; the six of 286 read jointly (94.2%, no refit)
    for m in main ctl; do PYTHONHASHSEED=0 python3 melody_v109_p40.py 1000 $m; PYTHONHASHSEED=0 python3 melody_v109_p40.py 1000 $m _r; done
                                                             # main 476 survivors, order 6ad97e7695d1; control 398, order 4974bb2f8af1
    python3 readings_v109_p40.py                             # the tests of 298-309 -> port_report_v109.md (findings 310-313)
    python3 trace_opens.py melody_v109_p40.py 20 main _trace # 309: every file a run reads (all committed; setup.sh links songs/pNN)
