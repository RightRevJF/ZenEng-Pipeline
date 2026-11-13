"""The Singer Doesn't Stop (song 47): the song record from melody_final.pkl (the pick of record) and the 438 chart -- acoustic-driven
modern CCM, q = 84, sixteenth-note strum, G major, 88 bars (Q4 B, Q6 A, Q7 A, the form A, the arrangement A). The record is built from
both: the chart (the half-bar chords) and the pick; the bass is written by the routine (bass_v131.py) from the record's chart, kicks and lead.
  the lift  the second bridge's first fourteen bars (its first seven lines) a whole step up in the record: the voice and the chords (A major);
            its last line ('You remember all of me') back in G (the bridge's build, A).
  voice     the tenor, every line.
  guitar    steel-string acoustic, a sixteenth-note strum on the chord: alone in the intro and verse 1; through everything; alone in the tag.
  bass      by the routine, from chorus 1 on; out for the first bridge; back at the second bridge's fifth bar.
  drums     a brushed kit from chorus 1 (kick on 1 and 3, brush on 2 and 4, brushed sixteenths; verse 2 without the kick); out for the first bridge; the second
            bridge brings it back (brushes from its fifth bar, the kick from its ninth); the last chorus plain; out for the tag.
  electric  a low clean electric guitar, swelled sustained chord tones: from verse 2 on, out for the first bridge.
  No pads, no gang vocals (the arrangement, A). The tag ends on one G chord on the guitar, let ring."""
import pickle, sys
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p57"]
import melody_v131_p57 as P
import bass_v131 as BV
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p57/melody_final.pkl", "rb")); c = F["pick"]
BAR = 48; NB = P.NBARS; QB = 84
assert list(P.CHORD2) == list(F["run"]["chords2"]), "the chart drawn on import differs from the run's"
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"doctor": ["doc", "tor"], "healthy": ["health", "y"], "never": ["nev", "er"], "perfect": ["per", "fect"], "Mama": ["Ma", "ma"], "hummed": ["hummed"],
        "before": ["be", "fore"], "humming": ["hum", "ming"], "ever": ["ev", "er"], "doesn't": ["does", "n't"], "singer": ["sing", "er"], "remember": ["re", "mem", "ber"],
        "every": ["ev", "ery"], "Every": ["Ev", "ery"], "heartbeat": ["heart", "beat"], "again": ["a", "gain"], "Lazarus": ["Laz", "a", "rus"], "into": ["in", "to"],
        "breathing": ["breath", "ing"], "morning": ["morn", "ing"], "Thomas": ["Thom", "as"], "copy,": ["cop", "y,"], "cover": ["cov", "er"], "stranger": ["stran", "ger"],
        "stumble": ["stum", "ble"], "carried": ["car", "ried"], "remembers": ["re", "mem", "bers"], "Even": ["E", "ven"], "'Cause": ["'Cause"], "into,": ["in", "to,"],
        "talked,": ["talked,"], "sing,": ["sing,"]}
def split_words(text, sy):
    out = []; ws = text.replace('"', "").split()
    for w in ws:
        n = len(P.syl(w)); core = w.rstrip(",.;:?")
        if n <= 1: out.append((w, False)); continue
        parts = HFIX.get(w) or HFIX.get(core) or _PY.inserted(core).split("-")
        tail = "" if w in HFIX else w[len(core):]
        if len(parts) > n: parts = parts[:n - 1] + ["".join(parts[n - 1:])]
        while len(parts) < n: parts.append("_")
        for j, p in enumerate(parts): out.append((p + (tail if j == n - 1 else ""), j < n - 1))
    assert len(out) == len(sy), (text, out, sy)
    return out
TEXT = {sec: [split_words(t, P.LINES[sec][i]) for i, (_, t) in enumerate(M.WORDS_OF[sec])] for sec in P.SUNG}
# ---- the lift: the second bridge's bars 1-14 a whole step up (voice and chords) ----
B2 = P.BAR0["Bridge 2"]; LIFTB = set(range(B2, B2 + 14)); LIFT = P.LIFT2
UP = {"G": "A", "C": "D", "D": "E", "Em": "F#m", "Am": "Bm", "Bm": "C#m"}
CH = dict(M.CH); CH.update({"A": (9, {9, 1, 4}), "E": (4, {4, 8, 11}), "F#m": (6, {6, 9, 1}), "C#m": (1, {1, 4, 8})})
ROM = {"G": "I", "D": "V", "Em": "vi", "C": "IV", "Am": "ii", "Bm": "iii"}
ROMA = {"A": "I", "E": "V", "F#m": "vi", "D": "IV", "Bm": "ii", "C#m": "iii"}
H2 = [UP[ch] if (h // 2) in LIFTB else ch for h, ch in enumerate(P.CHORD2)]
def roman(ch, b): return (ROMA if b in LIFTB else ROM)[ch]
bars = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=H2[2 * b], chord2=H2[2 * b + 1], roman=roman(H2[2 * b], b), start=b * BAR, len=BAR, qbpm=QB,
                         key="A major" if b in LIFTB else "G major", stop=False))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); t, hy = TEXT[sec][i][n["syl"]]
    up = LIFT if n["on"] // BAR in LIFTB else 0
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"] + up, sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="voice", lifted=bool(up)))
def tones(ch): return CH[ch][1]
def voicing(ch, lo=52):
    out, p = [], lo
    while len(out) < 4:
        if p % 12 in tones(ch): out.append(p)
        p += 1
    return [CH[ch][0] + 36 + (12 if CH[ch][0] < 4 else 0)] + out                         # a low root (E2-D#3), then four chord tones from E3
drums, gtr, elec = [], [], []
def ev(lst, on, dur, p, vel, art="", **kw): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art, **kw))
DR = dict(kick=36, brush=38, swirl=40, hat=42, ride=51)
STRUM = [(0, 80, "down"), (3, 46, "up"), (6, 62, "down"), (9, 50, "up")]                   # a sixteenth strum a beat: accents on the beat and its eighth
def band_on(sec, k, n, kind):
    """the arrangement (A): which parts play in a bar."""
    bass = kind in ("Chorus",) or sec == "Verse 2" or (sec == "Bridge 2" and k >= 4)
    kit = kind == "Chorus" or sec == "Verse 2" or (sec == "Bridge 2" and k >= 4)
    kick = kit and not (sec == "Bridge 2" and k < 8) and sec != "Verse 2"
    el = sec in ("Verse 2", "Chorus 2", "Bridge 2", "Last Chorus")
    return bass, kit, kick, el
for b_ in bars:
    sec, kind, st, k, n = b_["sec"], b_["kind"], b_["start"], b_["k"], b_["n"]
    if kind == "Tag" and k == n - 1:
        ev(gtr, st, BAR, voicing("G"), 70, "ring"); continue
    lift = 16 if sec == "Last Chorus" else 6 if kind == "Chorus" else 8 if (sec == "Bridge 2" and k >= 8) else 0
    soft = -14 if (sec == "Verse 1" or kind in ("Intro", "Tag") or sec == "Bridge") else 0
    bass, kit, kick, el = band_on(sec, k, n, kind)
    for h in (0, 1):
        ch = H2[2 * (st // BAR) + h]; vc = voicing(ch)
        for beat in (0, 1):
            for off, vel, d in STRUM:
                t = st + 24 * h + 12 * beat + off
                ev(gtr, t, 3, vc if d == "down" else vc[1:], vel + soft + lift // 2, "strum " + d)
        if el: ev(elec, st + 24 * h, 23, [p for p in range(55, 72) if p % 12 in tones(ch)][:3], 44 + lift, "swell")
    if kit:
        if kick:
            for e, v_ in ((0, 84), (18, 66), (24, 84)): ev(drums, st + e, 3, DR["kick"], v_ + lift)
        [ev(drums, st + e, 3, DR["brush"], 70 + lift) for e in (12, 36)]
        [ev(drums, st + e, 3, DR["hat"], 40 + lift // 2 + (8 if e % 12 == 0 else 0)) for e in range(0, 48, 6)]
    if kind == "Chorus" and k == 0 and sec != "Chorus 1": ev(drums, st, 3, 49, 70 + lift, "cymbal swell")
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); continue
        out.append(e)
    return out
drums = tidy(drums); gtr = tidy(gtr); elec = tidy(elec)
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title="The Singer Doesn't Stop", nbars=NB, bars=bars, chords2=H2, chords2_engine=list(P.CHORD2), lift=dict(bars=sorted(LIFTB), semitones=LIFT),
           plan=plan, lead=lead, drums=drums, guitar=gtr, electric=elec, slot="twelfth of a beat", bar=BAR, qbpm=QB, feel=P.FEEL, seconds=secs, tw_sec=60 / QB / 12,
           fp=c["fp"], order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"],
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, judge={k: c["judge"][k] for k in ("combined", "content", "order")},
           plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"], kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()},
           rerun=F["run"]["rerun"], text=TEXT, lift_reading=c["info"]["lift"], registers=c["meta"]["registers"], palettes=c["meta"]["palettes"],
           outside_target=c["meta"]["outside_target"], carriers=c["meta"]["carriers"], design=dict(gates=P.DESIGN_GATES, slots={s: P.slots_of(s) for s in P.SUNG}),
           chart438=F["run"]["rerun"].get("chart438"))
BV.SCALE_AT[0] = lambda b: ({9, 11, 1, 2, 4, 6, 8} if b in LIFTB else {7, 9, 11, 0, 2, 4, 6})
B, tries = BV.write_bass(rec, 33, (7, "major"), "47")
keep = lambda e: band_on(bars[e["on"] // BAR]["sec"], bars[e["on"] // BAR]["k"], bars[e["on"] // BAR]["n"], bars[e["on"] // BAR]["kind"])[0] and bars[e["on"] // BAR]["kind"] != "Tag"
B = [e for e in B if keep(e)]
rec["bass"] = B; rec["bass_written_by"] = "bass_v131.py write_bass (439, 445-448, 516, 517, 538; v131: the scale by the bar); kept where the arrangement has bass"; rec["bass_tries"] = tries
pickle.dump(rec, open("/home/claude/p57/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s;", len(lead), "sung;", {k: len(v) for k, v in dict(drums=drums, bass=B, guitar=gtr, electric=elec).items()}, "bass tries", tries)
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t + ("-" if h else "") for t, h in ws))
