"""Songs 52 to 56 on the lyric measures (lyrics_features.py), placed as percentiles of the Rolling Stone greatest-list songs (RS) and
the Billboard sample (BB), 1958-1991. Songs 52, 54, 55 and 56 are read as sung from their records and segmented by the same rule;
song 53 is read from its locked lyric, stanzas as written. Only derived numbers are written."""
import json, pickle, re, sys
import numpy as np
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/lyrics"); sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/hooks")
import lyrics_features as LF
import hooks_our_titles as OT
S = "/home/claude/zeneng-pipeline/songs/"
def from_events(events, tpq):
    ws = []; join = False
    for e in sorted(events, key=lambda e: e["on"]):
        line = (e["sec"], e["line"]); on = e["on"] / tpq; end = (e["on"] + e["dur"]) / tpq
        if ws and ws[-1]["line"] == line and (join or (e.get("same_word"))):
            ws[-1]["text"] += ("" if e.get("same_word") else LF.norm(e["text"])); ws[-1]["end"] = end
        else:
            ws.append(dict(text=LF.norm(e["text"]), on=on, end=end, sec=e["sec"], line=line))
        join = bool(e.get("hyph"))
    return LF.segment(ws)
songs = []
for folder, num, title, tpq in (("p64", 54, "The Man Mama Prayed I'd Be", 12), ("p65", 55, "Your Yard Man", 12), ("p66", 56, "Terpsichore", 24)):
    r = pickle.load(open(S + folder + "/song_record.pkl", "rb")); songs.append((num, title, from_events(r["lead"], tpq)))
m = json.load(open(S + "p62/melody_varied.json"))["pick"]["notes"]; ev = []
for n in sorted(m, key=lambda n: n["on"]):
    same = bool(ev) and ev[-1]["text"] == n["text"] and ev[-1]["line"] == n["line"] and ev[-1]["sec"] == n["sec"]
    ev.append(dict(on=n["on"], dur=n["dur"], sec=n["sec"], line=n["line"], text=n["text"], same_word=same))
songs.append((52, "The Room Next Door", from_events(ev, 12)))
locked = open(S + "p63/lyric_locked.md").read()
lines53 = [l.strip() for l in locked.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("**") and not l.startswith("|")]
songs.append((53, "Sung to Sleep", lines53))
R = json.load(open("/home/claude/zeneng-pipeline/studies/lyrics/lyrics_rows_scored.json"))
F = ["words_per_line", "mattr", "repeated_lines", "zipf", "rare", "you", "i", "third", "conc", "past", "time", "place", "propn", "valence_sd", "ending", "absolutes", "rhyme", "title_n"]
out = []
for num, title, lines in sorted(songs):
    f = LF.features(lines, title); row = dict(song=num, title=title, **{k: f[k] for k in F})
    for g in ("RS", "BB"):
        for k in F:
            v = np.array([x[k] for x in R if x["group"] == g and x.get(k) is not None], float)
            if f[k] is not None: row[f"{k}_pct_{g}"] = round(float(((v < f[k]).mean() + 0.5 * (v == f[k]).mean()) * 100), 1)
    out.append(row)
json.dump(out, open("/home/claude/zeneng-pipeline/studies/lyrics/lyrics_our_songs.json", "w"), indent=1)
for r in out:
    print(r["song"], " ".join("%s=%.3f(RS%.0f/BB%.0f)" % (k, r[k], r.get(k + "_pct_RS", -1), r.get(k + "_pct_BB", -1)) for k in ("repeated_lines", "rare", "valence_sd", "absolutes", "you", "conc", "zipf", "mattr", "title_n") if r[k] is not None))
