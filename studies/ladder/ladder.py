"""749.203: the ladder. Each v50 record's fitted spec; the draw's parts added one at a time from the barest draw (up), and the full engine with each part left out alone (down).
    python3 studies/ladder/ladder.py kept                    -> kept.json (the kept middle halves of the figures)
    OUT=x.json N=300 python3 studies/ladder/ladder.py run stem ...   -> the rungs"""
import os, sys, json, random, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "lib", "carol"), os.path.join(ROOT, "tables", "metre_atlas")]
import numpy as np
ORDER = ["register", "degrees", "chord", "clash", "moves", "words", "memory", "runs", "end_off", "plant", "borrow", "again", "lift", "gates"]; DRAW = {"register", "degrees", "chord", "moves", "words", "memory", "runs", "end_off"}
FIGS = ["between lines", "within lines", "share on the commonest pitch", "a line's first note less its middle", "a line's last note less its middle", "a line's range", "spread of the lines' first notes", "on-beat chord tones"]
def verse_figs(lines):
    lines = [l for l in lines if len(l) >= 3]
    if len(lines) < 3: return None
    w = np.array([len(l) for l in lines], float); mids = np.array([np.mean(l) for l in lines]); m = float(np.sum(w * mids) / w.sum())
    return {"between lines": float(np.sqrt(np.sum(w * (mids - m) ** 2) / w.sum())), "within lines": float(np.sqrt(sum(np.sum((np.array(l, float) - np.mean(l)) ** 2) for l in lines) / w.sum())),
            "a line's first note less its middle": float(np.mean([l[0] - np.mean(l) for l in lines])), "a line's last note less its middle": float(np.mean([l[-1] - np.mean(l) for l in lines])), "a line's range": float(np.median([max(l) - min(l) for l in lines])), "spread of the lines' first notes": float(np.std([l[0] for l in lines]))}
q = lambda v: [round(float(x), 3) for x in np.percentile(v, (25, 50, 75))]
if sys.argv[1] == "kept":
    import kept_corpus as KC
    R = collections.defaultdict(list); d = KC.table(); K = set(json.load(open(os.path.join(ROOT, "tables", "kept_songs_4-4_pop.json"))))
    for k in KC.kept_songs():
        cur = None; lines = collections.OrderedDict(); vp = []
        def flush():
            if cur == "verse" and lines:
                f = verse_figs(list(lines.values()))
                if f:
                    for a, b in f.items(): R[a].append(b)
        for i, (l, s) in enumerate(zip(k["lines"], k["sec"])):
            if str(s) != cur: flush(); cur = str(s); lines = collections.OrderedDict()
            lines.setdefault(l, []).append(int(k["p"][i]))
            if str(s) == "verse": vp.append(int(k["p"][i]))
        flush()
        if len(vp) >= 40: R["share on the commonest pitch"].append(collections.Counter(vp).most_common(1)[0][1] / len(vp))
    out = {a: q(b) for a, b in R.items()}; out["on-beat chord tones"] = [0.534, 0.635, 0.728]; out["note"] = "kept quartiles (25th, 50th, 75th): line figures by verse section; the share by song; on-beat chord tones by song (studies/held_chord)"
    json.dump(out, open(os.path.join(HERE, "kept.json"), "w"), indent=1); print(json.dumps(out, indent=1))
else:
    import song_from_lyric as SL, metre_engine as M, make_kept_commonest_pitch as CP
    N = int(os.environ.get("N", "300")); out = {}
    def spec_for(rec, on, full=False):
        spec = json.loads(json.dumps(rec["spec"]))
        if not full: spec["ladder_off"] = sorted(DRAW - set(on))
        if "clash" not in on: spec["clash_rule"] = False
        if "plant" not in on: spec["target"].pop("peak", None)
        if "borrow" not in on: spec["borrow"] = None
        if "again" not in on: spec["how"] = {k: v for k, v in spec.get("how", {}).items() if v[0] not in ("again", "copy")}
        if "lift" not in on: spec["vary_returns"] = []
        return spec
    def read(L, spec, gates):
        E = M.Engine(spec); E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
        rng = random.Random(L.get("seed", 1)); F = collections.defaultdict(list); nb = made = 0; a = b = 0
        for _ in range(N):
            c, err = E.build(rng)
            if err: continue
            made += 1
            if gates and E.gates(c): continue
            nb += 1; s = sorted(E.as_sung(c["notes"]), key=lambda n: n["on"]); by = collections.OrderedDict(); vp = []
            for n in s:
                if E.on_beat(n["on"]): a += n["p"] % 12 in E.chord_at(n["on"]); b += 1
                if CP.kind(n["sec"]) == "Verse": by.setdefault(n["sec"], collections.OrderedDict()).setdefault(n["line"], []).append(n["p"]); vp.append(n["p"])
            for lines in by.values():
                f = verse_figs(list(lines.values()))
                if f:
                    for x, y in f.items(): F[x].append(y)
            if vp: F["share on the commonest pitch"].append(collections.Counter(vp).most_common(1)[0][1] / len(vp))
        o = {x: round(float(np.median(y)), 3) for x, y in F.items()}; o["on-beat chord tones"] = round(a / max(1, b), 3); o["builds"] = nb; o["complete"] = made; return o
    for stem in sys.argv[2:]:
        L = json.load(open(stem + ".json")); rec = json.load(open(stem + ".song.json")); name = os.path.basename(stem); o = dict(up={}, down={})
        on = []
        o["up"]["the barest draw"] = read(L, spec_for(rec, on), False); print(name, "up", "bare", o["up"]["the barest draw"], flush=True)
        for part in ORDER:
            on.append(part); o["up"]["+ " + part] = read(L, spec_for(rec, on), "gates" in on); print(name, "up +", part, o["up"]["+ " + part], flush=True)
        o["full"] = read(L, spec_for(rec, ORDER, full=True), True); print(name, "full", o["full"], flush=True)
        for part in ORDER[:-1]:
            o["down"]["without " + part] = read(L, spec_for(rec, [x for x in ORDER if x != part]), True); print(name, "down -", part, o["down"]["without " + part], flush=True)
        o["down"]["without gates"] = read(L, spec_for(rec, ORDER, full=True), False)
        out[name] = o
    json.dump(out, open(os.path.join(HERE, os.environ.get("OUT", "rungs.json")), "w"), indent=1)
