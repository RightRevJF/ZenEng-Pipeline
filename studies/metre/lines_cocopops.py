"""Sung lines in the 214 CoCoPops Billboard songs with melody (github.com/Computational-Cognitive-Musicology-Lab/CoCoPops, CC BY-NC 4.0).
A line starts at a syllable written with a capital letter (the transcribers' line starts) or after two beats or more of silence (as Window 117).
For each line: its section and the section's length in bars, the bar it starts in (counted from the section's first bar), its beat position,
its slot (first onset to the next line's first onset, in beats and seconds), its sung span, syllables, longest inner rest, and the song's bar
length in seconds (from the chord timestamps). 4/4 songs only."""
import glob, os, re, json, numpy as np, sys
sys.path.insert(0, "/home/claude/zeneng-pipeline/studies/tension")
from parse_cocopops import kern_dur
D = "/home/claude/data/cocopops/CoCoPops/Billboard/Data"
def events(path):
    spines = None; label = None; bar = 0; pos = 0.0; meter = None; ev = []; bars = {}; sec_start = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if not line or line.startswith("!"): continue
        toks = line.split("\t")
        if line.startswith("**"): spines = toks[:]; continue
        if spines is None: continue
        if line.startswith("*"):
            if any(t in ("*^", "*v", "*-", "*+", "*x") for t in toks):
                new = []; i = 0
                while i < len(toks):
                    t = toks[i]
                    if t == "*^": new += [spines[i], spines[i]]; i += 1
                    elif t == "*v":
                        j = i
                        while j < len(toks) and toks[j] == "*v": j += 1
                        new.append(spines[i]); i = j
                    elif t == "*-": i += 1
                    else: new.append(spines[i]); i += 1
                spines = new; continue
            for t in toks:
                m = re.match(r"^\*M(\d+)/(\d+)$", t)
                if m: meter = (int(m.group(1)), int(m.group(2)))
                m_ = re.match(r"^\*>Label>(.+)$", t)
                if m_: label = m_.group(1)
            continue
        if line.startswith("="):
            m = re.match(r"=(\d+)", toks[0]); bar = int(m.group(1)) if m else bar + 1; pos = 0.0
            bars.setdefault(bar, dict(label=label, t=None, meter=meter)); continue
        if len(toks) != len(spines): continue
        bars.setdefault(bar, dict(label=label, t=None, meter=meter))
        if bars[bar]["label"] is None: bars[bar]["label"] = label
        ki = spines.index("**kern") if "**kern" in spines else None; si = spines.index("**silbe") if "**silbe" in spines else None
        ti = spines.index("**timestamp")
        if toks[ti] != "." and bars[bar]["t"] is None:
            try: bars[bar]["t"] = float(toks[ti])
            except ValueError: pass
        if ki is None: continue
        t = toks[ki]
        if t == ".": continue
        if "q" in t: continue
        d = kern_dur(t); rest = "r" in t and not re.search(r"[a-gA-G]", t)
        tie_cont = t.endswith("]") or t.endswith("_")
        syl = toks[si] if si is not None else "."
        ev.append(dict(bar=bar, pos=pos, q=d, rest=rest, tie=tie_cont, syl=syl, label=bars[bar]["label"]))
        pos += d
    return ev, bars
def role(l):
    l = (l or "").lower()
    if "pre" in l and "chorus" in l: return "pre-chorus"
    for r in ("chorus", "verse", "bridge", "intro", "outro"):
        if r in l: return r
    return "other"
out = []
for f in sorted(glob.glob(f"{D}/*.hum")):
    name = os.path.basename(f).split(".")[0]
    ev, bars = events(f)
    if not ev: continue
    meters = [b["meter"] for b in bars.values() if b["meter"]]
    if not meters or max(set(meters), key=meters.count) != (4, 4): continue
    # bar seconds
    bn = sorted(bars); ts = [(b, bars[b]["t"]) for b in bn if bars[b]["t"] is not None]
    secs = [(t2 - t1) / (b2 - b1) for (b1, t1), (b2, t2) in zip(ts, ts[1:]) if b2 > b1 and 0 < (t2 - t1) / (b2 - b1) < 8]
    barsec = float(np.median(secs)) if secs else None
    # sections: runs of bars with the same label
    sec_of = {}; sid = -1; prev = object(); start = {}
    for b in bn:
        lab = bars[b]["label"]
        if lab != prev: sid += 1; start[sid] = b; prev = lab
        sec_of[b] = sid
    sec_len = {}
    for b in bn: sec_len[sec_of[b]] = sec_len.get(sec_of[b], 0) + 1
    # notes with absolute beat time
    notes = [dict(e, beat=(e["bar"] - bn[0]) * 4 + e["pos"]) for e in ev if e["bar"] in bars]
    lines = []; cur = None; last_end = None
    for e in notes:
        if e["rest"] or e["tie"]: continue
        if e["syl"] in (".", None): continue
        s = e["syl"].strip()
        gap = (e["beat"] - last_end) if last_end is not None else 99
        newline = cur is None or (s[:1].isupper() and not s.startswith("-")) or gap >= 2.0
        if newline:
            if cur: lines.append(cur)
            cur = dict(onsets=[], ends=[], bar=e["bar"], pos=e["pos"], label=e["label"])
        cur["onsets"].append(e["beat"]); cur["ends"].append(e["beat"] + e["q"])
        last_end = e["beat"] + e["q"]
    if cur: lines.append(cur)
    for i, L in enumerate(lines):
        nxt = lines[i + 1]["onsets"][0] if i + 1 < len(lines) else None
        slot = (nxt - L["onsets"][0]) if nxt is not None else None
        on = L["onsets"]; inner = [b - a for a, b in zip(L["ends"][:-1], on[1:])]
        # the downbeat the line belongs to: its own if it starts on beat 1, else the next bar (a pickup)
        home_bar = L["bar"] if L["pos"] < 2.0 else L["bar"] + 1          # a start on beat 3 or later leads into the next bar
        sid = sec_of.get(home_bar, sec_of.get(L["bar"])); bar_in_sec = (home_bar - start[sid]) if sid is not None else None
        out.append(dict(song=name, role=role(L["label"]), syl=len(on), start_pos=L["pos"], pickup=L["pos"] >= 0.25,
                        bar_in_sec=bar_in_sec, sec_len=sec_len.get(sid), slot_beats=slot, span_beats=L["ends"][-1] - on[0],
                        max_inner_rest=max(inner) if inner else 0.0, barsec=barsec))
json.dump(out, open("cocopops_lines.json", "w"))
print(len(out), "lines in", len({l["song"] for l in out}), "4/4 songs")
