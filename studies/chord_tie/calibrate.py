"""The two weights (PREDICTION.md). pass 0: base rates with both weights 1. Then the weights by the odds formula; then the shares under them.
    python3 studies/chord_tie/calibrate.py base | check"""
import os, sys, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M
KEPT = {"on": 0.632, "off": 0.562}; SONGS = (("55", "songs/p65/lyric55"), ("58", "songs/p68/lyric58"), ("50", "songs/p60/lyric50")); odds = lambda x: x / (1 - x)
def shares(stem, tie, N=400):
    L = json.load(open(os.path.join(ROOT, stem + ".json"))); spec = json.load(open(os.path.join(ROOT, stem + ".song.json")))["spec"]; spec["chord_tie"] = tie; E = M.Engine(spec)
    E.as_sung = lambda ns_: SL.melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]
    rng = random.Random(L.get("seed", 1)); a = b = c = d = 0; nb = 0
    for _ in range(N):
        cc, err = E.build(rng)
        if err or E.gates(cc): continue
        nb += 1
        for n in E.as_sung(cc["notes"]):
            ct = n["p"] % 12 in E.chord_at(n["on"])
            if E.on_beat(n["on"]): a += ct; b += 1
            else: c += ct; d += 1
    return dict(living=nb, on=round(a / max(1, b), 3), off=round(c / max(1, d), 3))
T = os.path.join(ROOT, "tables", "kept_chord_tie.json")
if sys.argv[1] == "base":
    base = {s: shares(stem, {"on": 1.0, "off": 1.0}) for s, stem in SONGS}; w = {k: round(sum(odds(KEPT[k]) / odds(base[s][k]) for s, _ in SONGS) / len(SONGS), 3) for k in ("on", "off")}
    out = dict(note="749.198: the favour for a chord tone in a fresh line, by the kept odds over the draw's own base odds (both weights 1), averaged over songs 55, 58 and 50 (studies/chord_tie). Kept: 160 songs, triads, a beat is a quarter.", kept_share_of_chord_tones=KEPT, kept_on_beat_by_song_10_25_50_75_90=[0.441, 0.534, 0.635, 0.728, 0.825], base=base, weights=w)
    json.dump(out, open(T, "w"), indent=1); print(json.dumps(out, indent=1))
else:
    t = json.load(open(T)); under = {s: shares(stem, t["weights"]) for s, stem in SONGS}; t["shares_under_the_weights"] = under; json.dump(t, open(T, "w"), indent=1); print(json.dumps(under))
