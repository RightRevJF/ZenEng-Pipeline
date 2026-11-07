"""Build the song record for 'The Word Without a Word' from the frozen melody (melody_final.pkl). A concert carol: one high voice (written
for soprano; a tenor an octave lower), piano, cello, strings. Times in EIGHTHS; 3/4 (a bar = 6) at q = 66, the final refrain and coda
broadened to q = 56. D-flat major; E-flat from verse 4.
  piano      the cradle figure: the left hand in flowing eighths, root-fifth-tenth-octave-tenth-fifth (verse 1 thinner: root, fifth,
             tenth on 1-2-3); the right hand a chord on beat 1, held, from refrain 1; in verse 4 and the last refrain both hands full
  cello      from verse 2: the root a bar, held; in the INTERLUDE it sings refrain 1's tune an octave below the voice, at half voice --
             her lullaby; from the bridge a held bass line
  strings    a soft pad under the refrains; the interlude's last two bars swell (the lift toward the bridge); the bridge builds;
             verse 4 and the last refrain full, a held top line in the last refrain
  anchors    MA (verse 3): no new note under it -- the accompaniment holds and nothing moves. ABBA (the bridge): the whole band
             silent for its bar; AND JOSEPH TURNS: everyone back on B-flat, the pivot into E-flat
  the end    the last refrain thins under 'goes in, and out, and in': piano and strings pianissimo, the voice's last IN on B-flat4 over
             B-flat left open; the coda: the piano alone, A-flat, F minor, E-flat, the last chord E-flat with an added F, let ring."""
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
    if sec == "Coda":
        if k < 3: pno.append(dict(on=st, dur=6, p=[r, fifth] + voicing(ch, 60), vel=48 - 3 * k, hand="both", art="ring"))
        else: pno.append(dict(on=st, dur=6, p=[r, fifth, 63, 65, 67, 70], vel=42, hand="both", art="ring"))   # E-flat with an added F
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
# the interlude: the cello sings refrain 1's tune an octave below the voice, at half voice (her lullaby)
d = M.STARTS["Interlude"][1] - M.STARTS["Refrain 1"][1]
for n in R1:
    if M.STARTS["Interlude"][1] <= n["on"] + d < M.STARTS["Interlude"][1] + 36:
        cello.append(dict(on=n["on"] + d, dur=n["dur"], p=[n["midi"] - 12], vel=54, art="lullaby"))
# MA: nothing moves under it -- drop every accompaniment onset inside the held note
ma0, ma1 = MA["on"], MA["on"] + MA["dur"]
pno = [e for e in pno if not (ma0 < e["on"] < ma1)]; cello = [e for e in cello if not (ma0 < e["on"] < ma1)]
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], pno=pno, cello=cello, strings=strings,
           total_eighths=TOT, slot="eighth", seconds=secs, singers=dict(her=dict(lo=60, top=82)), singer_by_sec=L.SINGER, stop_at=None,
           abba_bar=ABBA, ma=dict(on=MA["on"], dur=MA["dur"]),
           meas={k_: (float(v_) if isinstance(v_, (int, float)) else v_) for k_, v_ in c["meas"].items()}, hand_edits=c["hand"], from_fp=c["from"],
           fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()),
           by_construction=R["by_construction"], qbpm={"3/4": 66, "final": 56}, plans=c["plans"], cell_log=c["cell_log"])
pickle.dump(rec, open("/home/claude/p29/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", len(pno), "piano;", len(cello), "cello;",
      len(strings), "strings; fp", rec["fp"])
