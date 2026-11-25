"""749.159, read on many drafts instead of one plan: within-section chord repetition of the writer's verses, choruses and bridges under each form of loop_less,
and the stage 4 held-out readings (written sections against held-out kept sections, beside the unpatched writer). See PREDICTION.md.
    python3 studies/proposed_v47/drafts.py off|loop_templates|loop_structure|loop_gate -> drafts_<form>.json"""
import os, sys, json, random, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier")); form = sys.argv[1]
sys.argv = ["run.py", "x", "0", form, "x"]; src = open(os.path.join(HERE, "run.py")).read(); exec(src[src.index("import proposed_v47"):src.index("import song_from_lyric")].replace('if os.path.basename(f).split(".")[0] in P.HOLDOUTS: raise SystemExit(f"{f} is a hold-out: not run")', ""))
ALL = json.load(open(C.DATA)); out = dict(form=form, repetition={}, stage4={})
for mode in ("major", "minor"):
    songs = [s for s in ALL if s["mode"] == mode]; W = C.Writer(mode, songs); S = C.sections(songs, mode); rng = random.Random(749159)
    for k in ("verse", "chorus", "bridge"):
        src_ = [b for kk, b, _, _ in S if kk == k]; kept = [r for r in (rep_of(b) for b in src_) if r is not None]; wrote = []
        for _ in range(1000):
            W.chromatic = C.weight_for(rng.choice(W.kept_out) * W.setting, mode) if W.setting > 0 else 0.0
            r = rep_of(W.section(rng, k, len(rng.choice(src_))))
            if r is not None: wrote.append(r)
        out["repetition"][f"{mode} {k}"] = dict(kept_sections=len(kept), kept_median=round(st.median(kept), 3), kept_mean=round(st.mean(kept), 3), written_median=round(st.median(wrote), 3), written_mean=round(st.mean(wrote), 3), written_at_or_under_the_kept_median=round(sum(w <= st.median(kept) for w in wrote) / len(wrote), 3))
    random.Random(56).shuffle(songs); cut = int(0.8 * len(songs)); tr, te = songs[:cut], songs[cut:]; W = C.Writer(mode, tr); KS = ("verse", "chorus", "bridge")
    held = [(k, b) for k, b, _, _ in C.sections(te) if k in KS]; train = [(k, b) for k, b, _, _ in C.sections(tr) if k in KS]; rng = random.Random(1); wrote = [(k, W.section(rng, k, len(b))) for k, b in held]
    cmp_ = C.compare(C.measures(held, mode), C.measures(wrote, mode)); fl = C.compare(C.measures(held, mode), C.measures(train, mode))
    out["stage4"][mode] = {k: dict(written={m: cmp_[k][m] for m in ("first", "last", "chords", "bigrams", "bars")}, floor={m: fl[k][m] for m in ("first", "last", "chords", "bigrams", "bars")}, loops_kept_written=cmp_[k]["loops"], distinct_bars_kept_written=cmp_[k]["distinct_bars"]) for k in cmp_}
json.dump(out, open(os.path.join(HERE, f"drafts_{form}.json"), "w"), indent=1); print(json.dumps(out["repetition"]))
