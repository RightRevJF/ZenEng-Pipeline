"""Verses that pile on one pitch (PREDICTION.md).  python3 studies/one_pitch_verses/read.py builds songs/p60/lyric50   |   python3 ... chords   |   python3 ... kept"""
import os, sys, json, random, collections, statistics as st
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
mode = sys.argv[1]
if mode == "builds":
    import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
    stem = sys.argv[2]; L = json.load(open(os.path.join(ROOT, stem + ".json"))); rec = json.load(open(os.path.join(ROOT, stem + ".song.json"))); ref = json.load(open(os.path.join(ROOT, "songs/p65/lyric55.song.json")))["spec"]; out = {}
    def switched(name):
        spec = json.loads(json.dumps(rec["spec"]))
        if name == "blue notes":
            for k, w in spec["degrees"]["weights"].items():
                for dgr in ("3", "10"): w[dgr] = ref["degrees"]["weights"][k][dgr]
            spec["degrees"]["blue"] = [3, 10]
        if name == "the repeat weight": spec["target"]["moves"]["repeat"] = ref["target"]["moves"]["repeat"]
        if name == "verse lines drawn fresh": spec["how"] = {k: v for k, v in spec.get("how", {}).items() if not (CP.kind(k.rsplit(":", 1)[0]) == "Verse" and v[0] in ("again", "copy"))}
        if name == "the chord's pull halved": spec["chord_pull"] = 0.5
        return spec
    for name in ("as it is", "blue notes", "the repeat weight", "verse lines drawn fresh", "the chord's pull halved"):
        spec = switched(name); E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); nb = 0; over = 0; sh = []; fits = []
        for _ in range(1000):
            c, err = E.build(rng)
            if err or E.gates(c): continue
            nb += 1; ps = [n["p"] for n in E.as_sung(c["notes"]) if CP.kind(n["sec"]) == "Verse"]; s_ = collections.Counter(ps).most_common(1)[0][1] / len(ps); sh.append(s_); over += s_ > spec["pitch_ceiling"]["Verse"]
        out[name] = dict(living=nb, verses_over_the_ceiling_in_100=round(100 * over / max(1, nb), 1), middle_share_on_the_commonest_pitch=round(st.median(sh), 3) if sh else None); print(os.path.basename(stem), name, out[name], flush=True)
    json.dump(out, open(os.path.join(HERE, f"switches_{os.path.basename(stem)}.json"), "w"), indent=1)
if mode == "chords":
    P = {"55": "songs/p65/lyric55.song.json", "54": "songs/p64/lyric54.song.json", "58": "songs/p68/lyric58.song.json", "49": "songs/p59/lyric49.song.json", "60": "songs/p70/lyric60.v50.song.json", "59": "songs/p69/lyric59.song.json", "61": "songs/p71/lyric61.song.json", "50": "songs/p60/lyric50.song.json"}; out = {}
    for s, p in P.items():
        r = json.load(open(os.path.join(ROOT, p))); bars = []
        for n, k, b in r["form"]:
            if k == "verse" and n in r["roman"]: bars += [x.split()[0] for x in r["roman"][n]]
        c = collections.Counter(bars); pc = r["judge7"].get("pitch_ceiling", {}); out[s] = dict(verse_bars=len(bars), different_chords=len(c), share_of_bars_on_the_commonest_chord=round(c.most_common(1)[0][1] / len(bars), 3), commonest=c.most_common(1)[0][0], ceiling_passed_of_read=[pc.get("passed"), pc.get("read")], blue=bool(r["spec"]["degrees"].get("blue_song")))
        print(s, out[s])
    json.dump(out, open(os.path.join(HERE, "chords.json"), "w"), indent=1)
if mode == "kept":
    import kept_corpus as KC, numpy as np
    d = KC.table(); K = set(json.load(open(os.path.join(ROOT, "tables", "kept_songs_4-4_pop.json")))); rows = []
    for s, g in d[d.song.astype(str).isin(K) & (d.section.astype(str) == "verse")].groupby("song"):
        if len(g) < 40: continue
        ps = collections.Counter(g.pitch.astype(int)); ch = collections.Counter(g.roman.astype(str)); rows.append((ps.most_common(1)[0][1] / len(g), ch.most_common(1)[0][1] / len(g), len(ch)))
    a = np.array(rows); r = float(np.corrcoef(a[:, 0], a[:, 1])[0, 1]); still = a[a[:, 1] >= np.percentile(a[:, 1], 75)]; moving = a[a[:, 1] <= np.percentile(a[:, 1], 25)]
    q = lambda v: [round(float(x), 3) for x in np.percentile(v, (25, 50, 75, 90))]
    out = dict(kept_songs_with_a_verse=len(a), share_on_the_commonest_pitch_25_50_75_90=q(a[:, 0]), notes_under_the_commonest_chord_25_50_75_90=q(a[:, 1]), correlation=round(r, 3), stillest_quarter_of_verses=dict(n=len(still), share_on_the_commonest_pitch_25_50_75_90=q(still[:, 0]), over_0_44=round(float((still[:, 0] > 0.44).mean()), 3)), most_moving_quarter=dict(n=len(moving), share_on_the_commonest_pitch_25_50_75_90=q(moving[:, 0]), over_0_44=round(float((moving[:, 0] > 0.44).mean()), 3)), all_over_0_44=round(float((a[:, 0] > 0.44).mean()), 3))
    json.dump(out, open(os.path.join(HERE, "kept.json"), "w"), indent=1); print(json.dumps(out, indent=1))
