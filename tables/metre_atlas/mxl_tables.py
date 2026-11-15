"""Tables from sung MusicXML collections: OpenScore Lieder (github.com/OpenScore/Lieder, CC0; 19th-century art songs) and OpenEWLD
(github.com/00sapo/OpenEWLD, MIT; popular-song lead sheets). The voice is the part carrying the most lyric syllables. Every bar is filed
under its own time signature, so a song that changes metre feeds each metre's table with its own bars. Per metre and collection: the
readings of atlas_build and their quartiles, bar rhythms, onset weights; and for English songs (most lyric words found in the CMU
Pronouncing Dictionary) the stress-to-position table of hymn_atlas. Writes tables/<collection>_mxl.json.
Usage: python3 mxl_tables.py lieder|ewld"""
import sys, glob, zipfile, re, json, collections
from multiprocessing import Pool
import numpy as np
from lxml import etree
import pronouncing
import atlas_build as AB
import hymn_atlas as HA
SRC = {"lieder": ("/home/claude/atlas/src/Lieder/scores/**/*.mxl", "CC0 (OpenScore Lieder)"),
       "ewld": ("/tmp/dl/00sapo_OpenEWLD/dataset/**/*.mxl", "MIT (OpenEWLD)")}
STEP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
def load(path):
    z = zipfile.ZipFile(path); names = [n for n in z.namelist() if n.endswith(".xml") and not n.startswith("META")]
    return etree.fromstring(z.read(names[0]))
def voice_part(root):
    parts = root.findall("part")
    return max(parts, key=lambda p: len(p.findall(".//lyric"))) if parts else None
def notes_of(part):
    div = 1; ts = None; out = []; mi = 0; t_abs_bar = 0
    for m in part.findall("measure"):
        a = m.find("attributes")
        if a is not None:
            d = a.find("divisions"); div = int(float(d.text)) if d is not None else div
            t = a.find("time")
            if t is not None and t.find("beats") is not None:
                try: ts = f"{int(t.find('beats').text)}/{int(t.find('beat-type').text)}"
                except ValueError: pass
        pos = 0; mnotes = []
        for el in m:
            if el.tag == "backup": pos -= int(float(el.find("duration").text)); continue
            if el.tag == "forward": pos += int(float(el.find("duration").text)); continue
            if el.tag != "note": continue
            if el.find("grace") is not None: continue
            dur_el = el.find("duration"); dur = int(float(dur_el.text)) if dur_el is not None else 0
            if el.find("chord") is not None: continue
            v = el.find("voice")
            if v is not None and v.text not in ("1", None): pos += dur; continue
            if el.find("rest") is None:
                p = el.find("pitch"); midi = None
                if p is not None:
                    alt = p.find("alter"); midi = 12 * (int(p.find("octave").text) + 1) + STEP[p.find("step").text] + (int(float(alt.text)) if alt is not None else 0)
                tie_stop = any(t.get("type") == "stop" for t in el.findall("tie"))
                ly = el.find("lyric"); syl = joins = None
                if ly is not None and ly.find("text") is not None:
                    syl = ly.find("text").text or ""; sy = ly.find("syllabic"); joins = sy is not None and sy.text in ("begin", "middle")
                mnotes.append(dict(pos=pos, dur=dur, p=midi, tie=tie_stop, syl=syl, joins=joins))
            pos += dur
        mlen = max([n["pos"] + n["dur"] for n in mnotes] + [pos, 0])
        out.append(dict(ts=ts, div=div, len=mlen, notes=mnotes, implicit=m.get("implicit") == "yes"))
    return out
def song(path):
    try:
        part = voice_part(load(path))
        if part is None: return None
        ms = notes_of(part)
    except Exception: return None
    words = []; cur = []
    for m in ms:
        for n in m["notes"]:
            if n["syl"]:
                cur.append(n["syl"])
                if not n["joins"]: words.append("".join(cur)); cur = []
    hits = sum(1 for w in words[:200] if pronouncing.phones_for_word(re.sub(r"[^a-z']", "", w.lower()).strip("'")))
    english = len(words) >= 20 and hits / max(1, min(200, len(words))) >= 0.75
    return dict(path=path, measures=ms, english=english, n_syl=sum(1 for m in ms for n in m["notes"] if n["syl"]))
BEATS = {"2/4": [0, 12], "3/4": [0, 12, 24], "4/4": [0, 12, 24, 36], "2/2": [0, 24], "3/2": [0, 24, 48], "6/8": [0, 18], "9/8": [0, 18, 36], "12/8": [0, 18, 36, 54],
         "3/8": [0], "6/4": [0, 36], "5/4": [0, 12, 24, 36, 48], "7/8": [0, 12, 24], "5/8": [0, 12], "4/2": [0, 24, 48, 72], "9/4": [0, 36, 72]}
STRONG = {"4/4": [0, 24], "6/8": [0, 18], "6/4": [0, 36], "9/8": [0, 18, 36], "12/8": [0, 18, 36, 54], "2/2": [0], "3/4": [0], "2/4": [0], "3/8": [0], "3/2": [0], "5/4": [0], "9/4": [0, 36, 72]}
if __name__ == "__main__":
    coll = sys.argv[1]; pat, lic = SRC[coll]
    files = sorted(glob.glob(pat, recursive=True))
    with Pool(2) as pool: songs = [s for s in pool.map(song, files, chunksize=8) if s]
    per = collections.defaultdict(lambda: dict(R=[], BAR=collections.Counter(), POS=collections.Counter(), songs=0, english=0, S=collections.Counter()))
    for s in songs:
        seg = collections.defaultdict(list)                                        # metre -> notes in absolute ticks of that metre's bars
        barcount = collections.Counter()
        for m in s["measures"]:
            ts = m["ts"]
            if not ts or ts not in BEATS or not m["div"]: continue
            num, den = map(int, ts.split("/")); bl = int(num * 48 / den); k = 12 / m["div"]
            shift = bl - int(round(m["len"] * k)) if (m["implicit"] and m["len"] * k < bl) else 0
            b = barcount[ts]; barcount[ts] += 1
            for n in m["notes"]:
                on = int(round(n["pos"] * k)) + shift; d = max(1, int(round(n["dur"] * k)))
                if n["p"] is None or n["tie"] or on < 0 or on >= bl or on % 3: continue
                seg[ts].append(dict(on=b * bl + on, dur=d, p=n["p"], syl=n["syl"], joins=n["joins"]))
        for ts, ns in seg.items():
            if len(ns) < 16: continue
            bl = int(int(ts.split("/")[0]) * 48 / int(ts.split("/")[1])); beats = BEATS[ts]; beat = AB.METRES.get(ts, (None, None, None))[2]
            D = per[ts]; D["songs"] += 1
            D["R"].append(AB.readings([[n["on"], n["dur"], n["p"]] for n in ns], bl, beats, beat))
            bars = collections.defaultdict(list)
            for n in ns: bars[n["on"] // bl].append(n["on"] % bl); D["POS"][n["on"] % bl] += 1
            for v in bars.values(): D["BAR"][tuple(v)] += 1
            if s["english"] and ts in STRONG:
                D["english"] += 1
                al = [dict(on=n["on"], syl=n["syl"], joins=n["joins"]) for n in ns if n["syl"]]
                for w in HA.stanza_words(al):
                    st = HA.word_stresses("".join(x["syl"] for x in w), len(w))
                    if st is None: continue
                    for x, s_ in zip(w, st):
                        pos = x["on"] % bl
                        lvl = "downbeat" if pos == 0 else ("strong beat" if pos in STRONG[ts] else ("beat" if pos in beats else "off the beat"))
                        D["S"][(["unstressed", "primary", "secondary"][s_], lvl)] += 1
    out = {"collection": coll, "licence": lic, "songs_read": len(songs), "english_songs": sum(s["english"] for s in songs), "by_metre": {}}
    for ts, D in sorted(per.items(), key=lambda x: -x[1]["songs"]):
        if not D["R"]: continue
        Q = {k: [float(np.percentile([r[k] for r in D["R"]], q)) for q in (25, 50, 75)] for k in D["R"][0]}
        tot = sum(D["POS"].values())
        stress = {}
        for cls in ("primary", "unstressed"):
            t = sum(v for (c, l), v in D["S"].items() if c == cls)
            stress[cls] = dict({l: round(D["S"][(cls, l)] / t, 3) for l in ("downbeat", "strong beat", "beat", "off the beat")}, syllables=t) if t else {}
        out["by_metre"][ts] = dict(songs=D["songs"], english_songs=D["english"], readings_quartiles=Q, bar_rhythms=[[list(k), v] for k, v in D["BAR"].most_common(15)],
                                   bars_total=sum(D["BAR"].values()), onset_weights={str(k): round(v / tot, 4) for k, v in sorted(D["POS"].items())}, stress=stress)
        print(ts, D["songs"], "songs;", D["english"], "English;", "stress", stress.get("primary"))
    json.dump(out, open(f"/home/claude/atlas/tables/{coll}_mxl.json", "w"))
    print("songs read", len(songs), "English", out["english_songs"])
