"""749.104 with 749.122, tried outside the engine: the bar fit. See PREDICTION.md. python3 studies/bar_fit/trial.py [N] -> trial.json  (PYTHONHASHSEED=0)"""
import sys, os, json, random, collections, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
import metre_engine as M, soundness as S
N = int(sys.argv[1]) if len(sys.argv) > 1 else 150; FIG, RHY, STR = "bars on a figure already sung", "bars on a rhythm already sung", "stressed syllables on a beat"
KR = json.load(open(os.path.join(ROOT, "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]
def bar_fit(self, rng, src, src_st0, sy, U, sec, i, tmin, slot):
    floor = max(tmin, 0) if (sy[0][1] and not src_st0 and src[0][0] < 0) else tmin
    keep = [(t, p) for t, p in src if t >= floor] or src[-1:]; on = [t for t, p in keep]; ps = [p for t, p in keep]; n = len(sy); mu, lo, hi = self.reg(sec, i)
    def nb(p, up):
        q = p + (1 if up else -1)
        while q % 12 not in self.SCALE: q += 1 if up else -1
        return q
    while len(on) < n:                                                                         # more syllables: split the longest note; its second half does not repeat the pitch
        gaps = [((on[j + 1] if j + 1 < len(on) else slot - 6) - on[j], -j) for j in range(len(on))]; g, j = max(gaps); j = -j
        if g < 6: return None
        h = on[j] + (g // 2 // 3) * 3
        if h <= on[j]: return None
        nxt = ps[j + 1] if j + 1 < len(ps) else ps[j]
        if nxt != ps[j]:
            q = nb(ps[j], nxt > ps[j])
            if q == nxt: q = nb(ps[j], nxt < ps[j])                                            # a step apart: the other neighbour, so the split does not land on the next note
        else: q = nb(ps[j], ps[j] < mu)
        on.insert(j + 1, h); ps.insert(j + 1, q)
    while len(on) > n:                                                                         # fewer syllables: drop the note the bar misses least
        c = [(ps[j - 1] == ps[j + 1] and ps[j] != ps[j - 1], ps[j] != ps[j - 1], bool(self.on_beat(U + on[j])), on[j + 1] - on[j], j) for j in range(1, len(on) - 1)]
        if not c: return None
        j = min(c)[-1]; del on[j]; del ps[j]
    out = []
    for t, p in zip(on, ps):                                                                   # the engine's own corrections, as in Engine.again
        ch = self.chord_at(U + t); j_ = on.index(t); long_ = j_ == len(on) - 1 or on[j_ + 1] - t >= self.BEAT
        if self.S.get("clash_rule") and long_ and p % 12 not in ch and ((p + 1) % 12 in ch or (p - 1) % 12 in ch):
            p = min((p + d for d in (-1, 1, -2, 2, -3, 3, -4, 4) if (p + d) % 12 in self.SCALE and (p + d) % 12 in ch and lo <= p + d <= hi), key=lambda q_: abs(q_ - p), default=p)
        if self.on_beat(U + t) and p % 12 not in ch: p = min((p + d for d in (-1, 1, -2, 2) if (p + d) % 12 in self.SCALE and (p + d) % 12 in ch), key=lambda q_: abs(q_ - p), default=p)
        while p > hi: p -= 12 if p - 12 >= lo else 1
        while p < lo: p += 1
        while p % 12 not in self.SCALE: p -= 1
        if self.S.get("clash_rule") and long_ and p % 12 not in ch and ((p + 1) % 12 in ch or (p - 1) % 12 in ch):
            p = min((p + d for d in (-1, 1, -2, 2, -3, 3, -4, 4) if (p + d) % 12 in self.SCALE and (p + d) % 12 in ch and lo <= p + d <= hi), key=lambda q_: abs(q_ - p), default=p)
        out.append((t, p))
    return out
def row(ns): return S.record_row(dict(melody=dict(notes=[dict(n, midi=n["p"]) for n in sorted(ns, key=lambda n: n["on"])]), checks={"the chorus's median over the verse's, semitones": 0, "rest share inside sung sections": 0}))
out = {}
for tag, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("59", "songs/p69/lyric59")):
    spec = json.load(open(os.path.join(ROOT, p + ".song.json")))["spec"]; tg = spec["target"]; aim = dict(zip(KR["names"], KR["rows"][tg["kept_song_row"]])); res = {}
    for form in ("the engine's refit", "the bar fit"):
        E = M.Engine(spec); fresh = {}; orig = E.pitches
        def rec_p(rng, ons, U, sec, i, prev, avoid=None, end_off=None, orig=orig, fresh=fresh):
            ps = orig(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off); fresh[(sec, i)] = ps; return ps
        E.pitches = rec_p
        if form == "the bar fit": E.again = bar_fit.__get__(E)
        rng = random.Random(17); rows = []; made = 0
        for _ in range(N):
            fresh.clear(); c, err = E.build(rng); made += 1
            if err or E.gates(c): continue
            r = row(c["notes"]); by = collections.OrderedDict()
            for n in c["notes"]: by.setdefault((n["sec"], n["line"]), []).append(n["p"])
            fr = [b == a for k, v in by.items() if fresh.get(k) == v for a, b in zip(v, v[1:])]; ot = [b == a for k, v in by.items() if fresh.get(k) != v for a, b in zip(v, v[1:])]
            rows.append({FIG: r[FIG], RHY: r[RHY], STR: r[STR], "repeated notes": r["repeated notes"], "the words' fit, whole": r["the words' fit, whole"], "fresh_repeats": float(np.mean(fr)) if fr else np.nan, "returning_repeats": float(np.mean(ot)) if ot else np.nan})
        res[form] = dict(builds=len(rows), tries=made, **{k: round(float(np.nanmedian([x[k] for x in rows])), 3) for k in rows[0]}) if rows else dict(builds=0, tries=made)
        print(tag, form, res[form], flush=True)
    a, b = res["the engine's refit"], res["the bar fit"]
    closed = {c: (round((b[c] - a[c]) / (aim[c] - a[c]), 2) if abs(aim[c] - a[c]) > 1e-9 else None) for c in (FIG, RHY)} if b.get("builds") else None
    out[tag] = dict(aims_at=tg["kept_song"], aim={c: round(float(aim[c]), 3) for c in (FIG, RHY, "repeated notes")}, forms=res, share_of_the_gap_closed=closed,
                    returning_over_fresh=round(b["returning_repeats"] - b["fresh_repeats"], 3) if b.get("builds") else None, returning_over_fresh_before=round(a["returning_repeats"] - a["fresh_repeats"], 3), builds_kept_share=round(b["builds"] / max(a["builds"], 1), 2))
    print(tag, {k: v for k, v in out[tag].items() if k != "forms"}, flush=True)
T3 = ("55", "54", "58")
c1 = all(sum((out[t]["share_of_the_gap_closed"][c] or 0) >= 1 / 3 for t in T3) >= 2 and all((out[t]["share_of_the_gap_closed"][c] or 0) >= 0 or abs(out[t]["forms"]["the bar fit"][c] - out[t]["forms"]["the engine's refit"][c]) <= 0.02 for t in T3) for c in (FIG, RHY))
c2 = all(out[t]["returning_over_fresh"] <= 0.03 for t in ("55", "54")); c3 = all(out[t]["forms"]["the bar fit"][STR] >= 0.446 and out[t]["builds_kept_share"] >= 2 / 3 for t in T3)
out["checks"] = {"1 bars return": bool(c1), "2 no extra repeats": bool(c2), "3 the words still sit": bool(c3), "passes": bool(c1 and c2 and c3)}; print(out["checks"])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "trial.json"), "w"), indent=1)
