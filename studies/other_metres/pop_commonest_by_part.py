"""749.255: the pop 3/4 clips' commonest-pitch share, a clip at a time (a clip is a section), by the clip's section label where Hooktheory gives one. Clips of 20 notes or more, as 956 reads a part. python3 -I studies/other_metres/pop_commonest_by_part.py -> prints JSON. The corpus stays outside the repository."""
import os, sys, json, gzip, collections, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "..", "lib", "luthier"), os.path.join(HERE, "..", "..", "lib", "carol"), os.path.join(HERE, "..", "..", "tables", "metre_atlas")]
import numpy as np, hooktheory_tables as HT
def label(x):
    u = (x["hooktheory"].get("urls") or {}).get("clip") or ""; m = re.search(r"#([a-z\-]+)", u); s = (m.group(1) if m else "").lower()
    return "Chorus" if "chorus" in s else "Verse" if "verse" in s else "Bridge" if "bridge" in s else ("other: " + s if s else "no label")
if __name__ == "__main__":
    D = json.load(gzip.open(HT.SRC)); G = collections.defaultdict(list); labels = collections.Counter(); urls = []
    for k, x in D.items():
        m = x["annotations"]["meters"]
        if len(m) != 1 or (m[0]["beats_per_bar"], m[0]["beat_unit"]) != (3, 4) or "MELODY" not in x["tags"] or HT.left_out(x["hooktheory"]): continue
        ns = HT.clip_notes(x, 12)
        if ns is None or len(ns) < 20: continue
        p = [n[2] for n in ns]; sh = max(collections.Counter(p).values()) / len(p); lb = label(x); labels[lb] += 1; G["every clip"].append(sh); G[lb if lb in ("Verse", "Chorus", "Bridge") else "other or no label"].append(sh)
        if len(urls) < 3: urls.append(sorted((x["hooktheory"].get("urls") or {}).keys()))
    q = lambda v: [round(float(a), 3) for a in np.percentile(v, (10, 25, 50, 75, 90))]
    print(json.dumps(dict(source="Hooktheory clips written in 3/4, the pop table's filter, 20 notes or more a clip", url_keys_seen=urls, labels=dict(labels.most_common(12)), by_part={k: dict(clips=len(v), p10_25_50_75_90=q(v), ceiling_the_90th=q(v)[4]) for k, v in G.items()}), indent=1))
