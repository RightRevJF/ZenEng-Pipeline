"""Run 09: parse the ChoCo v1.0.0 partitions that run 08 left unparsed (Zenodo 7706751; CC BY 4.0) into a chart cache, NOTES ONLY.
Same chart format as run 08's parse_choco.py: per chart id, part, title, artists (performer or composer string, as given), names_kind
("performer", "composer" or "" when the partition gives none), source ("recording" = transcribed from one recording; "chart" = a
fake-book / Band-in-a-Box chart), key, chords [time, dur, root_pc, bitmap12, bass_pc].

Partitions (Billboard and Chordify are left out: Billboard is the McGill hold-out's source and Chordify's songs are Billboard ids;
RWC-Pop's songs were written for the database; Mozart, Schubert, When in Rome and Nottingham are classical or folk with no recordings
to match; the Weimar partition's chords are the changes a soloist played over, so it counts as "recording"):
  biab-internet-corpus  4,989 Band-in-a-Box files, titles only           -> source chart, names ""
  real-book             2,846 Band-in-a-Box Real Book files, 609 with names -> source chart, names composer when given
  isophonics, uspop2002, rock-corpus, robbie-williams                    -> source recording, names performer
  jaah (track performer), weimar (performer; composers also kept)        -> source recording
Output: /home/claude/dl/choco/charts_run09.json (outside the repo).
"""
import json, csv, os
import mir_eval.chord as mc
R = "/home/claude/dl/choco/smashub-choco-f7dd3ee/partitions"
PC = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def pc(n):
    v = PC[n[0]]
    for ch in n[1:]:
        v += 1 if ch == '#' else -1 if ch == 'b' else 0
    return v % 12
out = []; bad = 0; missing = 0
def jpath(part, jid):
    for d in ("jams-converted", "jams"):
        p = os.path.join(R, part, "choco", d, jid if jid.endswith(".jams") else jid + ".jams")
        if os.path.exists(p): return p
    return None
def load(part, title_k, art_k, kind, source, comp_k=None):
    global bad, missing
    for r in csv.DictReader(open(os.path.join(R, part, "choco", "meta.csv"))):
        p = jpath(part, r["id"])
        if p is None: missing += 1; continue
        d = json.load(open(p)); ch = []; key = None
        anns = d["annotations"]; nss = [a["namespace"] for a in anns]
        use = "chord_harte" if "chord_harte" in nss else "chord"
        for a in anns:
            if a["namespace"] == use and not ch:
                for o in a["data"]:
                    v = o["value"]
                    if v in ("N", "X", None) or not isinstance(v, str): continue
                    root = None
                    for vv in (v, v.replace("113", "13"), v.split("(")[0]):
                        try:
                            root, bm, bass = mc.encode(vv); break
                        except Exception:
                            root = None
                    if root is None:
                        bad += 1; continue
                    if root < 0: continue
                    ch.append([round(o["time"], 3), round(o["duration"], 3), int(root), [int(x) for x in bm], int((root + bass) % 12)])
            if a["namespace"] == "key_mode" and a["data"] and key is None:
                v = a["data"][0]["value"]
                try:
                    t, m = v.split(":"); key = [pc(t), m]
                except Exception:
                    key = None
        names = (r.get(art_k) or "").strip() if art_k else ""
        out.append(dict(id=r["id"].replace(".jams", ""), part=part, title=(r.get(title_k) or "").strip(), artists=names,
                        names_kind=(kind if names else ""), source=source, composers=(r.get(comp_k) or "").strip() if comp_k else "",
                        genre="", key=key, chords=ch, timebase=("beats" if source == "chart" or part == "rock-corpus" else "seconds")))
load("biab-internet-corpus", "score_title", None, "", "chart")
load("real-book", "file_title", "file_artists", "composer", "chart")
load("isophonics", "file_title", "file_performer", "performer", "recording")
load("uspop2002", "file_title", "file_performer", "performer", "recording")
load("rock-corpus", "title", "performers", "performer", "recording")
load("robbie-williams", "file_title", "file_performer", "performer", "recording")
load("jaah", "track_title", "track_performer", "performer", "recording")
load("weimar", "title", "performers", "performer", "recording", comp_k="composers")
json.dump(out, open("/home/claude/dl/choco/charts_run09.json", "w"))
import collections
print(len(out), "charts; missing jams", missing, "; unparsed chord labels", bad, "; with >=8 chords", sum(len(c["chords"]) >= 8 for c in out))
print(collections.Counter(c["part"] for c in out))
