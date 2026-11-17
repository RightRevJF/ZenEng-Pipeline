"""Word setting in BiMMuDa (Hamilton and Pearce; the top five Billboard year-end singles, 1950-2022; melodies as MIDI per section and
lyrics as text, not aligned). Alignment by exact count: a section MIDI is paired with a lyric stanza (blank-line separated) whose
syllable count (CMU dictionary, every word found) equals the section's note count exactly, and syllables are then laid on notes in
order. Only exact matches are used, so the sample is small but the alignment is one-to-one. 4/4 songs only (metadata), positions
from the MIDI's own bars (MuseScore export, bar 1 at time 0). Measures as words_test.py and words_more.py, by period.
Fetch: git clone --depth 1 https://github.com/madelinehamilton/BiMMuDa.git into /home/claude/data/bimmuda (derived counts only)."""
import glob, os, re, csv, json, collections, numpy as np, mido, pronouncing
from words_test import FUNC, vclass
HERE = os.path.dirname(os.path.abspath(__file__)); D = "/home/claude/data/bimmuda/BiMMuDa"
VOICED = {"B", "D", "G", "V", "DH", "Z", "ZH", "JH"}; VOICELESS = {"P", "T", "K", "F", "TH", "S", "SH", "CH"}
META = {}
for r in csv.DictReader(open(f"{D}/metadata/bimmuda_per_song_metadata.csv", encoding="utf-8", errors="replace")):
    try: META[(int(r["Year"]), int(r["Position"]))] = r
    except (ValueError, KeyError): pass
def pron(word):
    w = re.sub(r"[^a-z']", "", word.lower())
    for c in (w, w.replace("'", ""), re.sub(r"in'$", "ing", w)):
        ph = pronouncing.phones_for_word(c)
        if ph: return ph[0].split()
    return None
def syllables(block):
    out = []
    toks = []
    for line in block.split("\n"):
        ws = [w for w in line.split() if re.search(r"[A-Za-z]", w)]
        for j, w in enumerate(ws): toks.append((w, j == len(ws) - 1))
    for word, eol in toks:
        if not re.search(r"[A-Za-z]", word): continue
        p = pron(word)
        if p is None: return None
        vs = [(re.sub(r"\d", "", x), int(x[-1])) for x in p if x[-1].isdigit()]
        last = re.sub(r"\d", "", p[-1])
        w = re.sub(r"[^a-z']", "", word.lower()).strip("'")
        for k, (v, st) in enumerate(vs):
            if len(vs) == 1: st = 0 if w in FUNC else 1
            out.append(dict(word=w, k=k, n=len(vs), st=1 if st > 0 else 0, v=vclass(v, st > 0), last=last if k == len(vs) - 1 else None,
                            eol=eol and k == len(vs) - 1))
    return out
def notes_of(path):
    m = mido.MidiFile(path); tpb = m.ticks_per_beat; ons = []
    for tr in m.tracks:
        t = 0; open_ = {}
        for msg in tr:
            t += msg.time
            if msg.type == "note_on" and msg.velocity > 0: open_[msg.note] = t; ons.append([t, None, msg.note])
            elif msg.type in ("note_off", "note_on") and msg.note in open_:
                for o in reversed(ons):
                    if o[2] == msg.note and o[1] is None: o[1] = t; break
                open_.pop(msg.note, None)
    ons.sort()
    return [dict(beat=o[0] / tpb, q=((o[1] or o[0] + tpb) - o[0]) / tpb, p=o[2]) for o in ons]
def strength(beat):
    f = (beat % 4)
    if abs(f) < 1e-3: return 4
    if abs(f - 2) < 1e-3: return 3
    if abs(f - round(f)) < 1e-3: return 2
    if abs(f * 2 - round(f * 2)) < 1e-3: return 1
    return 0
def period(y): return "1950-1979" if y < 1980 else "1980-1999" if y < 2000 else "2000-2022"
R = collections.defaultdict(collections.Counter); used = collections.Counter(); secs = collections.Counter()
for d in sorted(glob.glob(f"{D}/bimmuda_dataset/*/*")):
    try: y = int(os.path.basename(os.path.dirname(d))); pos = int(os.path.basename(d))
    except ValueError: continue
    meta = META.get((y, pos), {})
    if meta.get("Time Signature 1") != "4/4" or meta.get("Time Signature 2"): continue
    ly = glob.glob(d + "/*_lyrics.txt")
    if not ly: continue
    blocks = [b for b in re.split(r"\n\s*\n", open(ly[0], encoding="utf-8", errors="replace").read()) if b.strip()]
    sb = [syllables(b) for b in blocks]
    got = False
    for sec in sorted(glob.glob(d + "/*_[0-9].mid")):
        ns = notes_of(sec)
        match = next((s for s in sb if s and len(s) == len(ns)), None)
        if not match or len(ns) < 12: continue
        for n, s in zip(ns, match): n.update(s)
        # alignment check independent of stress: lyric line ends should fall on long notes or before gaps (phrase-final lengthening)
        ioi = [b["beat"] - a["beat"] for a, b in zip(ns, ns[1:])] + [4.0]
        fin = [x for x, n in zip(ioi, ns) if n["eol"]]; oth = [x for x, n in zip(ioi, ns) if not n["eol"]]
        ratio = (np.mean(fin) / np.mean(oth)) if fin and oth else 0
        R[("all", "alignment ratio")]["kept" if ratio >= 1.5 else "dropped"] += 1
        if ratio < 1.5: continue
        got = True; per = period(y); secs[per] += 1
        med = np.median([n["q"] for n in ns])
        wid = []; k = -1
        for n in ns:
            if n["k"] == 0: k += 1
            wid.append(k)
        for i, n in enumerate(ns):
            st = strength(n["beat"])
            if n["st"] == 0:
                R[(per, "weak on beat 1")]["yes" if st == 4 else "no"] += 1
                if n["n"] == 1: R[(per, "function words on beat 1")]["yes" if st == 4 else "no"] += 1
            if n["n"] == 1 and n["st"] == 1 and n["last"] and i + 1 < len(ns):
                if n["last"] in VOICED: R[(per, "voiced ending long")]["yes" if n["q"] > med else "no"] += 1
                if n["last"] in VOICELESS: R[(per, "voiceless ending long")]["yes" if n["q"] > med else "no"] += 1
            if i:
                a = ns[i - 1]; sa, sb_ = strength(a["beat"]), st
                if a["st"] != n["st"] and sa != sb_ and n["beat"] - a["beat"] <= 4:
                    opp = (n["st"] == 1 and sb_ < sa) or (n["st"] == 0 and sb_ > sa)
                    R[(per, "opposed inside words" if wid[i] == wid[i - 1] else "opposed across words")]["yes" if opp else "no"] += 1
        words = collections.defaultdict(list)
        for i, n in enumerate(ns): words[wid[i]].append(n)
        for w in words.values():
            if len(w) < 2 or 1 not in [x["st"] for x in w] or 0 not in [x["st"] for x in w]: continue
            pp = next(x["p"] for x in w if x["st"] == 1); pu = np.mean([x["p"] for x in w if x["st"] == 0])
            R[(per, "stress lower than its word")]["yes" if pp < pu else "no"] += 1
    if got: used[period(y)] += 1
out = {"songs": dict(used), "sections": dict(secs)}
for (per, k), c in sorted(R.items()):
    t = sum(c.values()); out.setdefault(k, {})[per] = dict(n=t, share=round(c["yes"] / t, 3))
json.dump(out, open(os.path.join(HERE, "bimmuda_words_results.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
