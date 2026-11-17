"""The title in songs 52, 54, 55 and 56, read the way hooks_titles.py reads CoCoPops: times sung, choruses that carry it, first or
last line of the chorus, first heard (seconds, share of the song). Song 53's soprano line carries no syllables in its record and is
read from its lyric layout instead (not here)."""
import json, pickle, re, collections
import numpy as np
SONGS = "/home/claude/zeneng-pipeline/songs/"
def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())
def words_from(events):
    """Syllables are joined into words where the record marks a hyphen (hyph) after a syllable; song 52's record repeats the
    whole word on each syllable, so a repeated text on consecutive syllables is one word."""
    W = []; join = False
    for e in events:
        tx = norm(e["text"]); line = (e["sec"], e["line"])
        if W and W[-1]["line"] == line and (join or (tx == W[-1]["text"] and e.get("syl", 0) > 0 and e.get("same_word"))):
            if join: W[-1]["text"] += tx
        else:
            W.append(dict(text=tx, sec=e["sec"], line=line, on=e["on"]))
        join = bool(e.get("hyph"))
    return W
def study(title, events, tpq, qbpm):
    t = [norm(x) for x in title.split()]; W = words_from(sorted(events, key=lambda e: e["on"])); T = [w["text"] for w in W]
    hits = [i for i in range(len(T) - len(t) + 1) if T[i:i + len(t)] == t]
    secs = collections.OrderedDict()
    for w in W: secs.setdefault(w["sec"], []).append(w)
    ch = []
    for s, ws in secs.items():
        if "chorus" not in s.lower(): continue
        lines = sorted({w["line"] for w in ws}, key=lambda l: l[1]); tl = {W[i]["line"] for i in hits if W[i]["sec"] == s}
        ch.append(dict(section=s, n_lines=len(lines), n_title=sum(1 for i in hits if W[i]["sec"] == s), first_line=lines[0] in tl, last_line=lines[-1] in tl))
    end = max(e["on"] + e["dur"] for e in events)
    first = W[hits[0]]["on"] if hits else None
    # the chorus's most repeated two- to four-word phrase (the hook phrase), counted in the first chorus
    c1 = [w["text"] for w in W if w["sec"] == next((s for s in secs if "chorus" in s.lower()), None)]
    best = (0, 0)
    for n in (4, 3, 2):
        cnt = collections.Counter(tuple(c1[i:i + n]) for i in range(len(c1) - n + 1))
        if cnt:
            g, k = cnt.most_common(1)[0]
            if k >= 2 and k * n > best[0] * best[1]: best = (k, n)
    return dict(title=title, sung=len(hits), hook_phrase_repeats_in_chorus1=best[0], hook_phrase_words=best[1], choruses=ch, first_seconds=round(first / tpq * 60 / qbpm, 1) if first is not None else None,
                first_share=round(first / end, 3) if first is not None else None, in_verse=sum(1 for i in hits if "verse" in W[i]["sec"].lower()))
out = []
for folder, title, tpq in (("p64", "The Man Mama Prayed I'd Be", 12), ("p65", "Your Yard Man", 12), ("p66", "Terpsichore", 24)):
    r = pickle.load(open(SONGS + folder + "/song_record.pkl", "rb")); out.append(study(title, r["lead"], tpq, r["qbpm"] if isinstance(r["qbpm"], (int, float)) else 72))
m = json.load(open(SONGS + "p62/melody_varied.json"))["pick"]["notes"]
ev = []
for n in sorted(m, key=lambda n: n["on"]):
    same = bool(ev) and ev[-1]["text"] == n["text"] and ev[-1]["line"] == n["line"] and ev[-1]["sec"] == n["sec"]
    ev.append(dict(on=n["on"], dur=n["dur"], sec=n["sec"], line=n["line"], syl=n["syl"], text=n["text"], same_word=same))
out.append(study("The Room Next Door", ev, 12, 81))
json.dump(out, open("/home/claude/zeneng-pipeline/studies/hooks/hooks_our_titles.json", "w"), indent=1)
for o in out: print(json.dumps(o))
