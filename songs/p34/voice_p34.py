"""Swallowed Up -- the harsh voice placed over the frozen riffs (ZenEng v78, 9-M.7). No pitch: a harsh line has rhythm, a register
and a vowel shape, and it is not searched as melody (9-M.10a). Each line takes two bars; its strokes lock to the guitar's accents and
the beats; a growled phrase ends with a breath before its riff cycle ends (the cap of two bars: DEFAULT).
  Families and registers: the verses GROWL, low; the choruses and the taunt SHOUT, mid (the intelligibility budget: the title,
  the hook and the taunt go to the voice that can be understood, repeated and printed); the last 'Swallowed up!' a FRY SCREAM, high
  (the contrasting colour as a climactic tag).
  Vowel shape (Smialek et al. 2012): a low growl darkens its stressed vowels toward back vowels, opens at the emphatic word and
  darkens at the line's end; the mid shout keeps the words' own vowels (to be understood); the high scream brightens.
  Stress: fix 140 (v78, 28.12): a compound the dictionary double-stresses takes one stress (Sunday, backhoe, everything); two song
  readings: 'like' as a preposition and 'you'll' are weak."""
import sys, re, pickle, hashlib, json
sys.path[:0] = ["/home/claude/p34", "/home/claude/carol", "/home/claude/pop"]
import engine_p34 as E, phrasestress48 as PS; PS.install(E); E.install_patches()
import lyric as L
import riffs_p34 as R

COMPOUND_140 = {"sunday", "backhoe", "everything", "somebody", "anybody", "nobody", "everybody", "clothesline"}
WEAK_34 = {"like", "you'll"}
def syl_line(line):
    s = E.syllables(line); out = []; seen = {}
    for k, (w, v, st, fn) in enumerate(s):
        wl = w.lower(); j = seen.get((wl, k - 1), 0) if False else None
        out.append([wl, v, st, fn])
    # one stress per fix-140 compound: keep the first stressed syllable of each run of the same word
    for k in range(len(out)):
        if out[k][0] in COMPOUND_140 and k > 0 and out[k - 1][0] == out[k][0] and out[k][2]:
            if any(out[j][2] for j in range(k - 1, -1, -1) if out[j][0] == out[k][0]): out[k][2] = False
        if out[k][0] in WEAK_34: out[k][2] = False
    return out

# the words with their punctuation, to find the sentence breaks inside a line
def words_of(line): return line.split()

FAMILY = {"verse": ("growl", "low"), "chorus": ("shout", "mid"), "hook": ("shout", "mid"), "taunt": ("shout", "mid")}
DARK = {"IY": "UW", "IH": "UH", "EY": "OW", "EH": "AO", "AE": "AA", "AH": "AO", "AY": "AA", "ER": "ER", "AW": "AW", "OY": "OY",
        "UW": "UW", "UH": "UH", "OW": "OW", "AO": "AO", "AA": "AA"}
BRIGHT = {"AH": "AE", "UW": "IY", "UH": "IH", "OW": "EY", "AO": "AE", "AA": "AE"}

# where each section's lines go: (section, line index) -> (first bar index into R.BARS)
def line_bars():
    out = {}
    for sec, ls in L.SECTIONS:
        b0 = R.SEC_FIRST[sec]
        if sec == "Slowdown":
            starts = [b0, b0 + 4, b0 + 8, b0 + 12]
        else:
            starts = [b0 + 2 * i for i in range(len(ls))]
        for i, b in enumerate(starts): out[(sec, i)] = b
    return out
LB = line_bars()

def accents(b):
    """the guitar's unmuted stroke onsets in bar b (16ths), and in the next bar offset by 16."""
    a = set()
    for k in (0, 1):
        if b + k < len(R.BARS):
            for s, d, o, pm in R.BARS[b + k]["strokes"]:
                if not pm: a.add(s + 16 * k)
    return a

def place(sec, i, role, line):
    syl = syl_line(line); n = len(syl)
    b = LB[(sec, i)]; acc = accents(b)
    fam, reg = FAMILY[role]
    if sec == "Last Chorus" and i == 3: fam, reg = "scream", "high"
    shout = fam in ("shout", "scream")
    # sentence breaks inside the line: after a word ending in . : ! ? (not the last)
    ws = words_of(line); brk = set(); k = 0
    for w in ws:
        m = len(E.syllables(w)); k += m
        if re.search(r"[.:!?]['\"”]?$", w) and k < n: brk.add(k - 1)
    word_id = []; k = 0
    for wi, w in enumerate(ws):
        for _ in range(len(E.syllables(w))): word_id.append(wi)
    brk_riff = R.BARS[b]["riff"] == "F"                        # the breakdown: lock to its unison strokes
    def sc_pos(j, p):
        st = syl[j][2]
        if st and brk_riff: return 4.0 if p in acc else (-0.5 if p % 2 == 0 else -2.0)
        if st:
            if p in acc: return 3.0 + (1.0 if p % 16 == 0 else 0)
            if p % 4 == 0: return 2.0
            if p % 2 == 0: return 0.8
            return -2.0
        return (0.0 if p % 2 == 0 else -0.6) - (1.0 if p % 16 == 0 and j > 0 else 0)
    def sc_gap(j, g):
        same = word_id[j] == word_id[j + 1]
        if j in brk: return {1: -9, 2: -3, 3: -1, 4: 0.3, 6: 0.3, 8: -0.2}.get(g, -9)
        pref = 4 if shout else 2
        if brk_riff: return {1: -2, 2: -0.4, 3: 0.0, 4: 0.0, 6: -0.4, 8: -1.0}.get(g, -9)
        tbl = {2: {1: -0.8, 2: 0.0, 3: -0.6, 4: -0.3, 6: -1.2, 8: -2.0}, 4: {1: -3, 2: -0.6, 3: -1.0, 4: 0.0, 6: -0.6, 8: -1.0}}[pref]
        return tbl.get(g, -9)
    GAPS = (1, 2, 3, 4, 6, 8)
    best = {}
    for p0 in range(0, 7):
        if p0 % 2: continue
        best[(0, p0)] = (sc_pos(0, p0) - 0.4 * (p0 // 2), [p0])
    for j in range(n - 1):
        nxt = {}
        for (jj, p), (sc, path) in best.items():
            if jj != j: continue
            for g in GAPS:
                q = p + g
                if q > 28: continue
                v = sc + sc_gap(j, g) + sc_pos(j + 1, q)
                if (j + 1, q) not in nxt or v > nxt[(j + 1, q)][0]: nxt[(j + 1, q)] = (v, path + [q])
        best.update(nxt)
    ends = [(sc, path) for (jj, p), (sc, path) in best.items() if jj == n - 1]
    sc, path = max(ends, key=lambda x: (x[0], -x[1][-1]))
    # durations: to the next syllable; the last held to the next accent or four sixteenths, a breath of at least two before the cycle ends
    durs = [path[j + 1] - path[j] for j in range(n - 1)]
    last = path[-1]; nxt_acc = [a for a in sorted(acc) if a > last]
    dl = min(max(4 if shout else 2, (nxt_acc[0] - last) if nxt_acc else 4), 8 if shout else 6, 30 - last)
    durs.append(max(1, dl))
    # vowel shape
    stressed = [j for j in range(n) if syl[j][2]]
    lastst = stressed[-1] if stressed else n - 1
    rank = lambda p: (2 if p % 16 == 0 else 0) + (1 if p in acc else 0)
    content = [j for j in stressed if j != lastst and not syl[j][3]]
    emph = max(content, key=lambda j: (rank(path[j]), -j)) if content else None
    ev = []
    for j in range(n):
        w, v, st, fn = syl[j]; v0 = re.sub(r"\d", "", v)
        if fam == "growl" and st:
            tgt = "AA" if j == emph else (("UW" if v0 in ("IY", "IH", "UW", "UH") else "OW") if j == lastst else DARK.get(v0, v0))
        elif fam == "scream" and st: tgt = BRIGHT.get(v0, v0)
        else: tgt = v0
        p = path[j]
        ev.append(dict(sec=sec, line=i, j=j, bar=b + p // 16, slot=p % 16, abs16=b * 16 + p, dur=durs[j], word=w, stressed=st,
                       family=fam, height=reg, vowel_src=v0, vowel=tgt, emphatic=(j == emph), line_end=(j == lastst)))
    lock = sum(1 for j in stressed if path[j] in acc or path[j] % 4 == 0) / max(1, len(stressed))
    return ev, dict(sec=sec, line=i, score=round(sc, 2), lock=round(lock, 2), first_bar=b + 1, family=fam, height=reg,
                    emphatic=(syl[emph][0] if emph is not None else None), end=path[-1] + durs[-1])

if __name__ == "__main__":
    allv, rep = [], []
    for sec, ls in L.SECTIONS:
        for i, (role, line) in enumerate(ls):
            ev, r = place(sec, i, role, line); allv += ev; rep.append(r)
    # checks: a breath before the two-bar cycle ends; no overlaps; every stressed syllable on a beat or an accent (the lock)
    for r in rep: assert r["end"] <= 30, r
    allv.sort(key=lambda e: e["abs16"])
    for a, b in zip(allv, allv[1:]): assert a["abs16"] + a["dur"] <= b["abs16"], (a, b)
    lock = sum(1 for e in allv if e["stressed"] and (e["slot"] % 4 == 0 or e["slot"] in accents(e["bar"])) ) / sum(1 for e in allv if e["stressed"])
    sha = hashlib.sha1(json.dumps([(e["abs16"], e["dur"], e["word"]) for e in allv]).encode()).hexdigest()[:12]
    pickle.dump(dict(voice=allv, lines=rep, lock=lock, sha=sha, riffs_sha=pickle.load(open("/home/claude/p34/riffs_frozen.pkl", "rb"))["sha"]),
                open("/home/claude/p34/voice.pkl", "wb"))
    print(f"{len(allv)} strokes; stressed on a beat or accent: {lock:.2f}; voice {sha}")
    for r in rep: print(f"  {r['sec']:12s} {r['line']} bar {r['first_bar']:3d} {r['family']:6s} {r['height']:4s} lock {r['lock']:.2f} emph {r['emphatic']}")
    for sec, i in (("Verse 1", 0), ("Verse 1", 2), ("Chorus 1", 0), ("Chorus 1", 1), ("Slowdown", 0), ("Verse 3", 4)):
        print(sec, i, " ".join(f"{e['word']}@{(e['abs16'] - LB[(sec, i)]*16)}/{e['dur']}{'*' if e['stressed'] else ''}{'['+e['vowel']+']' if e['stressed'] else ''}" for e in allv if e["sec"] == sec and e["line"] == i))
