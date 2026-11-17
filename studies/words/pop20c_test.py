"""Setting words across the century: the Pop20c corpus (VanderStel and Temperley 2022; the most popular American song of each year,
1900-1999, melodies transcribed from recordings, stress from the CMU dictionary with monosyllabic function words unstressed).
Fetch: git clone --depth 1 https://github.com/vanderstel/pop-corpus.git into /home/claude/data/pop20c (no licence stated; derived counts only).
Songs in simple quadruple time only (every onset on a sixteenth grid of the measure). By period: weak syllables on beat 1, one-syllable
function words on beat 1 (unstressed one-syllable words), stressed syllables on offbeat eighths (and of those, anticipations: the next
strong beat left empty), the stressed syllable lower than the rest of its word, and stress against metre as contours inside and across words."""
import os, re, glob, json, collections, numpy as np
D = "/home/claude/data/pop20c/pop-corpus"; HERE = os.path.dirname(os.path.abspath(__file__))
YEAR = {}
for l in open(f"{D}/year_list.txt"):
    p = l.split()
    if len(p) >= 2: YEAR[p[1].strip()] = int(p[0])
def strength(f):
    f = round(f * 16) / 16
    if f == 0: return 4
    if f == 0.5: return 3
    if f in (0.25, 0.75): return 2
    if f in (0.125, 0.375, 0.625, 0.875): return 1
    return 0
def load(path):
    out = []
    for l in open(path):
        p = l.split()
        if len(p) < 6: continue
        on, off, midi, deg, st = float(p[0]), float(p[1]), int(p[2]), int(p[3]), int(p[4])
        m = re.match(r"(.+)\[(\d+)\]$", p[5])
        if not m: continue
        out.append(dict(on=on, off=off, p=midi, st=st, word=m.group(1), k=int(m.group(2))))
    return out
def period(y): return "1900-1929" if y < 1930 else "1930-1954" if y < 1955 else "1955-1979" if y < 1980 else "1980-1999"
R = collections.defaultdict(collections.Counter); used = collections.Counter()
for f in sorted(glob.glob(f"{D}/transcriptions_notelist/*.txt")):
    name = os.path.basename(f)[:-4]; y = YEAR.get(name)
    if y is None: continue
    ns = load(f)
    if len(ns) < 40: continue
    fr = [n["on"] - int(n["on"]) for n in ns]
    if np.mean([abs(x * 16 - round(x * 16)) < 1e-3 for x in fr]) < 0.98: continue   # not on a sixteenth grid: compound or triple
    per = period(y); used[per] += 1
    # words: a word starts at syllable index 1
    words = []; cur = []
    for i, n in enumerate(ns):
        if n["k"] == 1 and cur: words.append(cur); cur = []
        cur.append(i)
    if cur: words.append(cur)
    wid = {i: k for k, w in enumerate(words) for i in w}; nsyl = {i: len(words[wid[i]]) for i in wid}
    onsets = set(round(n["on"] * 16) for n in ns)
    for i, n in enumerate(ns):
        s = strength(n["on"] - int(n["on"]))
        if n["st"] == 0:
            R[(per, "weak on beat 1")]["yes" if s == 4 else "no"] += 1
            if nsyl[i] == 1: R[(per, "function words on beat 1")]["yes" if s == 4 else "no"] += 1
        else:
            if s == 1:
                nxt = round(n["on"] * 16) + 2
                R[(per, "stress on offbeat eighth")]["yes"] += 1
                R[(per, "of which anticipations")]["yes" if nxt not in onsets else "no"] += 1
            else: R[(per, "stress on offbeat eighth")]["no"] += 1
    for w in words:
        if len(w) < 2: continue
        sts = [ns[i]["st"] for i in w]
        if 1 not in sts or 0 not in sts: continue
        pp = ns[w[sts.index(1)]]["p"]; pu = np.mean([ns[i]["p"] for i, s in zip(w, sts) if s == 0])
        R[(per, "stress lower than its word")]["yes" if pp < pu else "no"] += 1
    for i in range(1, len(ns)):
        a, b = ns[i - 1], ns[i]
        if a["st"] == b["st"] or b["on"] - a["on"] > 1: continue
        pa, pb = strength(a["on"] - int(a["on"])), strength(b["on"] - int(b["on"]))
        if pa == pb: continue
        opp = (b["st"] == 1 and pb < pa) or (b["st"] == 0 and pb > pa)
        R[(per, "opposed inside words" if wid[i] == wid[i - 1] else "opposed across words")]["yes" if opp else "no"] += 1
out = {"songs_by_period": dict(used)}
for (per, k), c in sorted(R.items()):
    t = sum(c.values()); out.setdefault(k, {})[per] = dict(n=t, share=round(c["yes"] / t, 3))
json.dump(out, open(os.path.join(HERE, "pop20c_results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
