"""Your Yard Man (song 55): the song record from melody_final.pkl (the pick of record) and the chart the run drew (438).
A country story song with an anthem's chorus (N/A), a neotraditional two-step, A major, q = 120, 4/4, 102 bars (song 54's sound; the form, A).
One singer, the baritone. A harmony voice joins him on the call and the answer in every chorus and the tag (the anthem), and on chorus 3's
middle lines. The band (song 54's): acoustic guitar, Telecaster, fiddle, pedal steel, bass, drums (a two-step with sticks), a little piano.
The plan by section role (749.14, 749.16, 749.17, 9.12): each chorus above its verse, each return above the one before; verse 2 (his
daddy) pulled back; the break before verse 3 releases and ends thin (a breath, 749.19, at about 0.65), verse 3 re-enters fresh; the top
at chorus 3; the tag's call sung over a stop, the answer with the band, 'man' held.
  Intro: the fiddle plays the call and the answer; the band in, light.   Verse 1: boom-chick, cross-stick, the steel answering.
  Chorus 1: snare 2 and 4, a crash; strummed; steel swells; Telecaster fills.   Verse 2: pulled back, cross-stick, the steel holding.
  Chorus 2: piano in.   Break: the fiddle plays the call and the answer, the steel replies; its last bar the acoustic alone.
  Verse 3: piano chords for the pew, sticks from the lake.   Chorus 3: ride, the fiddle's long notes, harmony on more lines.
  Tag: the call over a stop; the answer with the band.   Ending: the fiddle's answer home; D to A, ringing.
The sung sections' bass is written by the routine (bass_v134.py) on the engine's grid; the intro, break and ending in root-five."""
import pickle, sys, random, collections
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p65"]
import io as _io, contextlib as _cl
with _cl.redirect_stdout(_io.StringIO()): import melody_l7_p65 as P
import bass_v134 as BV
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p65/melody_final.pkl", "rb")); c = F["pick"]
EB = 48; NB = P.NBARS; QB = 120
assert list(P.CHORD2) == list(F["run"]["chords2"]), "the chart on import differs from the run's"
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"quarter": ["quar", "ter"], "coffee": ["cof", "fee"], "Half-ton,": ["Half-", "ton,"], "half-ton": ["half-", "ton"], "trailer,": ["trail", "er,"],
        "trailer": ["trail", "er"], "mower": ["mow", "er"], "reflux": ["re", "flux"], "across": ["a", "cross"], "finished": ["fin", "ished"],
        "forty": ["for", "ty"], "hours": ["hou", "rs"], "stopwatch": ["stop", "watch"], "never": ["nev", "er"], "Never": ["Nev", "er"],
        "frightened": ["fright", "ened"], "Holland": ["Hol", "land"], "weeded": ["weed", "ed"], "enough": ["e", "nough"], "tulip": ["tu", "lip"],
        "daddy": ["dad", "dy"], "Daddy": ["Dad", "dy"], "Thirty-one": ["Thir", "ty-", "one"], "wouldn't": ["would", "n't"], "summers": ["sum", "mers"],
        "kitchen": ["kitch", "en"], "Watchin'": ["Watch", "in'"], "before": ["be", "fore"], "party": ["par", "ty"], "Sunday": ["Sun", "day"],
        "mower": ["mow", "er"], "Second": ["Sec", "ond"], "Preacher": ["Preach", "er"], "Glory": ["Glo", "ry"], "callin'": ["call", "in'"],
        "livin'": ["liv", "in'"], "nobody": ["no", "bod", "y"], "summons": ["sum", "mons"], "Paris": ["Par", "is"], "Couldn't": ["Could", "n't"],
        "anywhere": ["an", "y", "where"], "plumb": ["plumb"]}
def split_words(text, sy):
    out = []; ws = text.replace('"', "").split()
    for w in ws:
        n = len(P.syl(w)); core = w.rstrip(",;:?") if w != "a.m." else w
        if n <= 1: out.append((w, False)); continue
        parts = list(HFIX.get(w) or HFIX.get(core) or _PY.inserted(core).split("-"))
        tail = "" if w in HFIX else w[len(core):]
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        for j, p in enumerate(parts): out.append((p + (tail if j == n - 1 else ""), j < n - 1 and not p.endswith("-") and w != "a.m."))   # a.m.: two syllables, no hyphen
    assert len(out) == len(sy), (text, out, [x[0] for x in sy])
    return out
TEXT = {sec: [split_words(t, P.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in P.SUNG}
H2 = list(P.CHORD2)
bars = []; t = 0; RS = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, b=b, meter="4/4", start=t, len=EB, chord=H2[2 * b], chord2=H2[2 * b + 1],
                         roman=M.ROMAN[H2[2 * b]], qbpm=QB, key="A major", movement=nm, stop=False))
        RS.append(t); t += EB
REC_END = t
SEC0 = {nm: RS[P.BAR0[nm]] for nm, _, _ in P.FORM}
def singer_of(sec, i): return "him"                                          # one singer (the voice)
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); tx, hy = TEXT[sec][i][n["syl"]]; sg = singer_of(sec, i)
    lead.append(dict(on=n["on"], on_engine=n["on"], dur=n["dur"], midi=n["p"] + (12 if sg == "her" else 0), engine_midi=n["p"], sec=sec, line=i,
                     syl=n["syl"], first=not n["slur"], text=tx, hyph=hy, stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer=sg))
CH = dict(M.CH)
def tones(ch): return CH[ch][1]
def up_to(p, pcs, k=1):
    q = p
    for _ in range(k):
        q += 1
        while q % 12 not in pcs: q += 1
    return q
def down_to(p, pcs, k=1):
    q = p
    for _ in range(k):
        q -= 1
        while q % 12 not in pcs: q -= 1
    return q
def chord_at_rec(t_): b_ = bars[min(NB - 1, t_ // EB)]; return b_["chord2"] if t_ % EB >= 24 else b_["chord"]
# ---- the other voices: harmony on the hook (choruses 1-3) and chorus 3's middle lines; him under her hook; the tag's two voices ----
def third_above(n):
    ct = tones(chord_at_rec(n["on"]))
    return next((q for q in range(n["midi"] + 3, n["midi"] + 6) if q % 12 in ct), up_to(n["midi"], M.SCALE, 2))
def third_below(n):
    ct = tones(chord_at_rec(n["on"]))
    return next((q for q in range(n["midi"] - 3, n["midi"] - 6, -1) if q % 12 in ct), down_to(n["midi"], M.SCALE, 2))
harm = []
for n in lead:
    sec, i = n["sec"], n["line"]
    if (KIND_ := P.KIND[sec]) in ("Chorus", "Tag") and (n["role"] in ("hook", "tag") or (sec == "Chorus 3" and 1 <= i <= 3)):
        harm.append(dict(n, midi=third_above(n), singer="harmony"))                          # the anthem: a high harmony on the call and the answer, and chorus 3's lines 2-4
# ---- the band ----
parts = collections.defaultdict(list)
def ev(part, on, dur, p, vel, art="", **kw): parts[part].append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=int(max(1, min(127, vel))), art=art, **kw))
DR = dict(kick=36, snare=38, rim=37, hat=42, ohat=46, ride=51, crash=49, tom_hi=48, tom_mid=45, tom_lo=41)
def voicing(ch, lo=55, n=4):
    out, p = [], lo
    while len(out) < n:
        if p % 12 in tones(ch): out.append(p)
        p += 1
    return out
def root_at(ch, lo): return lo + (BV.bass_pc(ch) - lo) % 12
LOW914 = {1: 60, 2: 60, 3: 53, 4: 53, 5: 46, 6: 47, 7: 34, 8: 41, 9: 41, 10: 41, 11: 41}     # Module 9.14: no second below C4, no third below F3 (749.21)
def gtr(ch, lo=40, n=6, hi=72):
    """a guitar voicing kept inside Module 9.14's low-interval limits: the root at the bottom, then each chord tone whose interval with
    the note below it is allowed at that height."""
    r = root_at(ch, lo); out = [r]; q = r
    while len(out) < n and q < hi:
        q += 1
        if q % 12 not in tones(ch): continue
        iv = q - out[-1]
        if iv >= 12 or out[-1] >= LOW914[iv]: out.append(q)
    return out
def fifth_at(ch, lo): return lo + ((BV.bass_pc(ch) + 7) - lo) % 12
LEVEL = {"Intro": 0.45, "Verse 1": 0.32, "Chorus 1": 0.55, "Verse 2": 0.28, "Chorus 2": 0.66, "Turnaround": 0.52, "Verse 3": 0.42, "Chorus 3": 0.90,
         "Tag": 0.70, "Ending": 0.50}                       # the plan by section role (749.17): each return above the one before
def V(sec, base=56, span=40): return base + int(round(span * LEVEL[sec]))
def boom_chick(st, ch, ch2, vel):
    """the acoustic: the root on 1, the fifth on 3 (the boom), the chord on 2 and 4 with an upstroke after (the chick)."""
    for half, c_ in ((0, ch), (24, ch2)):
        bs = root_at(c_, 40) if half == 0 else fifth_at(c_, 40)
        ev("acoustic", st + half, 12, bs, vel + 4)
        vc = gtr(c_, 53, 4)[1:] if root_at(c_, 53) < 55 else gtr(c_, 53, 3)                 # the chick: chord tones from F3 up (749.21)
        ev("acoustic", st + half + 12, 6, vc, vel); ev("acoustic", st + half + 18, 6, vc[1:], vel - 10)
def strum8(st, ch, ch2, vel, under=False):
    for e in range(0, 48, 6):
        c_ = ch if e < 24 else ch2; vc = gtr(c_, 40, 6, hi=64 if under else 72)            # under her: the voicing kept below her line (749.21)
        ev("acoustic", st + e, 6, vc if e % 12 == 0 else vc[2:], vel + (6 if e % 24 == 0 else 0) - (8 if e % 12 else 0))
PENTA = {9, 11, 1, 4, 6}
def lick(part, st, ch, vel, rng, top=74, n=4):
    """a short fill: n eighths down the major pentatonic from a chord tone near the top, ending on a chord tone (Telecaster or fiddle)."""
    p = max(q for q in range(top - 7, top + 1) if q % 12 in tones(ch)); seq = [p]
    for _ in range(n - 1):
        q = down_to(seq[-1], PENTA, rng.choice((1, 1, 2)))
        seq.append(q)
    if seq[-1] % 12 not in tones(ch): seq[-1] = max(q for q in range(seq[-1] - 4, seq[-1] + 1) if q % 12 in tones(ch))
    for j, q in enumerate(seq):
        dbl = part == "tele" and j == 0
        ev(part, st + 6 * j, 6 if j < n - 1 else 12, [q - 3 if (q - 3) % 12 in tones(ch) else q - 4, q] if dbl else q, vel - 4 * (j % 2))
def steel_swell(st, ch, vel, L=48, under=False):
    vc = [q for q in voicing(ch, 52 if under else 59, 3)]; ev("steel", st, L, vc[1:], vel)
def steel_fill(st, ch, vel, rng):
    a = max(q for q in range(64, 72) if q % 12 in tones(ch)); b_ = up_to(a, M.SCALE, 1)
    ev("steel", st, 6, b_, vel - 6); ev("steel", st + 6, 18, a, vel)                              # a bend from the note above into a chord tone
def piano_off(st, ch, ch2, vel):
    for e in (12, 36):
        c_ = ch if e < 24 else ch2; ev("piano", st + e, 10, voicing(c_, 60, 3), vel)
def fiddle_long(st, ch, vel, L=48, under=False):
    """long notes: over him (F#4-D5); under her (G3-E4), so nothing sits over her line (749.21)."""
    lo_, hi_ = (55, 65) if under else (66, 75)
    ev("fiddle", st, L, max(q for q in range(lo_, hi_) if q % 12 in tones(ch)), vel)
def two_step(st, vel, cross=False, ride=False, fill=False, stop_at=None):
    for e in range(0, 48, 6):
        if stop_at is not None and e >= stop_at: break
        if e in (0, 24): ev("drums", st + e, 3, DR["kick"], vel)
        if e in (12, 36): ev("drums", st + e, 3, DR["rim" if cross else "snare"], vel - (10 if cross else 0))
        if fill and e >= 24: continue
        ev("drums", st + e, 3, DR["ride" if ride else "hat"], vel - 26 + (6 if e % 12 == 0 else 0))
    if fill:
        for j, (e, d) in enumerate(((24, "snare"), (30, "snare"), (36, "tom_hi"), (39, "tom_mid"), (42, "tom_lo"), (45, "tom_lo"))): ev("drums", st + e, 3, DR[d], vel - 6 + 2 * j)
def crash(st, vel): ev("drums", st, 6, DR["crash"], vel)
# the voice's rests by half-bar: where the fills go
VON = collections.Counter(n["on"] // 24 for n in lead)
def quiet_half(h): return VON[h] == 0
CALLN = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]; ANSN = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 9]   # the call and the answer as sung
def play_line(part, ns, line, st, vel, octave=12):
    U = P.line_start("Chorus 1", line)
    for n in ns: ev(part, st + (n["on"] - U), n["dur"], n["midi"] + octave, vel)
def play_hook(part, st, vel): play_line(part, CALLN, 0, st, vel); play_line(part, ANSN, 9, st + 48, vel)   # the call, then the answer, a bar each
rng = random.Random("song 55 band")
first_line_bars = set()
for s_ in P.SUNG:
    for i_ in range(len(P.LINES[s_])): first_line_bars.add(P.line_start(s_, i_) // EB)
BRK_LAST = P.BAR0["Turnaround"] + 3; TAG0 = P.BAR0["Tag"]
for x in bars:
    sec, kind, st, k, nb = x["sec"], x["kind"], x["start"], x["k"], x["n"]
    ch, ch2 = x["chord"], x["chord2"]; last_bar = k == nb - 1; v = V(sec)
    h0, h1 = st // 24, st // 24 + 1
    if sec == "Intro":
        boom_chick(st, ch, ch2, v - 6); two_step(st, v - 10, cross=True, fill=last_bar)
        if k == 0: play_hook("fiddle", st, v + 4)
        elif k == 2: lick("fiddle", st, ch, v, rng, top=81, n=6)
        elif k == 3: steel_fill(st, ch, v - 4, rng)
        steel_swell(st, ch, v - 14)
    elif sec == "Verse 1":
        boom_chick(st, ch, ch2, v); two_step(st, v - 4, cross=True, fill=last_bar)
        if k % 2 == 1 and quiet_half(h1): steel_fill(st + 24, ch2, v - 8, rng)
    elif sec == "Verse 2":                                                                     # his daddy: pulled back, the steel holding under it
        boom_chick(st, ch, ch2, v - 4); two_step(st, v - 10, cross=True, fill=last_bar)
        steel_swell(st, ch, v - 12)
    elif sec == "Verse 3":                                                                     # Sunday: piano chords for the pew, then the lake
        boom_chick(st, ch, ch2, v); two_step(st, v - (8 if k < 8 else 0), cross=k < 8, fill=last_bar)
        if k < 8: ev("piano", st, 24, voicing(ch, 57, 4), v - 8); ev("piano", st + 24, 24, voicing(ch2, 57, 4), v - 10)
        elif k % 2 == 1 and quiet_half(h1): lick("tele", st + 24, ch2, v - 2, rng)
    elif kind == "Chorus":
        strum8(st, ch, ch2, v); two_step(st, v + 4, ride=sec == "Chorus 3", fill=last_bar)
        if k == 0: crash(st, v + 12)
        if sec == "Chorus 3" and x["b"] in first_line_bars: crash(st, v + 8)
        steel_swell(st, ch, v - 10)
        if sec in ("Chorus 2", "Chorus 3"): piano_off(st, ch, ch2, v - 14)
        if sec == "Chorus 3": fiddle_long(st, ch, v - 12, under=True)
        if quiet_half(h1) and k >= 4 and k % 2 == 1: lick("tele", st + 24, ch2, v - 4, rng, n=3)
    elif sec == "Turnaround":                                                                  # the break: the call and the answer on the fiddle, the steel's reply, then a breath
        if k < 3: boom_chick(st, ch, ch2, v); two_step(st, v, fill=False)
        if k == 0: play_hook("fiddle", st, v + 6)
        elif k == 2: steel_fill(st, ch, v, rng); steel_fill(st + 24, ch2, v - 4, rng)
        elif k == 3: ev("acoustic", st, 48, gtr(ch, 40, 6), v - 10)                           # 749.19: the last bar thin, the acoustic alone
    elif sec == "Tag":
        if k == 0: ev("drums", st, 3, DR["kick"], v); crash(st, v)                            # the call over a stop: one hit, then the voices
        else:
            strum8(st, ch, ch2, v); two_step(st, v); steel_swell(st, ch, v - 8); fiddle_long(st, ch, v - 12, under=True); piano_off(st, ch, ch2, v - 14)
    elif sec == "Ending":
        if k == 0:
            boom_chick(st, ch, ch2, v); two_step(st, v - 8, cross=True)
            play_line("fiddle", ANSN, 9, st, v)                                                # the answer, home to A
        else:
            ev("acoustic", st, 48, gtr("A", 40, 6), v); ev("steel", st, 48, [61, 64, 69], v - 6); ev("piano", st, 48, [57, 61, 64, 69], v - 10)
            ev("drums", st, 3, DR["kick"], v); crash(st, v)
# the fiddle's ending phrase lands home (G) over the last G: trimmed so nothing in it overruns
END0 = SEC0["Ending"]
parts["fiddle"][:] = [e for e in parts["fiddle"] if e["on"] < REC_END]
for e in parts["fiddle"]:
    if e["on"] + e["dur"] > REC_END: e["dur"] = REC_END - e["on"]
# ---- the sung sections' bass: the routine on the engine's grid ----
ebars = [dict(sec=nm, kind=kind, k=k, n=nb, chord=H2[2 * (P.BAR0[nm] + k)], start=(P.BAR0[nm] + k) * EB, len=EB) for nm, kind, nb in P.FORM for k in range(nb)]
edrums = [e for e in parts["drums"] if bars[e["on"] // EB]["sec"] in P.SUNG]
erec = dict(bars=ebars, chords2=list(P.CHORD2), drums=edrums, lead=[dict(n, on=n["on_engine"]) for n in lead])
BV.SCALE_AT[0] = None
BB, tries = BV.write_bass(erec, 33, (9, "major"), "55")
for e in BB:
    x = bars[e["on"] // EB]
    if x["sec"] in P.SUNG:
        if x["sec"] == "Tag" and x["k"] == 0: continue                                         # the tag's call over a stop
        parts["bass"].append(dict(e))
for x in bars:                                                                               # root-five where the routine is out (the intro, the turnaround, the ending)
    if x["sec"] in P.INSTRUMENTAL:
        if x["sec"] == "Ending" and x["k"] == 1: ev("bass", x["start"], 48, root_at("A", 33), 70); continue
        if x["sec"] == "Turnaround" and x["k"] == 3: continue                                  # the breath: the acoustic alone
        ev("bass", x["start"], 22, root_at(x["chord"], 33), V(x["sec"]) - 4); ev("bass", x["start"] + 24, 22, fifth_at(x["chord2"], 33), V(x["sec"]) - 8)
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"] and out[-1]["art"] == e["art"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); out[-1]["dur"] = max(out[-1]["dur"], e["dur"]); continue
        out.append(e)
    return out
for e in parts["bass"]: e["p"] = [q + 12 if q < 28 else q for q in e["p"]]
PARTS = {k: tidy(v) for k, v in parts.items()}
plan = [(nm, nb, SEC0[nm], ["4/4"] * nb, nm) for nm, kind, nb in P.FORM]
secs = sum(x["len"] / 12 * 60 / x["qbpm"] for x in bars)
rec = dict(title="Your Yard Man", file_title="Your Yard Man", nbars=NB, bars=bars, chords2=H2, plan=plan, lead=lead, harm=harm,
           parts=PARTS, slot="twelfth of a beat", qbpm=QB, feel=P.FEEL, seconds=secs, end=REC_END, level=LEVEL,
           fp=c["fp"], order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"],
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, judge={k: c["judge"][k] for k in ("combined", "content", "order")},
           plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"], kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()},
           rerun=F["run"]["rerun"], text=TEXT, registers=c["meta"]["registers"], carriers=c["meta"]["carriers"],
           design=dict(gates=P.DESIGN_GATES, call=P.CALL, answer=P.ANSWER, answer_tag=P.ANSWER_T, half_bars={f"{a}:{b}": v for (a, b), v in P.DESIGN_HALF.items()},
                       slots={s: P.slots_of(s) for s in P.SUNG}),
           chart438=F["run"]["rerun"].get("chart438"), bass_written_by="bass_v134.py write_bass (the sung sections, on the engine's grid)", bass_tries=tries,
           breath=dict(bar=BRK_LAST, at=RS[BRK_LAST], rule="749.19: the break's last bar thins to the acoustic alone; verse 3 re-enters"),
           stop=dict(bar=TAG0, rule="the tag's call over a stop: one kick and crash, the voices alone"))
pickle.dump(rec, open("/home/claude/p65/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{secs % 60:04.1f});", len(lead), "sung;", {k: len(v) for k, v in PARTS.items()}, "other voices", len(harm), "bass tries", tries)
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t_ + ("-" if h else "") for t_, h in ws))
