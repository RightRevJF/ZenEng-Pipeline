"""Word setting in OpenEWLD (public-domain Wikifonia lead sheets: standards and popular songs, mostly 1900-1950s), English only,
lyrics attached to notes in the MusicXML. Measures from score_words.py; first-performance decade from the database."""
import sqlite3, os, json, collections
from mxl_words import song_notes
from score_words import measure, summarise
D = "/home/claude/data/openewld/OpenEWLD"; HERE = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(f"{D}/OpenEWLD.db")
R = collections.defaultdict(collections.Counter); n = collections.Counter()
for title, date, lang, path in db.execute("select title, first_performance_date, language, path_leadsheet from works"):
    if lang and lang.lower() not in ("english", "en", "eng"): continue
    p = os.path.join(D, path) if not os.path.isabs(path) else path
    if not os.path.exists(p): continue
    try: ns = song_notes(p)
    except Exception: n["parse error"] += 1; continue
    yr = int(str(date)[:4]) if date and str(date)[:4].isdigit() else None
    cat = "standards before 1930" if yr and yr < 1930 else "standards 1930 on" if yr else "standards, date unknown"
    n["used" if measure(ns, cat, R) else "skipped"] += 1
out = summarise(R); out["counts"] = dict(n)
json.dump(out, open(os.path.join(HERE, "openewld_words_results.json"), "w"), indent=1)
print(json.dumps(out, indent=1)[:6000])
