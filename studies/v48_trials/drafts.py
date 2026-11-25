"""749.178: the writer's sections under no gate, the median gate (960 as built) and the gentle gate, drawn as studies/proposed_v47/drafts.py drew them. PREDICTION.md, section 3.
    python3 studies/v48_trials/drafts.py -> drafts.json"""
import os, sys, json, random, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "lib", "luthier")))
import chord_writer as C
ALL = json.load(open(C.DATA)); rep = lambda b: C.chord_repetition(b); out = {}
for form in (False, True, "gentle"):
    o = dict(repetition={}, stage4={})
    for mode in ("major", "minor"):
        songs = [s for s in ALL if s["mode"] == mode]; W = C.Writer(mode, songs); W.loop_less = form; S = C.sections(songs, mode); rng = random.Random(749159)
        for k in ("verse", "chorus", "bridge"):
            src_ = [b for kk, b, _, _ in S if kk == k]; kept = [r for r in (rep(b) for b in src_) if r is not None]; wrote = []
            for _ in range(1000):
                W.chromatic = C.weight_for(rng.choice(W.kept_out) * W.setting, mode) if W.setting > 0 else 0.0
                r = rep(W.section(rng, k, len(rng.choice(src_))))
                if r is not None: wrote.append(r)
            q = lambda v, p: round(float(sorted(v)[int(p * (len(v) - 1))]), 3)
            o["repetition"][f"{mode} {k}"] = dict(kept_quartiles=[q(kept, .25), q(kept, .5), q(kept, .75)], written_quartiles=[q(wrote, .25), q(wrote, .5), q(wrote, .75)], written_at_or_under_the_kept_median=round(sum(w <= st.median(kept) for w in wrote) / len(wrote), 3), written_over_the_kept_75th=round(sum(w > q(kept, .75) for w in wrote) / len(wrote), 3))
        songs = list(songs); random.Random(56).shuffle(songs); cut = int(0.8 * len(songs)); tr, te = songs[:cut], songs[cut:]; W = C.Writer(mode, tr); W.loop_less = form; KS = ("verse", "chorus", "bridge")
        held = [(k, b) for k, b, _, _ in C.sections(te) if k in KS]; rng = random.Random(1); wrote = [(k, W.section(rng, k, len(b))) for k, b in held]; cmp_ = C.compare(C.measures(held, mode), C.measures(wrote, mode))
        o["stage4"][mode] = {k: dict(written={m: cmp_[k][m] for m in ("first", "last", "chords", "bigrams", "bars")}, loops_kept_written=cmp_[k]["loops"]) for k in cmp_}
    out[{False: "off", True: "median", "gentle": "gentle"}[form]] = o
json.dump(out, open(os.path.join(HERE, "drafts.json"), "w"), indent=1)
for f, o in out.items():
    print(f, {k: (v["written_at_or_under_the_kept_median"], v["written_over_the_kept_75th"], v["written_quartiles"]) for k, v in o["repetition"].items() if "chorus" not in k})
    for m in ("major", "minor"): print("  ", m, {k: (v["loops_kept_written"], v["written"]) for k, v in o["stage4"][m].items() if k != "chorus"})
