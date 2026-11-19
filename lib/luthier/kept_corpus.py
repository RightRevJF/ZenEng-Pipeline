"""895 (749.70): the kept corpus, read from inside the repo. The kept songs are the CoCoPops Billboard songs in 4/4 named in tables/kept_songs_4-4_pop.json
(CoCoPops: github.com/Computational-Cognitive-Musicology-Lab/CoCoPops, CC BY 4.0; not committed here). To fetch and parse it:
    git clone https://github.com/Computational-Cognitive-Musicology-Lab/CoCoPops corpora/CoCoPops
    python3 lib/luthier/cocopops_parse.py corpora/CoCoPops/Billboard/Data          # writes cocopops_notes.csv.gz; move it to corpora/
The notes table is looked for at $LUTHIER_COCOPOPS_NOTES, then corpora/cocopops_notes.csv.gz. A maker that cannot find it says so and stops."""
import os, sys, json, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
def notes_path():
    for p in (os.environ.get("LUTHIER_COCOPOPS_NOTES"), os.path.join(ROOT, "corpora", "cocopops_notes.csv.gz")):
        if p and os.path.exists(p): return p
    raise SystemExit("the kept corpus is not here: set LUTHIER_COCOPOPS_NOTES or put cocopops_notes.csv.gz in corpora/ (see lib/luthier/kept_corpus.py)")
def table():
    import pandas as pd
    d = pd.read_csv(notes_path(), low_memory=False); return d[(d.dur > 0) & (d.lead == "voice")]
def kept_songs(min_notes=150):
    """each kept song: onsets and lengths in twelfths of a quarter, pitches, the words as (word, syllables sung), a line number for each note (lines split at
    onsets a half note apart), section labels, and the chart record"""
    K = set(json.load(open(os.path.join(ROOT, "tables", "kept_songs_4-4_pop.json"))))
    for s, g in table().groupby("song", sort=False):
        if str(s) not in K: continue
        g = g.sort_values("abs_beat")
        if len(g) < min_notes: continue
        t = np.round((g.bar.values * 4.0 + g.beat.values) * 12).astype(int); du = np.round(g.dur.values * 12).astype(int); p = g.pitch.values.astype(int); syl = [str(x) if x == x else "" for x in g.syl.values]
        words = []; cur = ""; n = 0; lines = []; line = 0
        for i, sx in enumerate(syl):
            if i and t[i] - t[i - 1] >= 24: line += 1
            lines.append(line); x = sx.strip(); cont = x.endswith("-"); cur += re.sub(r"[^A-Za-z']", "", x); n += 1
            if not cont: words.append((cur, n)); cur = ""; n = 0
        if n: words.append((cur, n))
        try: weeks = float(g.weeks.iloc[0]); peak = float(g.peak.iloc[0])
        except Exception: weeks = peak = float("nan")
        yield dict(song=str(s), t=t, dur=du, p=p, words=words, lines=lines, sec=g.section.astype(str).values, weeks=weeks, peak=peak, year=int(g.year.iloc[0]) if str(g.year.iloc[0]).isdigit() else None)
