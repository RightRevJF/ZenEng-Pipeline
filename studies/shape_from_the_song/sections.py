"""Does Luthier's own rule of movement hold in kept songs? See PREDICTION_sections.md. python3 studies/shape_from_the_song/sections.py -> sections.json"""
import sys, os, json, numpy as np
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")); sys.path.insert(0, os.path.join(ROOT, "lib", "luthier"))
import kept_corpus as KC
def kind(x): x = str(x).lower(); return "chorus" if ("chorus" in x or "refrain" in x) else "verse" if "verse" in x else "bridge" if "bridge" in x else None
rows = []
for k in KC.kept_songs():
    p = np.asarray(k["p"]); sec = [kind(x) for x in k["sec"]]; d = {}
    for nm in ("verse", "chorus"):
        iv = [abs(int(p[i + 1]) - int(p[i])) for i in range(len(p) - 1) if sec[i] == nm and sec[i + 1] == nm]; ps = [int(x) for x, s in zip(p, sec) if s == nm]
        if len(iv) >= 30: d[nm] = dict(step=float(np.mean([1 <= x <= 2 for x in iv])), leap=float(np.mean([x >= 5 for x in iv])), repeat=float(np.mean([x == 0 for x in iv])), top=max(ps), median=float(np.median(ps)))
    if len(d) == 2: rows.append(d)
n = len(rows); f = lambda c: np.array([r["verse"][c] - r["chorus"][c] for r in rows])
out = dict(songs=n,
    verses_step_more=dict(share_of_songs=round(float(np.mean(f("step") > 0)), 2), middle_difference=round(float(np.median(f("step"))), 3), verse_middle=round(float(np.median([r["verse"]["step"] for r in rows])), 3), chorus_middle=round(float(np.median([r["chorus"]["step"] for r in rows])), 3)),
    choruses_leap_more=dict(share_of_songs=round(float(np.mean(f("leap") < 0)), 2), middle_difference=round(float(np.median(-f("leap"))), 3), verse_middle=round(float(np.median([r["verse"]["leap"] for r in rows])), 3), chorus_middle=round(float(np.median([r["chorus"]["leap"] for r in rows])), 3)),
    repeated_notes=dict(verse_over_chorus_share_of_songs=round(float(np.mean(f("repeat") > 0)), 2), verse_middle=round(float(np.median([r["verse"]["repeat"] for r in rows])), 3), chorus_middle=round(float(np.median([r["chorus"]["repeat"] for r in rows])), 3)),
    the_top_is_the_choruss=dict(share_of_songs=round(float(np.mean(f("top") <= 0)), 2), chorus_strictly_higher=round(float(np.mean(f("top") < 0)), 2), middle_chorus_median_over_verse_median=round(float(np.median(-f("median"))), 2)))
a, b, c = out["verses_step_more"], out["choruses_leap_more"], out["the_top_is_the_choruss"]
out["holds"] = {"verses step more": bool(a["share_of_songs"] >= 0.6 and a["middle_difference"] >= 0.02), "choruses leap more": bool(b["share_of_songs"] >= 0.6 and b["middle_difference"] >= 0.01), "the top is the chorus's": bool(c["share_of_songs"] >= 0.6)}
print(json.dumps(out, indent=1)); json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sections.json"), "w"), indent=1)
