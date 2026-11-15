"""Accompaniment tables from OpenScore Lieder (CC0): the piano part under the voice, by metre (749.14).
Per song and metre: the piano's right hand (staff 1) and left hand (staff 2) as onsets with their chord sizes; per bar: the onset pattern
of each hand, the notes struck together, the register, and how the piano and voice share the beat. Texture of each bar, by rules:
  sustained   - each hand strikes once (or not at all) in the bar
  block       - one hand repeats chords (3+ notes) on several beats
  waltz       - the left hand strikes once on the downbeat and the right hand strikes chords on the other beats (3/4, 3/8)
  broken      - a hand strikes single notes in steady values whose pitches outline the chord (arpeggio, Alberti, rocking figures)
  melodic     - the right hand's top line moves by step in running values (a countermelody or doubling)
  mixed       - none of these
Readings per metre: piano onsets a beat (each hand), share of piano onsets falling where the voice has none (complementarity), notes
struck together, register gap between the voice and the right hand's top, share of bars per texture, and how density changes from the
song's first third to its last. Writes tables/accompaniment_lieder.json."""
import glob, zipfile, collections, json, re, statistics
from multiprocessing import Pool
import numpy as np
from lxml import etree
STEP = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
METRES = {"3/4": (36, [0, 12, 24]), "6/8": (36, [0, 18]), "2/4": (24, [0, 12]), "4/4": (48, [0, 12, 24, 36]), "3/8": (18, [0]), "9/8": (54, [0, 18, 36]),
          "12/8": (72, [0, 18, 36, 54]), "6/4": (72, [0, 36]), "2/2": (48, [0, 24]), "3/2": (72, [0, 24, 48])}
def load(path):
    z = zipfile.ZipFile(path); n = [x for x in z.namelist() if x.endswith(".xml") and not x.startswith("META")][0]
    return etree.fromstring(z.read(n))
def pitch(el):
    p = el.find("pitch")
    if p is None: return None
    alt = p.find("alter")
    return 12 * (int(p.find("octave").text) + 1) + STEP[p.find("step").text] + (int(float(alt.text)) if alt is not None else 0)
def part_events(part, keep_staff=None):
    """per measure: ts, length, events dict(on, dur, p, staff); chords merged into one event with a pitch list"""
    div = 1; ts = None; out = []
    for m in part.findall("measure"):
        a = m.find("attributes")
        if a is not None:
            d = a.find("divisions"); div = int(float(d.text)) if d is not None else div
            t = a.find("time")
            if t is not None and t.find("beats") is not None:
                try: ts = f"{int(t.find('beats').text)}/{int(t.find('beat-type').text)}"
                except ValueError: pass
        pos = 0; last_on = {}; evs = []
        for el in m:
            if el.tag == "backup": pos -= int(float(el.find("duration").text)); continue
            if el.tag == "forward": pos += int(float(el.find("duration").text)); continue
            if el.tag != "note" or el.find("grace") is not None: continue
            d = el.find("duration"); dur = int(float(d.text)) if d is not None else 0
            st = el.find("staff"); staff = int(st.text) if st is not None else 1
            if el.find("chord") is not None:
                on = last_on.get(staff, pos)
                p = pitch(el)
                if p is not None and evs and evs[-1]["on"] == on and evs[-1]["staff"] == staff: evs[-1]["p"].append(p)
                continue
            p = pitch(el); tie = any(t.get("type") == "stop" for t in el.findall("tie"))
            if p is not None and not tie: evs.append(dict(on=pos, dur=dur, p=[p], staff=staff, lyric=el.find("lyric") is not None))
            last_on[staff] = pos; pos += dur
        out.append(dict(ts=ts, div=div, evs=evs, implicit=m.get("implicit") == "yes"))
    return out
def texture(rh, lh, bl, beats, ts):
    """rh, lh: lists of (pos, pitches) in the bar"""
    def single_run(h):
        return len(h) >= 3 and all(len(p) == 1 for _, p in h)
    if len(rh) <= 1 and len(lh) <= 1: return "sustained"
    if ts in ("3/4", "3/8") and len(lh) == 1 and lh[0][0] == 0 and len(rh) >= 2 and all(len(p) >= 2 for _, p in rh) and all(o != 0 for o, _ in rh[1:]): return "waltz"
    for h in (lh, rh):
        if single_run(h):
            ps = [p[0] for _, p in h]; iv = np.diff(ps)
            gaps = np.diff([o for o, _ in h])
            if len(set(gaps)) <= 2 and np.mean(abs(iv) >= 3) >= 0.5: return "broken"
    if sum(1 for _, p in rh if len(p) >= 3) >= 2 or sum(1 for _, p in lh if len(p) >= 3) >= 2: return "block"
    if len(rh) >= 4:
        tops = [max(p) for _, p in rh]; iv = np.diff(tops)
        if np.mean((abs(iv) >= 1) & (abs(iv) <= 2)) >= 0.5: return "melodic"
    return "mixed"
def song(path):
    try: root = load(path)
    except Exception: return None
    parts = root.findall("part")
    if len(parts) < 2: return None
    voice = max(parts, key=lambda p: len(p.findall(".//lyric")))
    pianos = [p for p in parts if p is not voice and len(p.findall(".//staff")) > 0]
    if not pianos: return None
    V = part_events(voice); Pn = part_events(pianos[0])
    res = collections.defaultdict(lambda: dict(bars=0, rh_on=0, lh_on=0, comp=0, pon=0, struck=[], gap=[], tex=collections.Counter(), dens=[], rhpat=collections.Counter(), lhpat=collections.Counter()))
    for vm, pm in zip(V, Pn):
        ts = pm["ts"] or vm["ts"]
        if ts not in METRES or not pm["div"]: continue
        bl, beats = METRES[ts]; k = 12 / pm["div"]; kv = 12 / (vm["div"] or 1)
        rh = sorted([(int(round(e["on"] * k)), e["p"]) for e in pm["evs"] if e["staff"] == 1 and e["on"] * k < bl], key=lambda x: x[0])
        lh = sorted([(int(round(e["on"] * k)), e["p"]) for e in pm["evs"] if e["staff"] == 2 and e["on"] * k < bl], key=lambda x: x[0])
        vo = {int(round(e["on"] * kv)) for e in vm["evs"]}
        vp = [p for e in vm["evs"] for p in e["p"]]
        D = res[ts]; D["bars"] += 1; D["rh_on"] += len(rh); D["lh_on"] += len(lh)
        pon = {o for o, _ in rh} | {o for o, _ in lh}; D["pon"] += len(pon); D["comp"] += len(pon - vo)
        D["struck"] += [len(p) for _, p in rh + lh]
        if vp and rh: D["gap"].append(min(vp) - max(max(p) for _, p in rh))
        D["tex"][texture(rh, lh, bl, beats, ts)] += 1; D["dens"].append(len(pon))
        D["rhpat"][tuple(o for o, _ in rh if o % 3 == 0)] += 1; D["lhpat"][tuple(o for o, _ in lh if o % 3 == 0)] += 1
    out = {}
    for ts, D in res.items():
        if D["bars"] < 8: continue
        n = len(D["dens"]); third = max(1, n // 3)
        out[ts] = dict(bars=D["bars"], rh_onsets_a_bar=D["rh_on"] / D["bars"], lh_onsets_a_bar=D["lh_on"] / D["bars"], complementarity=D["comp"] / max(1, D["pon"]),
                       notes_struck=float(np.mean(D["struck"])) if D["struck"] else 0, voice_above_rh=float(np.median(D["gap"])) if D["gap"] else None,
                       texture={k: v / D["bars"] for k, v in D["tex"].items()}, density_first_third=float(np.mean(D["dens"][:third])), density_last_third=float(np.mean(D["dens"][-third:])),
                       rhpat=[[list(k), v] for k, v in D["rhpat"].most_common(8)], lhpat=[[list(k), v] for k, v in D["lhpat"].most_common(8)])
    return dict(path=path, metres=out) if out else None
if __name__ == "__main__":
    files = sorted(glob.glob("/home/claude/atlas/src/Lieder/scores/**/*.mxl", recursive=True))
    with Pool(2) as pool: songs = [s for s in pool.map(song, files, chunksize=8) if s]
    agg = {}
    for ts in METRES:
        S = [s["metres"][ts] for s in songs if ts in s["metres"]]
        if len(S) < 5: continue
        bl = METRES[ts][0]; nb = len(METRES[ts][1])
        q = lambda k: [float(np.percentile([x[k] for x in S if x[k] is not None], p)) for p in (25, 50, 75)]
        tex = collections.Counter()
        for x in S:
            for k, v in x["texture"].items(): tex[k] += v * x["bars"]
        tb = sum(tex.values())
        rp = collections.Counter(); lp = collections.Counter()
        for x in S:
            for k, v in x["rhpat"]: rp[tuple(k)] += v
            for k, v in x["lhpat"]: lp[tuple(k)] += v
        growth = [x["density_last_third"] / max(0.5, x["density_first_third"]) for x in S]
        agg[ts] = dict(songs=len(S), bars=sum(x["bars"] for x in S), rh_onsets_a_beat=[v / nb for v in q("rh_onsets_a_bar")], lh_onsets_a_beat=[v / nb for v in q("lh_onsets_a_bar")],
                       complementarity=q("complementarity"), notes_struck=q("notes_struck"), voice_above_rh_semitones=q("voice_above_rh"),
                       texture_share={k: round(v / tb, 3) for k, v in tex.most_common()}, density_growth_last_over_first=[float(np.percentile(growth, p)) for p in (25, 50, 75)],
                       rh_patterns=[[list(k), v] for k, v in rp.most_common(10)], lh_patterns=[[list(k), v] for k, v in lp.most_common(10)])
        print(ts, len(S), "songs;", {k: round(v / tb, 2) for k, v in tex.most_common()}, "comp", [round(x, 2) for x in q("complementarity")], "rh/beat", [round(v / nb, 2) for v in q("rh_onsets_a_bar")], "lh/beat", [round(v / nb, 2) for v in q("lh_onsets_a_bar")])
    json.dump(dict(source="OpenScore Lieder (github.com/OpenScore/Lieder)", licence="CC0", commercial_use="yes (CC0)", songs_read=len(songs), by_metre=agg),
              open("/home/claude/atlas/tables/accompaniment_lieder.json", "w"))
