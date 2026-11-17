"""Melisma and grace notes in sung corpora. (1) MusicXML (PDMX English songs with words, by PDMX category, and OpenEWLD standards): for the
first part with 20 or more lyric syllables, voice 1, every syllable with all its notes' pitches (ties merged), whether a rest or the end
follows it (phrase end), whether it ends a word, its place in the song (thirds by syllable count), and grace notes per 100 notes.
(2) CoCoPops (Billboard 1958-91 and Rolling Stone 200), from ../words/sung_syllables.json: melisma counts, line ends, era.
Writes ornament_results.json."""
import os, re, sys, json, collections, statistics as st
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "words"))
from mxl_words import load_xml, strip_ns, STEP
def syllables(path):
    root = strip_ns(load_xml(path))
    for part in root.findall("part"):
        notes = []; grace = 0; total = 0; div = 1; nly = 0
        for meas in part.findall("measure"):
            for el in meas:
                if el.tag == "attributes":
                    d = el.find("divisions")
                    if d is not None: div = int(float(d.text))
                elif el.tag == "note":
                    v = el.find("voice"); v = v.text if v is not None else "1"
                    if v != "1" or el.find("chord") is not None: continue
                    if el.find("grace") is not None:
                        if el.find("pitch") is not None: grace += 1
                        continue
                    d = el.find("duration"); dur = int(float(d.text)) / div if d is not None else 0
                    if el.find("rest") is not None: notes.append(("rest", dur)); continue
                    p = el.find("pitch")
                    if p is None: continue
                    total += 1
                    midi = 12 * (int(p.find("octave").text) + 1) + STEP[p.find("step").text] + int(float(p.find("alter").text if p.find("alter") is not None else 0))
                    ties = [t.get("type") for t in el.findall("tie")]
                    ly = None
                    for l in el.findall("lyric"):
                        tx = l.find("text"); sy = l.find("syllabic")
                        if tx is not None and tx.text and re.search(r"[A-Za-z]", tx.text):
                            ly = (tx.text.strip(), sy.text if sy is not None else "single"); break
                    nly += ly is not None
                    notes.append(("note", midi, dur, ly, "stop" in ties))
        if nly >= 20: break
    else: return None
    sy = []
    for i, n in enumerate(notes):
        if n[0] == "rest":
            if sy: sy[-1]["end"] = True
            continue
        _, p, d, ly, tie = n
        if ly is None:
            if not sy: continue
            if tie and sy[-1]["ps"][-1] == p: sy[-1]["q"] += d; continue
            sy[-1]["ps"].append(p); sy[-1]["q"] += d; continue
        sy.append(dict(ps=[p], q=d, txt=ly[0], wend=ly[1] in ("single", "end"), end=False, punct=bool(re.search(r"[,.;:!?]$", ly[0]))))
    if sy: sy[-1]["end"] = True
    return sy, grace, total
def summarise_song(sy):
    n = len(sy); R = collections.Counter(); R["syl"] = n
    for i, s in enumerate(sy):
        k = len(s["ps"]); third = min(2, 3 * i // n); fin = s["end"] or s["punct"]
        R[f"syl third{third}"] += 1; R["phrase-end syl"] += fin; R["word-end syl"] += s["wend"]
        if k > 1:
            R["mel"] += 1; R[f"len{min(k, 5)}"] += 1; R[f"mel third{third}"] += 1; R["mel phrase-end"] += fin; R["mel word-end"] += s["wend"]
            iv = [b - a for a, b in zip(s["ps"], s["ps"][1:])]
            R["mel moves"] += len(iv); R["mel steps"] += sum(1 for x in iv if 0 < abs(x) <= 2); R["mel repeats"] += sum(1 for x in iv if x == 0)
            R["first down"] += iv[0] < 0; R["first up"] += iv[0] > 0; R["ends lower"] += s["ps"][-1] < s["ps"][0]
            R["mel notes"] += k
    return R
def work(a):
    path, cat = a
    try:
        r = syllables(path)
        if r is None: return None
        sy, grace, total = r
        from score_words import english
        if not english([dict(syl=("-" if False else "") + s["txt"] + ("" if s["wend"] else "-")) for s in sy]): return None
        R = summarise_song(sy); R["grace"] = grace; R["notes"] = total; R["songs"] = 1
        return cat, dict(R), R["mel"] / max(R["syl"], 1)
    except Exception: return None
def table(R, rates):
    s = R["syl"] or 1; m = R["mel"] or 1
    q = sorted(rates); med = st.median(q) if q else None
    return dict(songs=R["songs"], syllables=R["syl"], melisma_share=round(100 * R["mel"] / s, 1),
        song_median=round(100 * med, 1) if med is not None else None, song_q=[round(100 * q[int(.25 * (len(q) - 1))], 1), round(100 * q[int(.75 * (len(q) - 1))], 1)] if q else None,
        songs_none=round(100 * sum(1 for x in q if x == 0) / max(len(q), 1)),
        length={f"{k}": round(100 * R[f"len{k}"] / m) for k in (2, 3, 4, 5)},
        at_phrase_end=round(100 * R["mel phrase-end"] / m), phrase_end_base=round(100 * R["phrase-end syl"] / s),
        on_word_end=round(100 * R["mel word-end"] / m), word_end_base=round(100 * R["word-end syl"] / s),
        by_third=[round(100 * R[f"mel third{t}"] / max(R[f"syl third{t}"], 1), 1) for t in range(3)],
        steps=round(100 * R["mel steps"] / max(R["mel moves"], 1)), repeats=round(100 * R["mel repeats"] / max(R["mel moves"], 1)),
        first_down=round(100 * R["first down"] / m), first_up=round(100 * R["first up"] / m), ends_lower=round(100 * R["ends lower"] / m),
        grace_per_100=round(100 * R["grace"] / max(R["notes"], 1), 2) if R["notes"] else None)
if __name__ == "__main__":
    import pandas as pd
    from pdmx_words import selection
    D = "/home/claude/data/pdmx"
    d = selection()
    jobs = [(os.path.join(D, "x", p.lstrip("./")), c) for c, p in zip(d.cat, d.mxl) if os.path.exists(os.path.join(D, "x", p.lstrip("./")))]
    import glob
    jobs += [(f, "standards (OpenEWLD)") for f in glob.glob("/home/claude/data/openewld/OpenEWLD/dataset/*/*/*.mxl")]
    if len(sys.argv) > 1: jobs = jobs[:int(sys.argv[1])] + [j for j in jobs if j[1].startswith("standards")][:50]
    G = collections.defaultdict(collections.Counter); RT = collections.defaultdict(list)
    with Pool(2) as pool:
        for r in pool.imap_unordered(work, jobs, chunksize=20):
            if r is None: continue
            cat, R, rate = r; G[cat].update(R); RT[cat].append(rate)
    out = {c: table(G[c], RT[c]) for c in G}
    # CoCoPops
    S = json.load(open(os.path.join(HERE, "..", "words", "sung_syllables.json")))
    CG = collections.defaultdict(collections.Counter); CR = collections.defaultdict(list)
    for k, notes in S.items():
        m = re.search(r"_(\d{4})$", k); y = int(m.group(1)) if m else None
        corpus = "Billboard" if k.startswith("BB:") else "Rolling Stone 200"
        grp = [corpus] + ([f"Billboard {'1958-69' if y < 1970 else '1970-79' if y < 1980 else '1980-91'}"] if corpus == "Billboard" and y else []) + ([f"RS200 {'before 1980' if y < 1980 else '1980 and after'}"] if corpus != "Billboard" and y else [])
        sy = []
        for i, n in enumerate(notes):
            fin = i + 1 == len(notes) or notes[i + 1].get("line_start")
            sy.append(dict(ps=[0] * n.get("melisma", 1), q=n["q"], txt=n["syl"], wend=not n["syl"].endswith("-"), end=bool(fin), punct=False))
        if len(sy) < 20: continue
        R = summarise_song(sy); R["songs"] = 1
        for g in grp: CG[g].update(R); CR[g].append(R["mel"] / R["syl"])
    for g in CG:
        t = table(CG[g], CR[g]); [t.pop(x) for x in ("steps", "repeats", "first_down", "first_up", "ends_lower", "grace_per_100")]
        t["at_line_end"] = t.pop("at_phrase_end"); t["line_end_base"] = t.pop("phrase_end_base"); out["CoCoPops " + g] = t
    json.dump(out, open(os.path.join(HERE, "ornament_results.json"), "w"), indent=1)
    for k, v in out.items(): print(k, json.dumps(v))
