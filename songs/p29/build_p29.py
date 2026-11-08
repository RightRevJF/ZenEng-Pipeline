"""Build the song record for 'The Breath That Made the World' from the frozen melody (melody_final.pkl). A concert carol: one high voice (written
for soprano; a tenor an octave lower), piano, cello, strings. Times in EIGHTHS; 3/4 (a bar = 6) at q = 66, the final refrain and coda
broadened to q = 56. D-flat major; E-flat from verse 4.
  piano      the cradle figure: the left hand in flowing eighths, root-fifth-tenth-octave-tenth-fifth (verse 1 thinner: root, fifth,
             tenth on 1-2-3); the right hand a chord on beat 1, held, from refrain 1; in verse 4 and the last refrain both hands full
  cello      from verse 2: the root a bar, held; in verses 2 and 3 it ANSWERS each line (revision 1): the line's last three notes an
             octave below, in eighths, after the singer lands, ending by the next line's downbeat; in the INTERLUDE it sings refrain 1's tune an octave below the voice, at
             half voice -- her lullaby -- with ONE note changed (revision 1): WORLD rises to F4 instead of D-flat4; from the bridge a held
             bass line
  strings    a soft pad under the refrains; the interlude's last two bars swell (the lift toward the bridge); the bridge builds;
             verse 4 and the last refrain full, a held top line in the last refrain
  anchors    MA (verse 3): no new note under it -- the accompaniment holds and nothing moves. ABBA (the bridge): the whole band
             silent for its bar; AND JOSEPH TURNS: everyone back on B-flat, the pivot into E-flat
  the end    the last refrain thins under 'goes in, and out, and in': piano and strings pianissimo, the voice's last IN on B-flat4 over
             B-flat left open; the coda (revision 1): the piano alone states the refrain's first phrase in E-flat (C5 C5 C5 B-flat4 C5 | F5, over
             A-flat and F minor), then E-flat, and the last chord E-flat with an added F, B-flat4 on top -- the pitch of MA -- let ring."""
import pickle, sys
sys.path[:0] = ["/home/claude/p29"]
import melody_p29 as M, lyric as L
c = pickle.load(open("/home/claude/p29/melody_final.pkl", "rb"))
R = pickle.load(open("/home/claude/p29/melody_result.pkl", "rb"))
bars = []
for i, b in enumerate(M.BARS):
    k = sum(1 for x in M.BARS[:i] if x["sec"] == b["sec"])
    key = "Eb major" if b["sec"] in ("Verse 4", "Refrain 3", "Coda") else "Db major"
    bars.append(dict(sec=b["sec"], meter="3/4", chord=b["chord"], start=b["start"], len=6, qbpm=M.QBPM.get(b["sec"], 66), k=k, key=key,
                     instrumental=b["sec"] in ("Intro", "Interlude", "Coda")))
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=M.SECS[s][li]["role"], meter="3/4", singer="her"))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL
secs = sum(6 * 60 / b["qbpm"] / 2 for b in bars)
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, "3/4"))
ROOT = {"Db": 1, "Gb": 6, "Ab": 8, "Bbm": 10, "Fm": 5, "Ebm": 3, "Bb": 10, "Eb": 3, "Cm": 0, "Gm": 7, "F": 5}
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
ABBA = next(b for b in bars if b["sec"] == "Bridge" and b["k"] == 6)["start"]           # the bridge's seventh bar: the band silent
MA = next(n for n in lead if n["sec"] == "Verse 3" and n["syl"][0] == "ma")
DYN = {"Intro": 50, "Verse 1": 46, "Refrain 1": 58, "Verse 2": 54, "Refrain 2": 64, "Interlude": 52, "Verse 3": 56, "Bridge": 62,
       "Verse 4": 74, "Refrain 3": 84, "Coda": 50}
R1 = [n for n in lead if n["sec"] == "Refrain 1"]
for bi, b in enumerate(bars):
    sec, ch, st, k = b["sec"], b["chord"], b["start"], b["k"]
    if st == ABBA: continue                                                   # ABBA: the whole band silent for its bar
    v = DYN[sec] + (2 * k if sec in ("Bridge", "Refrain 3") and k < 4 else 0)
    r = at_or_above(ROOT[ch], 36)                                             # C2-B2
    fifth = r + 7; tenth = at_or_above(THIRD[ch], r + 12); octv = r + 12
    last = sec == "Refrain 3" and k >= 6
    # ---- piano ----
    if sec == "Coda":                                                          # revision 1: the refrain's first phrase returns, then the open chord
        if k < 2: pno.append(dict(on=st, dur=6, p=[r, fifth], vel=46 - 3 * k, hand="lh", art="ring"))
        elif k == 2: pno.append(dict(on=st, dur=6, p=[r, fifth] + voicing(ch, 60), vel=44, hand="both", art="ring"))
        else: pno.append(dict(on=st, dur=6, p=[r, fifth, 63, 65, 67, 70], vel=42, hand="both", art="ring"))   # E-flat with an added F, B-flat4 on top
        continue
    if sec == "Verse 1":
        pno += [dict(on=st + e, dur=2, p=[q], vel=v - (0 if e == 0 else 6), hand="lh", art="") for e, q in zip((0, 2, 4), (r, fifth, tenth))]
    else:
        fig = [r, fifth, tenth, octv, tenth, fifth]
        pno += [dict(on=st + e, dur=1, p=[q], vel=v - (0 if e == 0 else 8), hand="lh", art="") for e, q in enumerate(fig)]
    if sec not in ("Intro", "Verse 1", "Verse 2", "Verse 3", "Interlude") or (sec == "Intro" and k in (0, 2)):
        rh = voicing(ch, 65 if sec not in ("Verse 4", "Refrain 3") else 67, 3 if not last else 2)
        pno.append(dict(on=st, dur=6, p=rh, vel=v - 6 - (14 if last else 0), hand="rh", art="ring"))
    # ---- cello ----
    if sec == "Interlude":
        pass                                                                  # the lullaby, written below
    elif sec in ("Verse 2", "Refrain 2", "Verse 3", "Bridge", "Verse 4") or (sec == "Refrain 3" and not last):
        cello.append(dict(on=st, dur=6, p=[r + 12 if r + 12 <= 52 else r], vel=v - 4, art=""))
    # ---- strings ----
    if sec in ("Refrain 1", "Refrain 2", "Bridge", "Verse 4", "Refrain 3") or (sec == "Interlude" and k >= 6):
        pad = voicing(ch, 55, 3)
        sv = v - 10 + (8 * (k - 5) if sec == "Interlude" else 0)
        if sec == "Refrain 3" and not last: pad = pad + [voicing(ch, 72, 1)[0]]
        strings.append(dict(on=st, dur=6, p=pad, vel=max(30, sv - (16 if last else 0)), art="pad"))
# the interlude: the cello sings refrain 1's tune an octave below the voice, at half voice (her lullaby), one note changed (revision 1):
# WORLD (line 3's second downbeat, over D-flat) rises from D-flat4 to F4 -- a familiar phrase with exactly one element changed
d = M.STARTS["Interlude"][1] - M.STARTS["Refrain 1"][1]
VARIED = None
for n in R1:
    if M.STARTS["Interlude"][1] <= n["on"] + d < M.STARTS["Interlude"][1] + 36:
        p = n["midi"] - 12
        if n["line"] == 2 and n["syl"][0] == "world": p = 65; VARIED = dict(on=n["on"] + d, was=n["midi"] - 12, now=65)
        cello.append(dict(on=n["on"] + d, dur=n["dur"], p=[p], vel=54, art="lullaby"))
assert VARIED and next(b for b in bars if b["start"] <= VARIED["on"] < b["start"] + 6)["chord"] == "Db"
# verses 2 and 3: the cello answers each line (revision 1) -- the line's last three notes an octave below, in eighths, from the eighth
# after the singer's last note begins; it ends by the next line's first downbeat (under its pickup); the held root gives way for that bar
ANSWERS = []
lines_ = {}
for n in lead: lines_.setdefault((n["sec"], n["line"]), []).append(n)
for (sec_, li), ns in lines_.items():
    if sec_ not in ("Verse 2", "Verse 3"): continue
    if sec_ == "Verse 3" and li == 3: continue                                # MA: nothing moves under it, and the bridge follows
    t = ns[-1]["on"] + 1
    stop = M.SECS[sec_][li]["at"] + 12                                         # by the next line's first downbeat (under its pickup, an octave down)
    figure = [x["midi"] - 12 for x in ns[-3:]]
    if t + 3 > stop: continue
    bar0 = next(b for b in bars if b["start"] <= t < b["start"] + 6)["start"]
    cello = [e for e in cello if not (e["on"] == bar0 and e["art"] == "")] + ([dict(on=bar0, dur=t - bar0, p=[e["p"][0] for e in cello if e["on"] == bar0 and e["art"] == ""][0:1] or [figure[0]], vel=50, art="")] if t > bar0 else [])
    cello += [dict(on=t + j, dur=1 if j < 2 else max(1, min(2, stop - (t + 2))), p=[q], vel=56, art="answer") for j, q in enumerate(figure)]
    ANSWERS.append(dict(sec=sec_, line=li, on=t, figure=figure))
cello.sort(key=lambda e: e["on"])
# the coda: the piano's right hand states the refrain's first phrase in E-flat (refrain 3's title line, the voice's own notes), then rests
CODA0 = next(b["start"] for b in bars if b["sec"] == "Coda")
T3 = [n for n in lead if n["sec"] == "Refrain 3" and n["line"] == 0]
at0 = M.SECS["Refrain 3"][0]["at"]
CODA_PHRASE = [dict(on=CODA0 + (n["on"] - at0), dur=n["dur"] if i < len(T3) - 1 else 6, p=[n["midi"]], vel=50, hand="rh", art="coda") for i, n in enumerate(T3)]
assert CODA_PHRASE[0]["on"] >= max(n["on"] + n["dur"] for n in lead), "the coda's pickup clears the voice"
pno += CODA_PHRASE; pno.sort(key=lambda e: e["on"])
# MA: nothing moves under it -- drop every accompaniment onset inside the held note
ma0, ma1 = MA["on"], MA["on"] + MA["dur"]
pno = [e for e in pno if not (ma0 < e["on"] < ma1)]; cello = [e for e in cello if not (ma0 < e["on"] < ma1)]
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], pno=pno, cello=cello, strings=strings,
           total_eighths=TOT, slot="eighth", seconds=secs, singers=dict(her=dict(lo=60, top=82)), singer_by_sec=L.SINGER, stop_at=None,
           abba_bar=ABBA, ma=dict(on=MA["on"], dur=MA["dur"]),
           meas={k_: (float(v_) if isinstance(v_, (int, float)) else v_) for k_, v_ in c["meas"].items()}, hand_edits=c["hand"], from_fp=c["from"],
           fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()),
           by_construction=R["by_construction"], qbpm={"3/4": 66, "final": 56}, plans=c["plans"], cell_log=c["cell_log"],
           revision=c.get("revision", 0), varied=VARIED, answers=ANSWERS, coda_phrase=[e["p"][0] for e in CODA_PHRASE], ossia=dict(word="world", sec="Refrain 3", note=80))
pickle.dump(rec, open("/home/claude/p29/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", len(pno), "piano;", len(cello), "cello;",
      len(strings), "strings; fp", rec["fp"])
