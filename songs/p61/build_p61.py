"""A Wire Pulled Tight (song 51): the song record from melody_final.pkl (the pick of record) and the writer's chords. Slow-build alternative
rock, A major, 194 bars, 4/4, written at double tempo with a half-time feel (the snare on beat 3 of every written bar): q = 116 rising to 164,
felt as 58 to 82 (the genre, A; the tempo plan, A; the length, A then A).
  Intro (4) and verse 1: the acoustic guitar alone, fingerpicked.
  Pre 1: the bass enters, held roots; a clean electric guitar swells.
  Chorus 1: the kit enters, light (kick, cross-stick, hat); clean electric arpeggios; the organ pad; harmony on the hook.
  Verse 2: brushes; the electric muted.     Pre 2: building, a snare roll into the chorus.
  Chorus 2: the full kit; overdriven guitar chords; the organ; harmony on the hook.
  Verse 3: the full kit; the overdriven guitar palm-muted.     Pre 3: building, the C#dim7 bar held back.
  Chorus 3: the most so far; crashes on the line downbeats; harmony on the hook and the first four lines.
  Verse 4: driving: the hat in written eighths, the guitars driving.
  Bridge: pass 1 the acoustic and the kick alone; pass 2 builds (snare, toms, the guitars swelling, the organ), a crash into a full stop.
  Approach (8): a bar of silence, then the acoustic guitar alone, slowing (164 to 120).
  Final chorus: the full band, steady; at the G (bars 13-15) thinned to voice, acoustic and organ; the band back on the Asus4 under 'through';
  the A rings. Harmony on every line.
  Tag: the acoustic guitar alone at 110 (felt 55); the last A decays.
The sung sections' bass is written by the routine (bass_v134.py) on the engine's grid."""
import pickle, sys, random, collections
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p61"]
import io as _io, contextlib as _cl
with _cl.redirect_stdout(_io.StringIO()): import melody_l7_p61 as P
import bass_v134 as BV
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p61/melody_final.pkl", "rb")); c = F["pick"]
EB = 48; NB = P.NBARS
assert list(P.CHORD2) == list(F["run"]["chords2"]), "the chart on import differs from the run's"
# ---- the tempo plan (A): written q per section, start and end (felt = half) ----
TEMPO = {"Intro": (116, 116), "Verse 1": (116, 116), "Pre 1": (116, 132), "Chorus 1": (132, 132), "Verse 2": (128, 128), "Pre 2": (128, 140),
         "Chorus 2": (140, 140), "Verse 3": (136, 136), "Pre 3": (136, 148), "Chorus 3": (148, 148), "Verse 4": (156, 156), "Bridge": (164, 164),
         "Approach": (164, 120), "Last Chorus": (132, 132), "Tag": (110, 110)}
def qb_of(sec, k, nb):
    a, z = TEMPO[sec]; return a if a == z else round(a + (z - a) * k / max(1, nb - 1))
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"There's": ["There's"], "waiting": ["wait", "ing"], "under": ["un", "der"], "forgets": ["for", "gets"], "second": ["sec", "ond"], "TV": ["T", "V"],
        "somebody's": ["some", "bod", "y's"], "coffee's": ["cof", "fee's"], "paper": ["pa", "per"], "nobody's": ["no", "bod", "y's"], "every": ["ev", "ery"],
        "cradle": ["cra", "dle"], "voice": ["voice"], "somewhere": ["some", "where"], "stillness": ["still", "ness"], "breaking": ["break", "ing"],
        "table": ["ta", "ble"], "afternoon": ["af", "ter", "noon"], "water": ["wa", "ter"], "halfway": ["half", "way"], "nobody": ["no", "bod", "y"],
        "noticed": ["no", "ticed"], "glasses": ["glass", "es"], "lived": ["lived"], "before": ["be", "fore"], "sixty": ["six", "ty"],
        "thousand": ["thou", "sand"], "strangers": ["stran", "gers"], "bleachers": ["bleach", "ers"], "stamping": ["stamp", "ing"], "carried": ["car", "ried"],
        "single": ["sin", "gle"], "something": ["some", "thing"], "fever": ["fe", "ver"], "a.m.": ["a.", "m."], "window": ["win", "dow"], "going": ["go", "ing"],
        "again": ["a", "gain"], "against": ["a", "gainst"], "apart": ["a", "part"], "ticking": ["tick", "ing"], "ever": ["ev", "er"], "wasted": ["wast", "ed"],
        "inside": ["in", "side"], "white-walled": ["white-", "walled"], "wire": ["wi", "re"], "hours": ["hou", "rs"], "hour": ["hou", "r"]}
def split_words(text, sy):
    out = []; ws = text.replace('"', "").split()
    for w in ws:
        n = len(P.syl(w)); core = w.rstrip(",;:?") if w != "a.m." else w
        if n <= 1: out.append((w, False)); continue
        parts = list(HFIX.get(w) or HFIX.get(core) or _PY.inserted(core).split("-"))
        tail = "" if w in HFIX else w[len(core):]
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        for j, p in enumerate(parts): out.append((p + (tail if j == n - 1 else ""), j < n - 1 and not p.endswith("-")))
    assert len(out) == len(sy), (text, out, [x[0] for x in sy])
    return out
TEXT = {sec: [split_words(t, P.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in P.SUNG}
H2 = list(P.CHORD2)
bars = []; t = 0; RS = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, b=b, meter="4/4", start=t, len=EB, chord=H2[2 * b], chord2=H2[2 * b + 1],
                         roman=M.ROMAN[H2[2 * b]], qbpm=qb_of(nm, k, nb), key="A major", movement=nm, stop=(nm == "Approach" and k == 0)))
        RS.append(t); t += EB
REC_END = t
def rt(on): return on                                                                    # one grid: the record is the engine's
SEC0 = {nm: RS[P.BAR0[nm]] for nm, _, _ in P.FORM}
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); tx, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], on_engine=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=tx, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="voice"))
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
# ---- harmony: the hook in every chorus; the first four lines of chorus 3; every line of the final chorus ----
def harmonised(n): return n["role"] == "hook" or n["sec"] == "Last Chorus" or (n["sec"] == "Chorus 3" and n["line"] < 4)
harm_hi, harm_lo = [], []
for n in lead:
    if not harmonised(n): continue
    ch = chord_at_rec(n["on"]); ct = tones(ch); sc = M.SCALE | {7}
    hi_ = next((q for q in range(n["midi"] + 3, n["midi"] + 6) if q % 12 in ct), up_to(n["midi"], sc, 2))
    lo_ = next((q for q in range(n["midi"] - 3, n["midi"] - 6, -1) if q % 12 in ct), down_to(n["midi"], sc, 2))
    harm_hi.append(dict(n, midi=hi_, singer="harmony high")); harm_lo.append(dict(n, midi=lo_, singer="harmony low"))
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
def pick(st, ch, vel):
    """the acoustic guitar fingerpicked, written eighths (felt sixteenths): the thumb on the root and fifth, the fingers between."""
    r = root_at(ch, 40); f5 = r + 7 if r + 7 <= 52 else r - 5; up = voicing(ch, 55, 3)
    for e, p in ((0, r), (6, up[1]), (12, up[2]), (18, up[0]), (24, f5), (30, up[1]), (36, up[2]), (42, up[0])):
        ev("acoustic", st + e, 6 if e % 12 else 12, p, vel + (6 if e % 24 == 0 else -4 if e % 12 else 0))
def strum(st, ch, vel):
    vc = voicing(ch, 43, 6)
    for e in (0, 12, 18, 30, 36): ev("acoustic", st + e, 12 if e % 12 == 0 else 6, vc, vel + (8 if e in (0, 24) else 0) - (6 if e % 12 else 0))
def clean_arp(st, ch, vel):
    vc = voicing(ch, 59, 4)
    for j, e in enumerate(range(0, 48, 6)): ev("electric", st + e, 6, vc[j % 4] if j < 4 else vc[3 - j % 4], vel - (4 if e % 12 else 0))
def driven(st, ch, vel, muted=False, step=6, eighths=False):
    r = root_at(ch, 40); pc_ = [r, r + 7, r + 12]
    if muted:
        for e in range(0, 48, step): ev("drive", st + e, 4, pc_[:2], vel - (6 if e % 12 else 0), art="mute")
    elif eighths:
        for e in range(0, 48, 6): ev("drive", st + e, 6, pc_, vel - (8 if e % 12 else 0))
    else: ev("drive", st, 24, pc_, vel); ev("drive", st + 24, 24, pc_, vel - 6)
def organ(st, ch, vel, L=48): ev("organ", st, L, voicing(ch, 57, 4), vel)
def kit_light(st, vel):
    ev("drums", st, 3, DR["kick"], vel); ev("drums", st + 30, 3, DR["kick"], vel - 14); ev("drums", st + 24, 3, DR["rim"], vel - 8)
    for e in range(0, 48, 12): ev("drums", st + e, 3, DR["hat"], vel - 24)
def brushes(st, vel):
    ev("drums", st, 3, DR["kick"], vel - 10); ev("drums", st + 24, 3, DR["snare"], vel - 18)
    for e in range(0, 48, 12): ev("drums", st + e, 3, DR["ride"], vel - 30)
def kit_full(st, vel, hat8=False, ride=False):
    ev("drums", st, 3, DR["kick"], vel); ev("drums", st + 18, 3, DR["kick"], vel - 12); ev("drums", st + 24, 3, DR["snare"], vel)
    for e in range(0, 48, 6 if hat8 else 12): ev("drums", st + e, 3, DR["ride" if ride else "hat"], vel - 22 + (6 if e % 12 == 0 else 0))
def fill(st, vel):
    for j, (e, d) in enumerate(((24, "snare"), (30, "snare"), (36, "tom_hi"), (39, "tom_mid"), (42, "tom_lo"), (45, "tom_lo"))): ev("drums", st + e, 3, DR[d], vel - 6 + 2 * j)
def crash(st, vel): ev("drums", st, 6, DR["crash"], vel)
first_line_bars = set()
for s_ in P.SUNG:
    for i_ in range(len(P.LINES[s_])): first_line_bars.add(P.line_start(s_, i_) // EB)
for x in bars:
    sec, kind, st, k, nb = x["sec"], x["kind"], x["start"], x["k"], x["n"]
    ch, ch2 = x["chord"], x["chord2"]; last_bar = k == nb - 1
    if sec == "Intro" or sec == "Verse 1": pick(st, ch, 56 if sec == "Intro" else 58)
    elif sec == "Pre 1":
        pick(st, ch, 60); ev("electric", st, 48, voicing(ch, 59, 3), 40 + 4 * k)
    elif sec == "Chorus 1":
        strum(st, ch, 62); ev("electric", st, 48, voicing(ch, 59, 3), 46); organ(st, ch, 40); kit_light(st, 64)
    elif sec == "Verse 2":
        pick(st, ch, 58); brushes(st, 60); driven(st, ch, 42, muted=True, step=12)
    elif sec == "Pre 2":
        strum(st, ch, 62); brushes(st, 66); driven(st, ch, 50, muted=True, step=12)
        if last_bar:
            for e in range(24, 48, 3): ev("drums", st + e, 3, DR["snare"], 50 + e)
    elif sec == "Chorus 2":
        strum(st, ch, 66); driven(st, ch, 64); clean_arp(st, ch, 50); organ(st, ch, 48); kit_full(st, 82)
        if k == 0: crash(st, 88)
    elif sec == "Verse 3":
        strum(st, ch, 62); driven(st, ch, 58, muted=True); kit_full(st, 78)
    elif sec == "Pre 3":
        strum(st, ch, 66); driven(st, ch, 64, muted=k < 2); organ(st, ch, 46); kit_full(st, 84)
        if last_bar: fill(st, 92)
    elif sec == "Chorus 3":
        strum(st, ch, 72); driven(st, ch, 74, eighths=True); clean_arp(st, ch, 56); organ(st, ch, 56); kit_full(st, 92, hat8=True, ride=True)
        if x["b"] in first_line_bars: crash(st, 96)
    elif sec == "Verse 4":
        strum(st, ch, 70); driven(st, ch, 72, muted=k % 4 < 2); organ(st, ch, 50); kit_full(st, 96, hat8=True)
        if k == 0: crash(st, 100)
    elif sec == "Bridge":
        if k < 8:
            pick(st, ch, 54); ev("drums", st, 3, DR["kick"], 60); ev("drums", st + 24, 3, DR["kick"], 52)
            if k >= 4: clean_arp(st, ch, 40)
        else:
            j = k - 8; strum(st, ch, 62 + 3 * j); clean_arp(st, ch, 48 + 3 * j); organ(st, ch, 40 + 3 * j); kit_full(st, 70 + 4 * j, hat8=j >= 4, ride=j >= 4)
            if j >= 4: driven(st, ch, 66 + 4 * j, eighths=True)                              # the peak: 'none of it was ever lost' (D4) and the full stop after it
            if j == 4: crash(st, 100)
            if last_bar: fill(st, 100)
    elif sec == "Approach":
        if k == 0: continue                                                                  # the full stop: a bar of silence (two felt beats)
        if k < 6: pick(st, ch, 56 - 2 * k)
        else: ev("acoustic", st, 48, voicing(ch, 45, 5), 52)
    elif sec == "Last Chorus":
        if 12 <= k <= 14:                                                                    # the G: thinned to voice, acoustic and the organ
            pick(st, ch, 58); organ(st, ch, 52)
        elif k in (15, 16):                                                                  # the Asus4 under 'through': the band back, swelling
            strum(st, ch, 70); driven(st, ch, 66 + 4 * (k - 15)); organ(st, ch, 56); kit_full(st, 82 + 6 * (k - 15), ride=True)
            if k == 15: crash(st, 96)
        elif k >= 17:                                                                        # the A: the release; held, then ringing
            if k == 17:
                crash(st, 104); ev("acoustic", st, 48 * 5, voicing("A", 45, 6), 70); ev("drive", st, 48 * 5, [45, 52, 57], 70); ev("organ", st, 48 * 5, voicing("A", 57, 4), 56)
                ev("drums", st, 3, DR["kick"], 100)
        else:
            strum(st, ch, 70); driven(st, ch, 70, eighths=True); clean_arp(st, ch, 52); organ(st, ch, 54); kit_full(st, 88, ride=True)
            if k == 0: crash(st, 96)
    elif sec == "Tag":
        if k < 4: pick(st, ch, 50 - 2 * k)
        elif k == 4: ev("acoustic", st, 48 * 4, voicing("A", 45, 6), 50)
ASTOP = RS[P.BAR0["Approach"]]
for n in lead:                                                                               # nothing sounds in the full stop
    if n["on"] < ASTOP < n["on"] + n["dur"]: n["dur"] = ASTOP - n["on"]
# ---- the sung sections' bass: the routine on the engine's grid ----
ebars = [dict(sec=nm, kind=kind, k=k, n=nb, chord=H2[2 * (P.BAR0[nm] + k)], start=(P.BAR0[nm] + k) * EB, len=EB) for nm, kind, nb in P.FORM for k in range(nb)]
edrums = [e for e in parts["drums"] if bars[e["on"] // EB]["sec"] in P.SUNG]
erec = dict(bars=ebars, chords2=list(P.CHORD2), drums=edrums, lead=[dict(n, on=n["on_engine"]) for n in lead])
BV.SCALE_AT[0] = None
BB, tries = BV.write_bass(erec, 33, (9, "major"), "51")
def bass_on(sec, k):
    if sec in ("Verse 1", "Tag") or sec in P.INSTRUMENTAL: return False
    if sec == "Bridge": return k >= 8
    if sec == "Last Chorus": return not (12 <= k <= 14) and k < 17
    return True
for e in BB:
    x = bars[e["on"] // EB]
    if x["sec"] in P.SUNG and bass_on(x["sec"], x["k"]): parts["bass"].append(dict(e))
for x in bars:                                                                               # the bass held where the routine is out: the first pre-chorus's roots, the bridge's first pass, the final A
    if x["sec"] == "Pre 1": parts["bass"] = [e for e in parts["bass"] if bars[e["on"] // EB]["sec"] != "Pre 1"]
for x in bars:
    if x["sec"] == "Pre 1": ev("bass", x["start"], 48, root_at(x["chord"], 33), 58)
    if x["sec"] == "Bridge" and 2 <= x["k"] < 8 and x["k"] % 2 == 0: ev("bass", x["start"], 96, root_at(x["chord"], 33), 52)
    if x["sec"] == "Last Chorus" and x["k"] == 17: ev("bass", x["start"], 48 * 5, 33, 70)
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"] and out[-1]["art"] == e["art"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); continue
        out.append(e)
    return out
for e in parts["bass"]: e["p"] = [q + 12 if q < 28 else q for q in e["p"]]
PARTS = {k: tidy(v) for k, v in parts.items()}
plan = [(nm, nb, SEC0[nm], ["4/4"] * nb, nm) for nm, kind, nb in P.FORM]
secs = sum(x["len"] / 12 * 60 / x["qbpm"] for x in bars)
rec = dict(title="A Wire Pulled Tight", file_title="A Wire Pulled Tight (v6)", nbars=NB, bars=bars, chords2=H2, plan=plan, lead=lead, harm_hi=harm_hi, harm_lo=harm_lo,
           parts=PARTS, slot="twelfth of a beat", qbpm=136, tempo=TEMPO, feel=P.FEEL, seconds=secs, end=REC_END,
           fp=c["fp"], order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"],
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, judge={k: c["judge"][k] for k in ("combined", "content", "order")},
           plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"], kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()},
           rerun=F["run"]["rerun"], text=TEXT, registers=c["meta"]["registers"], carriers=c["meta"]["carriers"],
           design=dict(gates=P.DESIGN_GATES, hook=P.HOOK, hook_final=P.HOOKL, bridge=P.LIFTD, tag=P.TAGL, bridge_low=P.BRIDGE_LOW, slots={s: P.slots_of(s) for s in P.SUNG}),
           chart438=F["run"]["rerun"].get("chart438"), bass_written_by="bass_v134.py write_bass (the sung sections, on the engine's grid)", bass_tries=tries)
pickle.dump(rec, open("/home/claude/p61/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{secs % 60:04.1f});", len(lead), "sung;", {k: len(v) for k, v in PARTS.items()}, "harmony", len(harm_hi), "bass tries", tries)
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t_ + ("-" if h else "") for t_, h in ws))
