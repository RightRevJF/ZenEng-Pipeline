"""Build the song record for 'I Took Him for the Gardener' from the frozen melody (melody_final.pkl). An Easter concert solo: one high
voice (written for soprano; the mezzo edition a minor third lower), piano, cello, strings. Times in EIGHTHS; 6/8 (a bar = 6) at
dotted quarter = 52 (q = 78), the last refrain broadened to q = 72 and the coda to q = 66. D minor; D major from MARY (bar 55).
  piano      the walking figure, the left hand rocking in eighths: root-fifth-tenth | octave-tenth-fifth (verse 1 bare: the root and
             fifth in dotted quarters, the dark); the right hand a chord on each dotted-quarter beat from refrain 1, held; full from verse 4
  cello      from verse 2: the root a bar, held; in verses 2 and 3 it ANSWERS each line (fix 90): the line's last three notes an octave
             below, in eighths, after the singer lands, ending by the next line's downbeat; in the INTERLUDE it sings the refrain's first
             two lines an octave below the voice, with ONE note changed (fix 91): DAWN's A3 rises to C#4 over A, the leading tone, the
             first lean toward the light; from verse 4 a held bass line
  strings    a soft pad under the refrains; the interlude's last two bars swell; the Name builds through its first two lines
  anchors    NAME (the Name, line 3): the whole band silent for its bar (N.C.), the voice alone. MARY: everyone back on D major, soft and
             full, held through the bar of silence after it; RABBONI over G and A
  the end    the last refrain's last line: the title cell, then a bar where only the strings hold A (the voice and the piano silent), then 'and he WAS'
             on D5 over D, closed; the coda (fix 93): the piano alone states the title cell in D major (refrain 3's own notes), then the
             open D chord with an added E, A4 on top, let ring."""
import pickle, sys
sys.path[:0] = ["/home/claude/p32"]
import melody_p32 as M, lyric as L
c = pickle.load(open("/home/claude/p32/melody_final.pkl", "rb"))
MARY_AT = M.SECS["The Name"][3]["at"]
bars = []
for i, b in enumerate(M.BARS):
    k = sum(1 for x in M.BARS[:i] if x["sec"] == b["sec"])
    key = "D major" if b["start"] >= MARY_AT else "D minor"
    nc = any(b["sec"] == s and M.SECS[s][li]["at"] + 6 * bl == b["start"] for s, li, bl in M.TACET)
    bars.append(dict(sec=b["sec"], meter="6/8", chord=("N.C." if nc else b["chord"]), implied=b["chord"], start=b["start"], len=6,
                     qbpm=M.QBPM.get(b["sec"], M.QDEF), k=k, key=key, instrumental=b["sec"] in ("Intro", "Interlude", "Coda")))
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=M.SECS[s][li]["role"], meter="6/8", singer="her"))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL
secs = sum(6 * 60 / b["qbpm"] / 2 for b in bars)
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, "6/8"))
ROOT = {"Dm": 2, "Gm": 7, "Bb": 10, "F": 5, "C": 0, "A": 9, "Am": 9, "D": 2, "G": 7, "Bm": 11, "Em": 4, "F#m": 6}
THIRD = {k: (r + (3 if k.endswith("m") else 4)) % 12 for k, r in ROOT.items()}
def at_or_above(pc, lo):
    p = lo
    while p % 12 != pc: p += 1
    return p
def voicing(ch, lo, n=3):
    out, p = [], lo
    while len(out) < n:
        if p % 12 in M.CH[ch]: out.append(p)
        p += 1
    return out
pno, cello, strings = [], [], []
NC_BAR = next(b for b in bars if b["chord"] == "N.C.")["start"]
MARY = next(n for n in lead if n["sec"] == "The Name" and n["syl"][0] == "mary")
LAST5 = M.SECS["Refrain 3"][4]["at"]; HUSH = LAST5 + 12                         # the last line's third bar: the voice silent, the strings hold
DYN = {"Intro": 48, "Verse 1": 44, "Refrain 1": 56, "Verse 2": 52, "Refrain 2": 62, "Interlude": 52, "Verse 3": 56, "The Name": 52,
       "Verse 4": 72, "Refrain 3": 82, "Coda": 48}
for bi, b in enumerate(bars):
    sec, ch, st, k = b["sec"], b["implied"], b["start"], b["k"]
    if st == NC_BAR: continue                                                 # NAME: the whole band silent for its bar
    mary = sec == "The Name" and st >= MARY_AT
    v = DYN[sec] + (2 * k if sec == "The Name" and k < 4 else 0) + (6 if mary else 0)
    r = at_or_above(ROOT[ch], 36)                                             # C2-B2
    fifth = r + 7; tenth = at_or_above(THIRD[ch], r + 12); octv = r + 12
    last = sec == "Refrain 3" and st >= LAST5
    # ---- piano ----
    if sec == "Coda":                                                          # fix 93: the title cell returns (below), then the open chord
        if k < 2: pno.append(dict(on=st, dur=6, p=[r, fifth], vel=46 - 3 * k, hand="lh", art="ring"))
        elif k == 2: pno.append(dict(on=st, dur=6, p=[r, fifth] + voicing(ch, 62), vel=44, hand="both", art="ring"))
        else: pno.append(dict(on=st, dur=6, p=[r, fifth, 62, 64, 66, 69], vel=40, hand="both", art="ring"))   # D with an added E, A4 on top
        continue
    if st == HUSH:
        pass                                                                   # bar 77: the strings alone (revision 2: the piano's low A cut)
    elif mary:                                                                 # MARY: one D major chord a bar, held, no figure
        pno.append(dict(on=st, dur=6, p=[r, fifth, tenth], vel=v - 6, hand="lh", art="ring"))
        pno.append(dict(on=st, dur=6, p=voicing(ch, 62, 3), vel=v - 10, hand="rh", art="ring"))
    elif sec == "Verse 1":
        pno += [dict(on=st + e, dur=3, p=[q], vel=v - (0 if e == 0 else 6), hand="lh", art="") for e, q in zip((0, 3), (r, fifth))]
    else:
        fig = [r, fifth, tenth, octv, tenth, fifth]
        pno += [dict(on=st + e, dur=1, p=[q], vel=v - (0 if e == 0 else 8), hand="lh", art="") for e, q in enumerate(fig)]
    if not mary and st != HUSH and (sec not in ("Intro", "Verse 1", "Verse 2", "Verse 3", "Interlude") or (sec == "Intro" and k in (0, 2))):
        rh = voicing(ch, 62 if sec not in ("Verse 4", "Refrain 3") else 66, 3 if not last else 2)
        for e in ((0, 3) if sec in ("Verse 4", "Refrain 3") and not last else (0,)):
            pno.append(dict(on=st + e, dur=6 - e if e == 0 and sec not in ("Verse 4", "Refrain 3") else 3, p=rh, vel=v - 6 - (14 if last else 0) - (4 if e else 0), hand="rh", art="ring"))
    # ---- cello ----
    if sec == "Interlude": pass                                               # the refrain's lines 1-2, written below
    elif sec in ("Verse 2", "Refrain 2", "Verse 3", "The Name", "Verse 4") or (sec == "Refrain 3" and not last):
        cello.append(dict(on=st, dur=6, p=[r + 12 if r + 12 <= 52 else r], vel=v - 4, art=""))
    elif last and st != HUSH: cello.append(dict(on=st, dur=6, p=[r + 12 if r + 12 <= 52 else r], vel=48, art=""))
    # ---- strings ----
    if sec in ("Refrain 1", "Refrain 2", "Verse 4", "Refrain 3") or (sec == "Interlude" and k >= 2) or (sec == "The Name" and (k < 4 or mary)):
        pad = voicing(ch, 57, 3)
        sv = v - 10 + (8 * (k - 1) if sec == "Interlude" else 0)
        if sec == "Refrain 3" and not last: pad = pad + [voicing(ch, 74, 1)[0]]
        if mary: pad = pad + [voicing(ch, 69, 1)[0]]
        strings.append(dict(on=st, dur=6, p=pad, vel=max(30, sv - (18 if last else 0)), art="pad"))
# the interlude: the cello sings the refrain's lines 1-2 an octave below the voice, one note changed (fix 91): DAWN rises from A3 to
# C#4 over A -- the leading tone, the first lean toward D
I0 = M.STARTS["Interlude"][1]; d = I0 - M.STARTS["Refrain 1"][1]
R1 = [n for n in lead if n["sec"] == "Refrain 1" and n["line"] in (0, 1)]
VARIED = None
for n in R1:
    p = n["midi"] - 12; dur = n["dur"]
    if n["line"] == 1 and n["syl"][0] == "dawn":
        p = 61; dur = I0 + 24 - (n["on"] + d); VARIED = dict(on=n["on"] + d, was=n["midi"] - 12, now=61)
    cello.append(dict(on=n["on"] + d, dur=dur, p=[p], vel=54, art="interlude"))
assert VARIED and next(b for b in bars if b["start"] <= VARIED["on"] < b["start"] + 6)["implied"] == "A"
assert min(e["on"] for e in cello if e["art"] == "interlude") >= max(n["on"] + n["dur"] for n in lead if n["sec"] == "Refrain 2"), "the pickup clears GONE"
# verses 2 and 3: the cello answers each line (fix 90) -- the line's last three notes an octave below, in eighths, from the eighth after
# the singer's last note begins; it ends by the next line's first downbeat; the held root gives way for that bar
ANSWERS = []
lines_ = {}
for n in lead: lines_.setdefault((n["sec"], n["line"]), []).append(n)
for (sec_, li), ns in lines_.items():
    if sec_ not in ("Verse 2", "Verse 3"): continue
    t = ns[-1]["on"] + 1
    stop = M.SECS[sec_][li]["at"] + 12
    figure = [x["midi"] - 12 for x in ns[-3:]]
    if t + 3 > stop: continue
    bar0 = next(b for b in bars if b["start"] <= t < b["start"] + 6)["start"]
    held = [e for e in cello if e["on"] == bar0 and e["art"] == ""]
    cello = [e for e in cello if not (e["on"] == bar0 and e["art"] == "")] + ([dict(on=bar0, dur=t - bar0, p=held[0]["p"], vel=50, art="")] if held and t > bar0 else [])
    cello += [dict(on=t + j, dur=1 if j < 2 else max(1, min(2, stop - (t + 2))), p=[q], vel=56, art="answer") for j, q in enumerate(figure)]
    ANSWERS.append(dict(sec=sec_, line=li, on=t, figure=figure))
cello.sort(key=lambda e: e["on"])
for a_, b_ in zip(cello, cello[1:]):                                          # a held root gives way to the next entry (the interlude's pickup)
    if a_["on"] + a_["dur"] > b_["on"]: a_["dur"] = b_["on"] - a_["on"]
assert all(e["dur"] >= 1 for e in cello)
# the coda: the piano's right hand states the title cell in D major (refrain 3's title line, the voice's own notes), then rests
CODA0 = next(b["start"] for b in bars if b["sec"] == "Coda")
T3 = [n for n in lead if n["sec"] == "Refrain 3" and n["line"] == 0]
at0 = M.SECS["Refrain 3"][0]["at"]
CODA_PHRASE = [dict(on=CODA0 + (n["on"] - at0), dur=n["dur"] if i < len(T3) - 1 else 4, p=[n["midi"]], vel=50, hand="rh", art="coda") for i, n in enumerate(T3)]
assert CODA_PHRASE[0]["on"] >= max(n["on"] + n["dur"] for n in lead), "the coda's pickup clears the voice"
pno += CODA_PHRASE; pno.sort(key=lambda e: e["on"])
assert not [e for e in pno + cello + strings if NC_BAR <= e["on"] < NC_BAR + 6], "NAME: the band silent"
assert not [e for e in pno + cello if HUSH <= e["on"] < HUSH + 6] and [e for e in strings if e["on"] == HUSH], "bar 77: the strings alone"
R = c["search"]
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], pno=pno, cello=cello, strings=strings,
           total_eighths=TOT, slot="eighth", seconds=secs, singers=dict(her=dict(lo=62, top=81)), singer_by_sec=L.SINGER, stop_at=None,
           nc_bar=NC_BAR, mary=dict(on=MARY["on"], dur=MARY["dur"], bar=next(i for i, b in enumerate(bars) if b["start"] == MARY_AT) + 1),
           hush_bar=HUSH, meas={k_: (float(v_) if isinstance(v_, (int, float)) else v_) for k_, v_ in c["meas"].items()}, hand_edits=c["hand"],
           from_fp=c["from"], fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"],
           deaths=dict(sorted(R["deaths"].items(), key=lambda kv: -kv[1])), by_construction=c["by_construction"],
           qbpm={"6/8": M.QDEF, "Refrain 3": 72, "Coda": 66}, plans=c["plans"], cell_log=c["cell_log"],
           varied=VARIED, answers=ANSWERS, coda_phrase=[e["p"][0] for e in CODA_PHRASE])
pickle.dump(rec, open("/home/claude/p32/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", len(pno), "piano;", len(cello), "cello;",
      len(strings), "strings; fp", rec["fp"], "MARY bar", rec["mary"]["bar"], "N.C. bar", next(i for i, b in enumerate(bars) if b["start"] == NC_BAR) + 1)
