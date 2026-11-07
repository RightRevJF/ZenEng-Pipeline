"""Build the song record for 'Through Its Breaking' from the frozen melody (melody_final.pkl: ranking #1, 255b01910113, with one hand
edit logged). One female voice; piano, cello, strings. Times in eighths, 6/8 felt in two at dotted-q = 54 (a bar = 6 eighths).
  piano      the 6/8 ballad figure: the left hand R-5-8-10-8-5 in eighths (verse 1 thinner: R held, 5-8-10 on beat 2);
             the chorus adds a right-hand chord on beat 1, held a dotted half
  the bell   (on the piano) a low octave toll on the downbeat, and on beat 2 the crack: the chord's root with the half step below
             it struck together (Am: A4+G#4; C: C5+B4; F: F4+E4; G: G4+F#4; Dm: D5+C#5; E: E4+D#4), let ring. Intro, the
             interludes, the second half of the bridge, the tag and the outro.
  cello      from verse 2: the root a bar, held; chorus 2 and 3 a dotted-quarter answer on beat 2 (the fifth)
  strings    chorus 2 a held pad; the bridge builds (bars 1-4 out, 5-8 one held line, 9-16 the pad, swelling); chorus 3 full;
             out for the tag; back for the last bar (C)
  chorus 3   the bell joins: the toll every bar, the crack on beat 2 -- the wrong bell, rung through the last chorus
  the end    the outro's last bar: C held, and B4 against C5 left ringing -- the crack, unresolved."""
import pickle, sys
sys.path[:0] = ["/home/claude/p25"]
import melody_p25 as M, lyric as L
c = pickle.load(open("/home/claude/p25/melody_final.pkl", "rb"))
R = pickle.load(open("/home/claude/p25/melody_result.pkl", "rb"))
QB = 54
BELL_SECS = ("Intro", "Interlude 1", "Interlude 2", "Tag", "Outro")
bars = []
for b in M.BARS:
    k = sum(1 for x in M.BARS[:M.BARS.index(b)] if x["sec"] == b["sec"])
    key = "C major" if b["sec"].startswith("Chorus") or b["sec"] in ("Tag", "Outro") else "A minor"
    bars.append(dict(sec=b["sec"], meter="6/8", chord=b["chord"], start=b["start"], len=b["len"], qbpm=QB, key=key, k=k,
                     build=b["sec"] == "Bridge", instrumental=b["sec"] in ("Intro", "Interlude 1", "Interlude 2", "Outro"),
                     bell=b["sec"] in BELL_SECS or (b["sec"] == "Bridge" and k >= 8) or b["sec"] == "Chorus 3"))
lead = []
for s in M.SINGS:
    for o, d, p, x, li in c[s]:
        lead.append(dict(on=o, dur=d, midi=p, syl=x, sec=s, line=li, role=M.SECS[s][li]["role"], meter="6/8", singer="her"))
lead.sort(key=lambda n: n["on"])
TOT = M.TOTAL; secs = TOT * 60 / QB / 3
plan = []
for sec, met, scale, lines, chs in M.FORM:
    b0 = next(i for i, b in enumerate(bars) if b["sec"] == sec); nb = sum(1 for b in bars if b["sec"] == sec)
    plan.append((sec, nb, b0, met))
ROOT = {"Am": 9, "F": 5, "C": 0, "G": 7, "E": 4, "Em": 4, "Dm": 2}
TONES = M.CH
def at_or_above(pc, lo):
    p = lo
    while p % 12 != pc: p += 1
    return p
def third(ch): return [t for t in TONES[ch] if (t - ROOT[ch]) % 12 in (3, 4)][0]
def fifth(ch): return (ROOT[ch] + 7) % 12
def lh(ch):
    r = at_or_above(ROOT[ch], 40)                         # the root E2-D#3
    return dict(R=r, F5=r + 7, O=r + 12, T=at_or_above(third(ch), r + 13))
def rh(ch, top=67):
    out, p = [], top
    while len(out) < 3:
        if p % 12 in TONES[ch]: out.append(p)
        p -= 1
    return sorted(out)
def crack(ch):
    r = at_or_above(ROOT[ch], 64)
    return [r - 1, r]
def toll(ch):
    r = at_or_above(ROOT[ch], 28)
    return [r, r + 12]
pno, bell, cel, strg = [], [], [], []
for bi, b in enumerate(bars):
    sec, ch, st, k = b["sec"], b["chord"], b["start"], b["k"]
    nsec = sum(1 for x in bars if x["sec"] == sec)
    last = bi == len(bars) - 1
    L_ = lh(ch)
    # ---- the bell ----
    if b["bell"]:
        bv = dict(Intro=50, Tag=46, Outro=42).get(sec, 44)
        if sec == "Bridge": bv = 48 + (k - 8) * 2
        if sec == "Chorus 3": bv = 64                       # inside the bridge it climbs with the strings
        if not (sec == "Outro" and k in (1, 3)) or last:
            bell.append(dict(on=st, dur=6, p=toll(ch), vel=bv, art="ring", kind="toll"))
        if not last and not (sec == "Outro" and k == 2):
            nxt_bell = bi + 1 < len(bars) and bars[bi + 1]["bell"]
            bell.append(dict(on=st + 3, dur=6 if (nxt_bell and sec != "Bridge") else 3, p=crack(ch), vel=bv - 10, art="ring", kind="crack"))
    if last:
        pno.append(dict(on=st, dur=6, p=[L_["R"], L_["F5"], L_["O"], L_["T"]], vel=46, art="ring", hand="lh"))
        bell.append(dict(on=st + 3, dur=3, p=[71, 72], vel=44, art="ring", kind="crack"))     # B against C, left ringing
        continue
    # ---- the piano ----
    if sec in ("Intro", "Interlude 1", "Interlude 2", "Outro"):
        if sec != "Outro" or k == 0:
            pno.append(dict(on=st, dur=6, p=[L_["R"], L_["F5"]], vel=40, art="ring", hand="lh"))
    elif sec == "Tag":
        pno.append(dict(on=st, dur=6, p=[L_["R"], L_["F5"], L_["O"]], vel=38, art="ring", hand="lh"))
    elif sec == "Verse 1":
        pno.append(dict(on=st, dur=6, p=[L_["R"]], vel=48, art="ring", hand="lh"))
        pno.append(dict(on=st + 3, dur=3, p=[L_["F5"], L_["O"], L_["T"]], vel=40, art="", hand="lh"))
    else:
        bridge_thin = sec == "Bridge" and k < 4
        full = sec in ("Chorus 2", "Chorus 3") or (sec == "Bridge" and k >= 8)
        base = dict(Verse=46, Chorus=52, Bridge=46 + k)[sec.split()[0]] + (4 if sec == "Chorus 3" else 0)
        pat = ["R", "F5", "O", "T", "O", "F5"]
        for e, w in enumerate(pat):
            if bridge_thin and e in (1, 4): continue
            pno.append(dict(on=st + e, dur=1, p=[L_[w]], vel=base - (0 if e in (0, 3) else 6), art="", hand="lh"))
        if sec.startswith("Chorus") or full:
            pno.append(dict(on=st, dur=6, p=rh(ch, 67), vel=base - 8, art="", hand="rh"))
    # ---- the cello ----
    if sec in ("Verse 2", "Chorus 2", "Bridge", "Chorus 3", "Tag", "Interlude 2") or (sec == "Chorus 1" and k >= 4):
        r = at_or_above(ROOT[ch], 36)
        if sec in ("Chorus 2", "Chorus 3"):
            cel.append(dict(on=st, dur=3, p=[r], vel=58 + (8 if sec == "Chorus 3" else 0), art=""))
            cel.append(dict(on=st + 3, dur=3, p=[at_or_above(fifth(ch), r)], vel=52, art=""))
        else:
            cel.append(dict(on=st, dur=6, p=[r], vel=dict(Bridge=46 + k, Tag=44).get(sec, 50), art=""))
    # ---- the strings ----
    if sec == "Chorus 2":
        strg.append(dict(on=st, dur=6, p=rh(ch, 64), vel=44, art=""))
    elif sec == "Bridge" and 4 <= k < 8:
        strg.append(dict(on=st, dur=6, p=[at_or_above(third(ch), 52)], vel=36 + 2 * (k - 4), art=""))
    elif sec == "Bridge" and k >= 8:
        strg.append(dict(on=st, dur=6, p=rh(ch, 67), vel=46 + 2 * (k - 8), art=""))
    elif sec == "Chorus 3":
        strg.append(dict(on=st, dur=6, p=rh(ch, 67) + [at_or_above(ROOT[ch], 72)], vel=70, art=""))
rec = dict(title=L.TITLE, nbars=len(bars), bars=bars, plan=plan, lead=lead, harm=[], pno=pno, bell=bell, cello=cel, strings=strg,
           total_eighths=TOT, seconds=secs, singers=dict(her=M.HER), singer_by_sec=L.SINGER,
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, hand_edits=c["hand"], from_fp=c["from"],
           fp=c["fp"], order_fp=R["order_fp"], survivors=R["survivors"], built=R["made"], attempts=R["tries"], deaths=dict(R["deaths"].most_common()),
           by_construction=R["by_construction"], qbpm={"6/8": QB}, eighth_sec={"6/8": 60 / QB / 3}, plans=c["plans"], cell_log=c["cell_log"])
pickle.dump(rec, open("/home/claude/p25/song_record.pkl", "wb"))
print(rec["nbars"], "bars,", f"{secs:.0f} s ({int(secs//60)}:{int(round(secs%60)):02d});", len(lead), "sung;", len(pno), "piano;", len(bell), "bell;",
      len(cel), "cello;", len(strg), "strings; fp", rec["fp"])
