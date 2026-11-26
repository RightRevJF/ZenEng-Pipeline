"""The melody under a chord that stays (PREDICTION.md).  python3 read.py kept | python3 read.py builds stem | python3 read.py switches stem"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
BANDS = ("under 1 bar", "1 to 2", "2 to 4", "4 or more"); band = lambda b: 0 if b < 1 else 1 if b < 2 else 2 if b < 4 else 3
def summarise(seqs):
    """seqs: lists of (bar, on_beat, is_chord_tone, pitch, chord_id) in order, one list a section"""
    T = [[0, 0] for _ in BANDS]; R = [[0, 0] for _ in BANDS]; runs = []
    for s in seqs:
        start = None; cur = None; prev = None; run = []
        for bar, ob, ct, p, ch in s:
            if ch != cur:
                if run and run[-1][0] - run[0][0] + 1 >= 4: runs.append([x[1] for x in run])
                cur = ch; start = bar; run = []
            k = band(bar - start); run.append((bar, p))
            if ob: T[k][0] += ct; T[k][1] += 1
            if prev is not None: R[k][0] += p == prev; R[k][1] += 1
            prev = p
        if run and run[-1][0] - run[0][0] + 1 >= 4: runs.append([x[1] for x in run])
    sh = [collections.Counter(r).most_common(1)[0][1] / len(r) for r in runs if len(r) >= 8]
    return dict(on_beat_chord_tones={b: round(T[i][0] / T[i][1], 3) if T[i][1] else None for i, b in enumerate(BANDS)}, on_beat_notes={b: T[i][1] for i, b in enumerate(BANDS)}, repeats={b: round(R[i][0] / R[i][1], 3) if R[i][1] else None for i, b in enumerate(BANDS)},
                stretches_of_four_bars_or_more=len(sh), share_on_a_stretchs_commonest_pitch_quartiles=[round(x, 3) for x in (sorted(sh)[int(.25 * (len(sh) - 1))], st.median(sh), sorted(sh)[int(.75 * (len(sh) - 1))])] if sh else None)
mode = sys.argv[1]
if mode == "kept":
    import kept_corpus as KC
    d = KC.table(); K = set(json.load(open(os.path.join(ROOT, "tables", "kept_songs_4-4_pop.json")))); d = d[d.song.astype(str).isin(K) & d.roman.notna() & d.chord_deg.notna()]; seqs = []; vseqs = []
    MAJ = [0, 2, 4, 5, 7, 9, 11]; MIN = [0, 2, 3, 5, 7, 8, 10]; Q = {"maj": (0, 4, 7), "min": (0, 3, 7), "dim": (0, 3, 6), "aug": (0, 4, 8)}
    for s, g in d.groupby("song", sort=False):
        g = g.sort_values("abs_beat"); s_ = []; sec = None
        for r in g.itertuples():
            root = (int(r.key_pc) + (MIN if str(r.mode) == "minor" else MAJ)[int(r.chord_deg) - 1] - (1 if str(r.roman).startswith("b") else 0) + (1 if str(r.roman).startswith("#") else 0)) % 12
            row = (int(r.bar), float(r.beat) == int(r.beat), (int(r.pitch) - root) % 12 in Q.get(str(r.chord_qual), (0, 4, 7)), int(r.pitch), str(r.roman))
            if str(r.section) != sec:
                if s_: (vseqs if sec == "verse" else seqs).append(s_)
                s_ = []; sec = str(r.section)
            s_.append(row)
        if s_: (vseqs if sec == "verse" else seqs).append(s_)
    out = dict(all_sections=summarise(seqs + vseqs), verses=summarise(vseqs)); json.dump(out, open(os.path.join(HERE, "kept.json"), "w"), indent=1); print(json.dumps(out, indent=1))
else:
    import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
    stem = sys.argv[2]; L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); name = os.path.basename(stem)
    def engine(sw=()):
        spec = json.loads(json.dumps(rec["spec"]))
        if "memory" in sw: spec["page_gate"]["memory"] = 1.0
        if "pull" in sw: spec["chord_pull"] = 0.0
        if "clash" in sw: spec["clash_rule"] = False
        if "fresh" in sw: spec["how"] = {k: v for k, v in spec.get("how", {}).items() if not (CP.kind(k.rsplit(":", 1)[0]) == "Verse" and v[0] in ("again", "copy"))}
        E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]; return E, spec
    def living(E):
        rng = random.Random(L.get("seed", 1))
        for _ in range(1000):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            yield sorted(E.as_sung(c["notes"]), key=lambda n: n["on"])
    if mode == "builds":
        E, spec = engine(); seqs = []; vseqs = []
        for sung in living(E):
            by = collections.OrderedDict()
            for n in sung: by.setdefault(n["sec"], []).append(n)
            for sec, ns in by.items():
                s_ = [(n["on"] // E.BAR, E.on_beat(n["on"]), n["p"] % 12 in E.chord_at(n["on"]), n["p"], tuple(sorted(E.chord_at(n["on"])))) for n in ns]; (vseqs if CP.kind(sec) == "Verse" else seqs).append(s_)
        out = dict(all_sections=summarise(seqs + vseqs), verses=summarise(vseqs)); json.dump(out, open(os.path.join(HERE, f"builds_{name}.json"), "w"), indent=1); print(name, json.dumps(out), flush=True)
    if mode == "switches":
        out = {}
        for label, sw in (("8. the figure memory off", ("memory",)), ("9. memory, pull, clash rule off", ("memory", "pull", "clash")), ("10. fresh verse lines, pull, clash rule off", ("fresh", "pull", "clash")), ("11. all four", ("memory", "fresh", "pull", "clash"))):
            E, spec = engine(sw); sh = []
            for sung in living(E):
                ps = [n["p"] for n in sung if CP.kind(n["sec"]) == "Verse"]; sh.append(collections.Counter(ps).most_common(1)[0][1] / len(ps))
            out[label] = dict(living=len(sh), verses_over_the_ceiling_in_100=round(100 * sum(x > 0.44 for x in sh) / max(1, len(sh)), 1), middle_share=round(st.median(sh), 3) if sh else None); print(name, label, out[label], flush=True)
        json.dump(out, open(os.path.join(HERE, f"switches_{name}.json"), "w"), indent=1)
