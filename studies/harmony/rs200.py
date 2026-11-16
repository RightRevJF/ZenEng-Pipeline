"""Harmony study, part 4: the second collection. The Rolling Stone 200 (de Clercq and Temperley 2011; 2013), one analyst's file (dt) per
song, read from ChoCo's raw copy: each section rule (Vr, Ch, Br, PC, In, Ou) expanded ($references, empty bars repeat the bar before,
'.' holds the chord), Roman numerals reduced to the same alphabet as the Billboard tables. Prints first and last chords, distinct chords,
changes a bar and the top bigrams by section kind, beside the Billboard figures (major songs)."""
import os, re, json, collections, statistics as st
D = "/home/claude/data/choco/smashub-choco-f7dd3ee/partitions/rock-corpus/raw/rs200_harmony"
KMAP = {"Vr": "verse", "Ch": "chorus", "Br": "bridge", "PC": "pre", "In": "intro", "Ou": "outro"}
def red(tok):
    t = tok.split("/")[0]
    m = re.match(r"^([b#]?)([IViv]+)(.*)$", t)
    if not m: return None
    acc, num, q = m.groups(); minor = num.islower()
    deg = acc + num.upper()
    if "o" in q or "h" in q: return deg.lower() + "o" if not acc else acc + num.lower() + "o"
    return (acc + num.lower()) if minor else deg
def expand(rules, name, depth=0):
    if depth > 8 or name not in rules: return []
    out = []
    for part in rules[name].split():
        if part.startswith("$"): out += expand(rules, part[1:].split("*")[0], depth + 1) * (int(part.split("*")[1]) if "*" in part else 1)
        else: out.append(part)
    return out
res = collections.defaultdict(lambda: collections.defaultdict(list)); BIG = collections.defaultdict(collections.Counter)
for fn in sorted(os.listdir(D)):
    if not fn.endswith("_dt.har"): continue
    rules = {}
    for line in open(f"{D}/{fn}", errors="ignore"):
        line = line.split("%")[0].strip()
        m = re.match(r"^([A-Za-z0-9]+):\s*(.*)$", line)
        if m: rules[m.group(1)] = m.group(2)
    for name, body in rules.items():
        k = KMAP.get(re.sub(r"\d+$", "", name))
        if not k: continue
        toks = expand(rules, name); bars, cur, prevbar = [], [], None
        for t in toks + ["|"]:
            if t == "|":
                if cur: bars.append(cur); prevbar = cur
                elif prevbar is not None and bars: bars.append(prevbar)
                cur = []
            elif t.startswith("[") or t == "R": continue
            else: cur.append(t)
        ch, last = [], None
        for b in bars:
            for t in b:
                x = last if t == "." else red(t)
                if t != ".": last = x
                if x and (not ch or ch[-1] != x): ch.append(x)
        if len(bars) < 2 or not ch: continue
        R = res[k]; R["first"].append(ch[0]); R["last"].append(ch[-1]); R["distinct"].append(len(set(ch))); R["cpb"].append(len(ch) / len(bars))
        for a, b in zip(ch, ch[1:]): BIG[k][(a, b)] += 1
BB = json.load(open("billboard_tables.json"))["by_section"]
out = {}
for k in ("verse", "chorus", "bridge", "pre", "intro", "outro"):
    R = res[k]; n = len(R["first"])
    if n < 10: continue
    top = lambda c, m=6: [[x, round(v / sum(c.values()), 3)] for x, v in c.most_common(m)]
    out[k] = dict(n=n, first=top(collections.Counter(R["first"])), last=top(collections.Counter(R["last"])), distinct=st.median(R["distinct"]),
                  changes_a_bar=round(st.median(R["cpb"]), 3), bigrams=[[" ".join(a), b] for a, b in top(BIG[k], 8)])
    b = BB.get(f"{k} (major)", {})
    print(f"== {k}: RS200 n={n} first {out[k]['first'][:4]} | Billboard {b.get('first', [])[:4]}")
    print(f"   last {out[k]['last'][:4]} | Billboard {b.get('last', [])[:4]}")
    print(f"   distinct {out[k]['distinct']} vs {b.get('distinct')}; changes a bar {out[k]['changes_a_bar']} vs {b.get('changes_a_bar')}")
    print(f"   bigrams {out[k]['bigrams'][:6]}")
json.dump(out, open("rs200_tables.json", "w"), indent=1)
