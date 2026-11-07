"""Build the song record for 'The Song You Sang Me' from the frozen melody ranking (#1): one tenor and one guitar. Times in eighths at
q = 76 in 3/4 (a bar = 6 eighths). The guitar (steel-string, fingerpicked, capo 3 -- written at concert pitch, the capo shapes as chord
names) is the only accompaniment:
  accompaniment  the D-shape voicings with the capo (the bass on its string, the top three strings): verses 1-3 the waltz pattern in eighths
                 (bass, then the top three strings up and back); the bass alternates
                 root and fifth bar by bar; chorus 1: the same with the top note pinched on beat 1; the final chorus: pinched on beats 1 and 3, a little stronger; verse 4: one
                 chord a bar, let ring (the song thins where he sings the lullaby to them)
  the tune       (27.21, the run's reading: the instrumental line quotes the lullaby) the intro plays the chorus's first two lines alone
                 on the top strings over bass and chord; the outro its last two, ending on F, the last chord left to ring."""
import pickle, sys
sys.path[:0] = ["/home/claude/p24"]
import melody_p24 as M, lyric as L
R = pickle.load(open("/home/claude/p24/melody_result.pkl", "rb"))
c = R["alive"][0]
QB = 76
bars = [dict(sec=b["sec"], meter=b["meter"], chord=b["chord"], start=b["start"], len=b["len"], qbpm=QB, key="F major",
             build=False, instrumental=b["sec"] in ("Intro", "Outro")) for b in M.BARS]
def bar_at(e): return next(b for b in bars if b["start"] <= e < b["start"] + b["len"])
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        ln = M.SECS[s][li]
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=ln["role"], meter="3/4", singer="him"))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL; secs = sum(b["len"] * 60 / QB / 2 for b in bars)
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, met))
# ---- the guitar ----
# the D-shape voicings with capo 3 (shape pitches as played; concert = shape + 3): bass (root, fifth) and the top three strings
SHAPE = {"F": "D", "Bb": "G", "C": "A", "Dm": "Bm", "Gm": "Em", "Am": "F#m"}
SBASS = {"D": (50, 45), "G": (43, 50), "A": (45, 40), "Bm": (47, 42), "Em": (40, 47), "F#m": (42, 49)}      # D3/A2, G2/D3, A2/E2, B2/F#2, E2/B2, F#2/C#3
STOP = {"D": (57, 62, 66), "G": (55, 59, 67), "A": (57, 61, 64), "Bm": (59, 62, 66), "Em": (55, 59, 64), "F#m": (57, 61, 66)}
SSTR = {"bass_root": {"D": 4, "G": 6, "A": 5, "Bm": 5, "Em": 6, "F#m": 6}, "bass_fifth": {"D": 5, "G": 4, "A": 6, "Bm": 6, "Em": 5, "F#m": 5}}
CAPO_N = 3
def bass_of(ch, k): sh = SHAPE[ch]; return SBASS[sh][0 if k % 2 == 0 else 1] + CAPO_N
def upper(ch): return [p + CAPO_N for p in STOP[SHAPE[ch]]]
def lowest(pc, lo=43):
    p = lo
    while p % 12 != pc: p += 1
    return p
CAPO = {"F": "D", "Bb": "G", "C": "A", "Dm": "Bm", "Gm": "Em", "Am": "F#m"}
acc, mel = [], []
for bi, b in enumerate(bars):
    sec, ch, st = b["sec"], b["chord"], b["start"]
    k = bi - next(i for i, x in enumerate(bars) if x["sec"] == sec)
    bass = bass_of(ch, k); u = upper(ch)
    last = bi == len(bars) - 1
    if last:
        acc.append(dict(on=st, dur=6, p=[bass_of(ch, 0)] + u, vel=62, art="ring")); continue
    if sec in ("Intro", "Outro"):
        acc.append(dict(on=st, dur=2, p=[bass], vel=56, art="")); acc.append(dict(on=st + 2, dur=2, p=u[:2], vel=44, art="")); acc.append(dict(on=st + 4, dur=2, p=u[:2], vel=42, art=""))
    elif sec == "Verse 4":
        acc.append(dict(on=st, dur=6, p=[bass] + u, vel=50, art="ring"))
    else:
        pinch = sec.startswith("Chorus"); full = sec == "Chorus 2"
        pat = [None, 0, 1, 2, 1, 0]
        for e, i in enumerate(pat):
            if i is None: acc.append(dict(on=st, dur=1, p=[bass] + ([u[2]] if pinch else []), vel=(66 if full else 60) if pinch else 52, art=""))
            elif full and e == 4: acc.append(dict(on=st + e, dur=1, p=[u[0], u[2]], vel=54, art=""))      # the final chorus: a second pinch on beat 3
            else: acc.append(dict(on=st + e, dur=1, p=[u[i]], vel=(52 if full else 48 if pinch else 42) - (2 if e % 2 else 0), art=""))
# the tune (27.21): the lullaby quoted, intro = chorus lines 1-2 (from SLEEP), outro = chorus lines 3-4 (chorus 1's line 3, WAKE on F4)
ch1 = [n for n in lead if n["sec"] == "Chorus 1"]
c_at = M.SECS["Chorus 1"][0]["at"]; i_at = next(b["start"] for b in bars if b["sec"] == "Intro"); o_at = next(b["start"] for b in bars if b["sec"] == "Outro")
for n in ch1:
    if n["line"] in (0, 1):
        on = n["on"] - c_at + i_at
        if on >= i_at: mel.append(dict(on=on, dur=n["dur"], p=[n["midi"]], vel=70, art="", src="lullaby"))
    else:
        on = n["on"] - M.SECS["Chorus 1"][2]["at"] + o_at
        if on >= o_at: mel.append(dict(on=on, dur=n["dur"], p=[n["midi"]], vel=70, art="", src="lullaby"))   # the pickup dropped: the voice is still holding 'here'
mel.sort(key=lambda e: e["on"])
mel[-1]["dur"] = TOT - mel[-1]["on"]                                      # the last F held to the end
for a, b2 in zip(mel, mel[1:]):
    if a["on"] + a["dur"] > b2["on"]: a["dur"] = b2["on"] - a["on"]
def floor():
    out = {}
    for sec in ("Intro", "Outro"):
        ns = [n for n in mel if bar_at(n["on"])["sec"] == sec]
        strong = [n for n in ns if (n["on"] - bar_at(n["on"])["start"]) == 0]
        ct = sum(1 for n in strong if n["p"][0] % 12 in M.CH[bar_at(n["on"])["chord"]]) / max(1, len(strong))
        span = max(n["p"][0] for n in ns) - min(n["p"][0] for n in ns)
        out[sec] = dict(chord_tones_on_strong=(round(ct, 2), ct >= 0.8), distinct_pitches=(len({n["p"][0] for n in ns}), len({n["p"][0] for n in ns}) >= 3),
                        span=(span, span >= 7), range=([min(n["p"][0] for n in ns), max(n["p"][0] for n in ns)], True))
    return out
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], gtr=acc, gmel=mel, capo=3, capo_shapes=CAPO, shape_strings=SSTR, shape_of=SHAPE,
           instrument=dict(name="steel-string acoustic guitar", program=25, clef="treble_8"), gmel_floor=floor(), total_eighths=TOT, seconds=secs,
           singers=dict(him=M.HIM), singer_by_sec=L.SINGER, meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()),
           by_construction=R["by_construction"], qbpm={"3/4": QB}, eighth_sec={"3/4": 60 / QB / 2}, plans=c["plans"], cell_log=c["cell_log"])
pickle.dump(rec, open("/home/claude/p24/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", len(acc), "guitar events;", len(mel), "tune notes; fp", rec["fp"])
print(rec["gmel_floor"])
