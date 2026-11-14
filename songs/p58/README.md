# songs/p58: song 48, The Ratios Hold (ZenEng v134, Module 27.78)

Words and music: Jason Bryant. Symphonic progressive suite in five movements, E major, ♩ = 92, high tenor (D3–C5), 174 bars, every sung line
in a two-bar slot. Written on v134 as the dense song the judge has not seen (571).

- Choices: intake.py (the full LOG). Lyric: lyric_draft1-3.md, lyric_locked.md, lyric_p58.py.
- Engine: gen_v134_p58.py writes melody_v134_p58.py from songs/p57's melody_v134_p57.py with the song's frame (E major with D as ♭7), form,
  lyric and designs (the hook, the bridge's build, the chorus above the verse). Runs: run_v134.sh (main and control, each twice; logs in run/).
- Pick: pick_p58.py. Bass: bass_v134.py. Record: build_p58.py (meters 4/4, 7/8, 5/4; the instrumentals from one theme).
- Documents: demo_p58.py, engrave_p58.py (lead sheet, parts), score_p58.py (full score), nashville_p58.py, songbook_p58.py, q1020.py. Checks: consistency_p58.py.
- Readings: judge547.py (547, read/judge547.json), read_p58.py (read/read_p58.json). Tables copied from songs/p57.
- Report: test_report_p58.md; findings_p58.md (580-588; v135 used 577).

The source pieces are not in the repo.

## v136 (Module 27.80, Window 156): the regression run

gen_v136_p58.py writes melody_v136_p58.py from melody_v134_p58.py with 573 and 577 (v135) and 578 and 579 (v136); tables/zeneng_v136_slot_rate.json.
run_v136.sh (main and control, once, the v134 seed and designs; logs in run136/). read_v136.py -> read/read_v136.json (557 by section, 578's gap
shares, the dense lines' runs, 579's classes, 589). Report: test_report_v136.md; findings_v136.md (590-595). The song's record stays on v134.

## v137 (Module 27.81, Window 157)

gen_v137_p58.py writes melody_v137_p58.py from melody_v136_p58.py with 600-603; tables/zeneng_v137_span.json. 602 over 262 by the writer's
ruling (intake.py). run_v137.sh (logs in run137/); read_v137.py -> read/read_v137.json (600-603 tests, 604's split, 557 by section).
Report: test_report_v137.md; findings_v137.md (610-617).
Side run for 610 (not of record): gen_v137s_p58.py -> melody_v137s_p58.py, run_v137s.sh (run137s/), read_v137s.py -> read/read_v137s.json (finding 618).

## Luthier v1 (formerly ZenEng v138; Module 27.82, Window 158)

gen_l1_p58.py writes melody_l1_p58.py from melody_v137_p58.py with 605 (the section's template) and 606 (the song's palette);
tables/luthier_v1_structure.json. luthier_read.py: 605-607's readings. run_l1.sh (runl1/); read_l1.py -> read/read_l1.json and
read/l1_pick_candidates.json (every survivor's coupling gain and judge score, for 607's pick once the kept quartile is supplied);
read_608.py -> read/read_608.json. Report: test_report_l1.md; findings_l1.md (619-626; 610-618 are v137's).
