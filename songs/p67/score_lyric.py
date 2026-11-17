"""score_lyric.py: a draft of song 57 against the hook rules (Part 30) and the lyric rules (Part 32). Usage: python3 score_lyric.py lyric_draftN.md"""
import sys, re, json, numpy as np
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/lyrics")
import lyrics_features as LF
from intake import NEVER_SAY, NEVER_PHRASES, TITLE
t = open(sys.argv[1]).read(); secs, order, cur = {}, [], None
for l in t.split("\n"):
    if l.startswith("## "): cur = l[3:].strip(); order.append(cur); secs.setdefault(cur, [])
    elif l.strip() and cur and not l.startswith("#"): secs[cur].append(l.strip())
lines = []
for s in order:
    if s == "Jam": continue
    lines += secs[s] if secs[s] else secs.get(re.sub(r" \d+$", "", s), secs["Chorus"])
f = LF.features(lines, TITLE); R = json.load(open("/home/claude/zeneng-pipeline/studies/lyrics/lyrics_rows_scored.json"))
def pct(k, g="RS"):
    v = np.array([x[k] for x in R if x["group"] == g and x.get(k) is not None], float); return round(float(((v < f[k]).mean() + 0.5 * (v == f[k]).mean()) * 100))
low = " ".join(lines).lower(); words = re.findall(r"[a-z']+", low)
hits = [w for w in NEVER_SAY if w in words] + [p for p in NEVER_PHRASES if p in low]
ch = secs["Chorus"]; tl = TITLE.lower()
print(f"lines sung {len(lines)}; never-say hits {hits or 'none'}")
print(f"L1 repeated lines {f['repeated_lines']:.2f} (band 0.42-0.57; greatest-list pct {pct('repeated_lines')})")
print(f"L2 feeling's range {f['valence_sd']:.2f} (floor 0.22, aim 0.26; pct {pct('valence_sd')})")
print(f"L5 rare words {f['rare']*100:.1f}% (at most ~4%)   concreteness {f['conc']:.2f} (pct {pct('conc')})   absolutes/line {f['absolutes']:.3f}")
print(f"H title per chorus {sum(tl in l.lower() for l in ch)}; in chorus line 1: {tl in ch[0].lower()}; title in song {f['title_n']}")
if "-v" in sys.argv:
    seen = set()
    for l in lines:
        if l in seen: continue
        seen.add(l); print(f"{LF.VADER.polarity_scores(l)['compound']:+.2f}  {l}")
if "-a" in sys.argv:
    print("L4 story readings per 100 words:", {k: round(f[k] * (100 if f[k] < 1 else 1), 2) for k in ("past", "time", "place", "propn", "third") if f.get(k) is not None},
          "| greatest-list pct:", {k: pct(k) for k in ("past", "time", "place", "propn", "third") if f.get(k) is not None})
    print(f"L3 ending (last fifth minus the rest) {f['ending']:+.2f}; sad ending: {bool(f['sad_end'])}")
    arc = []
    for s in order:
        if s == "Jam": arc.append((s, None)); continue
        ls = secs[s] if secs[s] else secs["Chorus"]; arc.append((s, np.mean([LF.VADER.polarity_scores(l)["compound"] for l in ls])))
    print("L2 arc:", " | ".join(f"{s} {'(jam)' if v is None else f'{v:+.2f}'}" for s, v in arc))
