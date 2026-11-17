"""Arrangement study, part 1: texture by section role in POP909 (Wang et al. 2020; 909 Chinese pop songs, each a lead melody, a
secondary melody ('BRIDGE') and a professional piano accompaniment, CC BY 4.0, read from github.com/music-x-lab/POP909-Dataset) with
the human phrase labels of Dai, Zhang and Dannenberg (2020; github.com/Dsqvival/hierarchical-structure-analysis): i intro, o outro,
upper case a sung phrase (A usually the verse, B usually the chorus, letters by repetition), lower case an instrumental phrase.
Per phrase: the piano's notes a beat, notes struck together, lowest and highest pitch, share of onsets off the beat, sustain (share of
the phrase with a piano note sounding), the secondary melody's notes a beat. By role, and paired within songs (B against A; the last
B against the first). Writes pop909_texture.json."""
import os, re, json, collections, statistics as st
import pretty_midi
D = "/home/claude/data/pop909"
def roles(lab):
    out = []
    for m in re.finditer(r"([A-Za-z])(\d+)", lab):
        c, n = m.group(1), int(m.group(2))
        r = "intro" if c == "i" else "outro" if c == "o" else ("instrumental" if c.islower() else ("A" if c == "A" else "B" if c == "B" else "other sung"))
        out.append((r, c, n))
    return out
rows = []; pairs = collections.defaultdict(list)
for sid in sorted(os.listdir(D)):
    p = f"{D}/{sid}"
    if not os.path.isdir(p) or not os.path.exists(f"{p}/{sid}.mid"): continue
    try:
        lab = open(f"{p}/human_label1.txt").read().strip(); beats = [list(map(float, l.split())) for l in open(f"{p}/beat_midi.txt") if l.strip()]
        m = pretty_midi.PrettyMIDI(f"{p}/{sid}.mid")
    except Exception: continue
    if not lab or "Not Found" in lab or len(beats) < 16: continue
    bt = [b[0] for b in beats]; db = [b[0] for b in beats if len(b) > 2 and b[2] == 1.0]
    if len(db) < 8: continue
    tr = {i.name: i.notes for i in m.instruments}
    if "PIANO" not in tr: continue
    b0 = 0; song = []
    for r, c, n in roles(lab):
        if b0 + n >= len(db): break
        t0, t1 = db[b0], db[b0 + n]; nb = sum(1 for x in bt if t0 <= x < t1) or 4 * n
        pn = [x for x in tr["PIANO"] if t0 <= x.start < t1]
        ons = collections.defaultdict(list)
        for x in pn: ons[round(x.start / 0.03)].append(x.pitch)
        beatset = [x for x in bt if t0 <= x < t1]; spb = (t1 - t0) / nb
        off = sum(1 for k in ons if min(abs(k * 0.03 - b) for b in beatset) > spb * 0.2) / max(1, len(ons)) if beatset else None
        cover = 0.0
        if pn:
            iv = sorted((x.start, min(x.end, t1)) for x in pn); cs, ce = iv[0]
            for s, e in iv[1:]:
                if s > ce: cover += ce - cs; cs, ce = s, e
                else: ce = max(ce, e)
            cover += ce - cs
        sec = dict(song=sid, role=r, letter=c, bars=n, piano_per_beat=len(pn) / nb, together=(st.mean(len(v) for v in ons.values()) if ons else 0),
                   low=(st.median(min(v) for v in ons.values()) if ons else None), high=(st.median(max(v) for v in ons.values()) if ons else None),
                   offbeat=off, sustain=cover / (t1 - t0), second_per_beat=len([x for x in tr.get("BRIDGE", []) if t0 <= x.start < t1]) / nb,
                   melody_per_beat=len([x for x in tr.get("MELODY", []) if t0 <= x.start < t1]) / nb)
        song.append(sec); rows.append(sec); b0 += n
    A = [s for s in song if s["role"] == "A"]; B = [s for s in song if s["role"] == "B"]
    if A and B:
        for k in ("piano_per_beat", "together", "high", "low", "sustain", "second_per_beat"):
            a, b = st.mean(x[k] for x in A if x[k] is not None), st.mean(x[k] for x in B if x[k] is not None)
            pairs[k].append(b - a)
    if len(B) >= 2:
        pairs["last_B_minus_first_B piano_per_beat"].append(B[-1]["piano_per_beat"] - B[0]["piano_per_beat"])
        pairs["last_B_minus_first_B together"].append(B[-1]["together"] - B[0]["together"])
q = lambda v: [round(x, 3) for x in st.quantiles([y for y in v if y is not None], n=4)] if len([y for y in v if y is not None]) >= 4 else None
by = collections.defaultdict(list)
for r in rows: by[r["role"]].append(r)
out = dict(about=__doc__.split("\n")[0], songs=len({r["song"] for r in rows}), phrases=len(rows), by_role={}, paired_B_minus_A={})
for role, rs in sorted(by.items()):
    out["by_role"][role] = dict(n=len(rs), **{k: q([r[k] for r in rs]) for k in ("bars", "piano_per_beat", "together", "low", "high", "offbeat", "sustain", "second_per_beat", "melody_per_beat")})
for k, v in pairs.items(): out["paired_B_minus_A"][k] = dict(n=len(v), median=round(st.median(v), 3), share_positive=round(sum(1 for x in v if x > 0) / len(v), 3))
json.dump(out, open("pop909_texture.json", "w"), indent=1)
print(out["songs"], "songs", out["phrases"], "phrases")
for k, v in out["by_role"].items(): print(k, v)
for k, v in out["paired_B_minus_A"].items(): print("paired", k, v)
