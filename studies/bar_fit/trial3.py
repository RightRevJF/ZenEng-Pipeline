"""749.104, third trial outside the engine: the bar fit where the words allow. See PREDICTION3.md. python3 studies/bar_fit/trial3.py [N] -> trial3.json  (PYTHONHASHSEED=0)"""
import sys, os, json, random, collections, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
import song_from_lyric as SL, metre_engine as M, soundness as S, word_weight as WW_
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
def words_score(E, r, sy):
    o = [t for t, _ in r]; tr = WW_.tier(sy); return E.stress_score(o, sy, True) - E.WW["short"] * sum(1 for k in range(len(o) - 1) if tr[k] == 2 and o[k + 1] - o[k] <= 3)
FIT = "the words' fit, whole"; FORMS = (("the engine's refit", None), ("strict", 0.0), ("one note's worth", 1.0)); out = {}
for tag, p in (("55", "songs/p65/lyric55"), ("54", "songs/p64/lyric54"), ("58", "songs/p68/lyric58"), ("59", "songs/p69/lyric59")):
    spec = json.load(open(os.path.join(ROOT, p + ".song.json")))["spec"]; L = json.load(open(os.path.join(ROOT, p + ".json"))); tg = spec["target"]; aim = dict(zip(KR["names"], KR["rows"][tg["kept_song_row"]])); res = {}
    for form, margin in FORMS:
        E = M.Engine(spec); fresh = {}; orig = E.pitches; orig_again = E.again; took = collections.Counter()
        def rec_p(rng, ons, U, sec, i, prev, avoid=None, end_off=None, orig=orig, fresh=fresh):
            ps = orig(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off); fresh[(sec, i)] = ps; return ps
        def again(rng, src, src_st0, sy, U, sec, i, tmin, slot, E=E, orig_again=orig_again, margin=margin, took=took):
            a = orig_again(rng, src, src_st0, sy, U, sec, i, tmin, slot)                        # the engine's refit is always made first, so the draws stay in step
            if margin is None or not (E.WW and E.WW["again"]): return a
            b = bar_fit(E, rng, src, src_st0, sy, U, sec, i, tmin, slot)
            if b is None or b[0][0] < tmin or any(y[0] - x[0] < 3 for x, y in zip(b, b[1:])): took["engine"] += 1; return a
            if a is None or words_score(E, b, sy) >= words_score(E, a, sy) - margin * E.WW["cost"]: took["bar"] += 1; return b
            took["engine"] += 1; return a
        E.pitches = rec_p; E.again = again; rng = random.Random(17); rows = []; made = 0
        for _ in range(N):
            fresh.clear(); c, err = E.build(rng); made += 1
            if err or E.gates(c): continue
            r = row(SL.melisma_notes(c["notes"], L, set(spec["scale"]), key="p", how=spec.get("how"), cap=tg.get("run"), share=tg.get("melisma_share"))[0]); by = collections.OrderedDict()
            for n in c["notes"]: by.setdefault((n["sec"], n["line"]), []).append(n["p"])
            fr = [y == x for k, v in by.items() if fresh.get(k) == v for x, y in zip(v, v[1:])]; ot = [y == x for k, v in by.items() if fresh.get(k) != v for x, y in zip(v, v[1:])]
            rows.append({FIG: r[FIG], RHY: r[RHY], STR: r[STR], FIT: r[FIT], "repeated notes": r["repeated notes"], "over": (float(np.mean(ot)) - float(np.mean(fr))) if fr and ot else np.nan})
        res[form] = dict(builds=len(rows), tries=made, bar_fit_taken_share=round(took["bar"] / max(sum(took.values()), 1), 2), **{k: round(float(np.nanmedian([x[k] for x in rows])), 3) for k in rows[0]})
        print(tag, form, res[form], flush=True)
    out[tag] = dict(aims_at=tg["kept_song"], aim={c: round(float(aim[c]), 3) for c in (FIG, RHY, "repeated notes")}, forms=res)
T3 = ("55", "54", "58"); base = "the engine's refit"; d = lambda t, f, c: out[t]["forms"][f][c] - out[t]["forms"][base][c]; out["checks"] = {}
for f, _ in FORMS[1:]:
    c1 = sum(d(t, f, RHY) > 0 for t in T3) >= 2 and all(d(t, f, RHY) >= -0.01 and d(t, f, FIG) >= -0.01 for t in T3); c2 = all(d(t, f, FIT) >= -0.02 and d(t, f, STR) >= -0.03 for t in T3)
    c3 = all(d(t, f, "over") <= 0 for t in ("55", "54")); c4 = all(out[t]["forms"][f]["builds"] >= 0.9 * out[t]["forms"][base]["builds"] for t in T3)
    out["checks"][f] = {"1 bars return": bool(c1), "2 the words hold": bool(c2), "3 no extra repeats": bool(c3), "4 builds survive": bool(c4), "passes": bool(c1 and c2 and c3 and c4), "gain_in_bars_on_a_rhythm_already_sung": [round(d(t, f, RHY), 3) for t in T3]}
    print(f, out["checks"][f])
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "trial3.json"), "w"), indent=1)
