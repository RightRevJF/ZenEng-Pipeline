"""Terpsichore (song 56): the song record from melody_final.pkl (the pick of record) and the chart the run drew (438).
A Longing love song with Paradox's colour (V/L), a slow-burn soul ballad, E minor, q = 72, 4/4, 74 bars (the engine wrote it at q = 144 in
148 bars with a half-time feel; the record is written at 72: a bar of the record is two of the engine's, its ticks the engine's own, 24 to
the quarter). One singer, the baritone. The band (A): Hammond organ, a tremolo electric guitar answering in the gaps, bass, drums (brushes,
sticks for chorus 3); two backing voices answer 'come back' over his held B in chorus 3 and the outro.
The plan by section role (749.14, 749.16, 749.17, 9.12): each chorus above its verse, each return above the one before; the bridge (the
sensible chair) flat and low; the breath after it (749.19) on the organ alone; verse 3 re-enters fresh; the top at chorus 3; the outro
lets it go and ends open on C, never home.
  Intro: the guitar plays the hook; the organ holds; brushes and bass in at bar 3.   Verse 1: organ held low, brushes, the guitar answering.
  Chorus 1: the organ opens up, the guitar in eighths.   Verse 2: a little fuller.   Chorus 2: above chorus 1, a crash.
  Bridge: flat, low, rim and held bass.   Breath (2 bars): the organ alone.   Verse 3: fresh, brushes again.
  Chorus 3: sticks, ride, a crash on each line; the backing voices answer 'come back'.   Outro: down; the last 'Come back' held, answered.
  Ending: C (with the held B), ringing.
The bass is written for the groove: the root on 1 held to the kick, a step into each change; held in the bridge and the ending."""
import pickle, sys, random, collections
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p66"]
import io as _io, contextlib as _cl
with _cl.redirect_stdout(_io.StringIO()): import melody_l7_p66 as P
import bass_v134 as BV
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p66/melody_final.pkl", "rb")); c = F["pick"]
TPQ = 24; EB = 4 * TPQ; QB = 72; EBAR = 48                                   # the record: 24 ticks a quarter at 72 (the engine's 12 a quarter at 144)
NB = P.NBARS // 2
assert list(P.CHORD2) == list(F["run"]["chords2"]), "the chart on import differs from the run's"
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"never": ["nev", "er"], "hunger": ["hun", "ger"], "sternum": ["ster", "num"], "everywhere": ["ev", "ery", "where"], "beautiful": ["beau", "ti", "ful"],
        "anyway": ["an", "y", "way"], "burning": ["burn", "ing"], "nobody": ["no", "bod", "y"], "quiet": ["qui", "et"], "governor": ["gov", "er", "nor"],
        "needle": ["nee", "dle"], "interested": ["in", "terest", "ed"], "without": ["with", "out"], "Without": ["With", "out"], "pages": ["pa", "ges"],
        "inside": ["in", "side"], "dying": ["dy", "ing"], "little": ["lit", "tle"], "theologians": ["the", "o", "lo", "gians"], "around": ["a", "round"],
        "sensible": ["sen", "si", "ble"], "leaving's": ["leav", "ing's"], "ravishing": ["rav", "ish", "ing"], "after,": ["af", "ter,"], "pillow": ["pil", "low"],
        "only": ["on", "ly"], "body": ["bod", "y"], "remember": ["re", "mem", "ber"], "Everything": ["Ev", "ery", "thing"]}
def split_words(text, sy):
    out = []; ws = text.replace('"', "").split()
    for w in ws:
        n = len(P.syl(w)); core = w.rstrip(",;:?")
        if n <= 1: out.append((w, False)); continue
        parts = list(HFIX.get(w) or HFIX.get(core) or _PY.inserted(core).split("-"))
        tail = "" if w in HFIX else w[len(core):]
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        for j, p in enumerate(parts): out.append((p + (tail if j == n - 1 else ""), j < n - 1))
    assert len(out) == len(sy), (text, out, [x[0] for x in sy])
    return out
TEXT = {sec: [split_words(t, P.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in P.SUNG}
H2 = list(P.CHORD2)                                                          # the engine's half-bars: a beat of the record each
SEC0 = {}; bars = []
for nm, kind, nb2 in P.FORM:
    nb = nb2 // 2; SEC0[nm] = P.BAR0[nm] * EBAR
    for k in range(nb):
        b = P.BAR0[nm] // 2 + k; beats = H2[4 * b: 4 * b + 4]
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, b=b, meter="4/4", start=b * EB, len=EB, beats=beats, chord=beats[0], chord2=beats[2],
                         roman=M.ROMAN[beats[0].split("/")[0]], qbpm=QB, key="E minor", movement=nm, stop=False))
assert len(bars) == NB
REC_END = NB * EB
def singer_of(sec, i): return "him"
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); tx, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], on_engine=n["on"], dur=n["dur"], midi=n["p"], engine_midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"],
                     text=tx, hyph=hy, stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="him"))
CH = dict(M.CH)
def tones(ch): return CH[ch.split("/")[0]][1]
def chord_at_rec(t_): return H2[min(len(H2) - 1, t_ // TPQ)]
# ---- the backing voices (A): 'come back' answered over his held B in chorus 3 and the outro ----
harm = []
def answer(sec, line, U):
    for j, (t, ps, w) in enumerate(((144, (64, 67), "come"), (168, (62, 67), "back"))):
        for v, p in enumerate(ps):
            harm.append(dict(on=U + t, dur=22, midi=p, engine_midi=p, sec=sec, line=line, syl=100 + j, first=v == 0, text=w, hyph=False, stress=True,
                             role="answer", singer="harmony"))
for line in (0, 3): answer("Chorus 3", line, P.line_start("Chorus 3", line))
answer("Tag", 4, P.line_start("Tag", 4))
# ---- the band ----
parts = collections.defaultdict(list)
def ev(part, on, dur, p, vel, art="", **kw): parts[part].append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=int(max(1, min(127, vel))), art=art, **kw))
DR = dict(kick=36, snare=38, rim=37, hat=42, ohat=46, ride=51, crash=49, tom_hi=48, tom_mid=45, tom_lo=41)
LOW914 = {1: 60, 2: 60, 3: 53, 4: 53, 5: 46, 6: 47, 7: 34, 8: 41, 9: 41, 10: 41, 11: 41}     # Module 9.14: no second below C4, no third below F3 (749.21)
def root_at(ch, lo): return lo + (BV.bass_pc(ch) - lo) % 12
def stack(ch, lo, n, hi=80, root=True):
    """a voicing inside Module 9.14's low-interval limits: (the root at the bottom,) then each chord tone the limits allow above the last."""
    q = root_at(ch, lo) if root else lo - 1
    if not root:
        q += 1
        while q % 12 not in tones(ch): q += 1
    out = [q]
    while len(out) < n and q < hi:
        q += 1
        if q % 12 not in tones(ch): continue
        iv = q - out[-1]
        if iv >= 12 or out[-1] >= LOW914[iv]: out.append(q)
    return out
LEVEL = {"Intro": 0.40, "Verse 1": 0.30, "Chorus 1": 0.55, "Verse 2": 0.38, "Chorus 2": 0.66, "Bridge": 0.30, "Breath": 0.15, "Verse 3": 0.45,
         "Chorus 3": 0.90, "Tag": 0.55, "Ending": 0.35}                       # the plan by section role (749.17): each return above the one before
def V(sec, base=52, span=44): return base + int(round(span * LEVEL[sec]))
def changes(x):
    """the record bar's chord changes: (offset, length, chord), a beat (24 ticks) at a time."""
    out = []
    for j, ch in enumerate(x["beats"]):
        if out and out[-1][2] == ch: out[-1][1] += TPQ
        else: out.append([j * TPQ, TPQ, ch])
    return out
def organ(x, vel, lo=52, n=4, hi=70, upper=False, low=False):
    for off, L, ch in changes(x):
        vc = stack(ch, 45 if low else lo, n, hi=60 if low else hi)
        ev("organ", x["start"] + off, L, vc, vel)
        if upper: ev("organ", x["start"] + off, L, stack(ch, 64, 3, hi=79, root=False), vel - 10)
VON = collections.Counter(n["on"] // TPQ for n in lead)
VSPAN = set()
for n in lead:
    for t_ in range(n["on"] // 6, (n["on"] + n["dur"]) // 6 + 1): VSPAN.add(t_)                # the voice's sounding sixteenths
def quiet(t0, t1): return not any(t_ in VSPAN for t_ in range(t0 // 6, t1 // 6))
def gtr_answer(t0, ch, vel, rng, n=3):
    """a short tremolo figure in a gap of the voice: n eighths down the chord's tones from near E5, never under a sung word."""
    ts = sorted(q for q in range(62, 77) if q % 12 in tones(ch))[::-1]
    k = rng.randrange(0, 2); seq = ts[k:k + n]
    for j, q in enumerate(seq): ev("guitar", t0 + 12 * j, 12 if j < n - 1 else 24, q, vel - 3 * j, art="trem")
def gtr_eighths(x, vel):
    for off, L, ch in changes(x):
        ts = stack(ch, 52, 5, hi=71)
        for e in range(0, L, 12): ev("guitar", x["start"] + off + e, 12, ts[(e // 12) % len(ts)], vel - (6 if e % 24 else 0), art="trem")
def groove(st, vel, brush=True, ride=False, fill=False, rim=False, kick=True):
    """the half-time soul groove at 72 (the engine's 144 felt in half): kick on 1 and the and of 3, the backbeat on 2 and 4, eighths over it."""
    for e in range(0, EB, 12):
        if kick and e in (0, 60): ev("drums", st + e, 6, DR["kick"], vel - (8 if e else 0))
        if e in (24, 72): ev("drums", st + e, 6, DR["rim" if rim else "snare"], vel - (14 if brush else 0))
        if fill and e >= 72: continue
        ev("drums", st + e, 6, DR["ride" if ride else "hat"], vel - (30 if brush else 24) + (6 if e % 24 == 0 else 0))
    if fill:
        for j, (e, d) in enumerate(((72, "snare"), (78, "snare"), (84, "tom_hi"), (87, "tom_mid"), (90, "tom_lo"), (93, "tom_lo"))): ev("drums", st + e, 3, DR[d], vel - 10 + 2 * j - (10 if brush else 0))
def crash(st, vel): ev("drums", st, 12, DR["crash"], vel)
HOOKN = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]
rng = random.Random("song 56 band")
line_starts = {P.line_start(s_, i_) for s_ in P.SUNG for i_ in range(len(P.LINES[s_]))}
BREATH0 = P.BAR0["Breath"] // 2; TAG0 = P.BAR0["Tag"] // 2
for x in bars:
    sec, kind, st, k, nb = x["sec"], x["kind"], x["start"], x["k"], x["n"]
    ch = x["chord"]; last_bar = k == nb - 1; v = V(sec)
    if sec == "Intro":
        organ(x, v - 6)
        if k == 0:                                                                     # the guitar plays the hook an octave up (G4 B4, D5 B4)
            U = P.line_start("Chorus 1", 0)
            for n in HOOKN: ev("guitar", st + (n["on"] - U), n["dur"], n["midi"] + 12, v + 6, art="trem")
        if k >= 2: groove(st, v - 6, fill=last_bar)
    elif kind == "Verse":
        organ(x, v - (4 if sec != "Verse 1" else 8), upper=sec == "Verse 3")
        groove(st, v - 4, fill=last_bar)
        for half in (48, 72) if sec != "Verse 1" else (72,):
            ch_ = x["beats"][half // TPQ]
            if quiet(st + half, st + half + 36) and rng.random() < (0.5 if sec == "Verse 1" else 0.7): gtr_answer(st + half, ch_, v - 6, rng); break
    elif kind == "Chorus":
        organ(x, v - 2, n=5, upper=True)
        groove(st, v, brush=sec != "Chorus 3", ride=sec == "Chorus 3", fill=last_bar)
        if k == 0 and sec != "Chorus 1": crash(st, v + 8)
        if sec == "Chorus 3" and any(st <= t_ < st + EB for t_ in line_starts): crash(st, v + 4)
        gtr_eighths(x, v - 14 if sec == "Chorus 1" else v - 10)
    elif sec == "Bridge":                                                              # the sensible chair: flat and low, rim, held bass
        organ(x, v - 2, low=True); groove(st, v - 6, rim=True, kick=k % 2 == 0)
    elif sec == "Breath":                                                              # 749.19: the organ alone
        ev("organ", st, EB, stack(ch, 52, 4, hi=66), v + 6 - 6 * k)
    elif sec == "Tag":
        organ(x, v - 4, upper=k >= 4)
        if k < 4: groove(st, v - 8 - 4 * k, fill=False)
        elif k == 4: crash(st, v); ev("drums", st, 6, DR["kick"], v)
    elif sec == "Ending":
        ev("organ", st, EB, [48, 55, 59, 64, 67], v - 8 * k); ev("organ", st, EB, [71, 76], v - 14 - 8 * k)   # C with the held B, ringing (open)
        if k == 0: ev("guitar", st + 24, 72, [71, 76], v - 10, art="trem")
# ---- the bass: written for the groove at 72 (the routine's cells are drawn at the engine's 144 and would run sixteenths here) ----
SC = {4, 6, 7, 9, 11, 0, 2}
def approach(nxt_root, prev):
    """the note a step below or above the next root, in the key, nearest the last note."""
    c_ = [q for q in (nxt_root - 1, nxt_root - 2, nxt_root + 1, nxt_root + 2) if q % 12 in SC and 28 <= q <= 52]
    return min(c_, key=lambda q: abs(q - prev)) if c_ else nxt_root
BASS_REST = set()
for bi, x in enumerate(bars):
    sec, st, k = x["sec"], x["start"], x["k"]
    if sec == "Breath" or (sec == "Intro" and k < 2): continue
    v = V(sec) - 2; chs = changes(x); hold = sec in ("Bridge", "Ending") or (sec == "Tag" and k >= 4)
    nxt = bars[bi + 1]["beats"][0] if bi + 1 < NB else None
    for j, (off, L, ch) in enumerate(chs):
        r = root_at(ch, 33) if root_at(ch, 33) <= 45 else root_at(ch, 33) - 12
        if hold or L < 48: ev("bass", st + off, L - 2, r, v); continue
        ev("bass", st + off, min(L, 60) - 2 if L > 60 else L - 14, r, v)                              # the root on 1, held to the kick
        if off + 60 < off + L: ev("bass", st + off + 60, 12, r + 12 if (r + 12) <= 52 and rng.random() < 0.5 else r, v - 8)   # with the kick on the and of 3
        last = j == len(chs) - 1
        if last and nxt and off + L == EB and sec not in ("Ending",) and rng.random() < (0.8 if x["kind"] == "Chorus" else 0.55):
            tgt = root_at(nxt, 33) if root_at(nxt, 33) <= 45 else root_at(nxt, 33) - 12
            ev("bass", st + 84, 12, approach(tgt, r), v - 6)                                            # a step into the next chord
tries = "written for the groove (no routine)"
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"] and out[-1]["art"] == e["art"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); out[-1]["dur"] = max(out[-1]["dur"], e["dur"]); continue
        out.append(e)
    return out
PARTS = {k: tidy(v) for k, v in parts.items()}
for e in PARTS["guitar"]:                                                             # nothing overruns the record
    e["dur"] = min(e["dur"], REC_END - e["on"])
plan = [(nm, nb // 2, SEC0[nm], ["4/4"] * (nb // 2), nm) for nm, kind, nb in P.FORM]
secs = sum(x["len"] / TPQ * 60 / x["qbpm"] for x in bars)
rec = dict(title="Terpsichore", file_title="Terpsichore", nbars=NB, bars=bars, chords2=H2, chords_by_beat=H2, tpq=TPQ, plan=plan, lead=lead, harm=harm,
           parts=PARTS, slot="twenty-fourth of a beat (the engine's twelfth at 144)", qbpm=QB, engine_qbpm=144, feel=P.FEEL, seconds=secs, end=REC_END, level=LEVEL,
           fp=c["fp"], order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"],
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, judge={k: c["judge"][k] for k in ("combined", "content", "order")},
           plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"], kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()},
           rerun=F["run"]["rerun"], text=TEXT, registers=c["meta"]["registers"], carriers=c["meta"]["carriers"],
           design=dict(gates=P.DESIGN_GATES, hook=P.HOOK, hook_tag=P.HOOK_T, half_bars={f"{a}:{b}": v for (a, b), v in P.DESIGN_HALF.items()},
                       slots={s: P.slots_of(s) for s in P.SUNG}),
           chart438=F["run"]["rerun"].get("chart438"), bass_written_by="build_p66.py: the root on 1 held to the kick on the and of 3, a step into the next chord (the routine's 144 cells would run sixteenths at 72)", bass_tries=tries,
           breath=dict(bar=BREATH0, at=BREATH0 * EB, rule="749.19: after the bridge, two bars of the organ alone; verse 3 re-enters"),
           outro=dict(bar=TAG0, rule="the outro's last 'Come back' over a crash and the organ, the backing voices answering; the ending on C, open"))
pickle.dump(rec, open("/home/claude/p66/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{secs % 60:04.1f});", len(lead), "sung;", {k: len(v) for k, v in PARTS.items()}, "other voices", len(harm), "bass tries", tries)
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t_ + ("-" if h else "") for t_, h in ws))
