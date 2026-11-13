"""Dry Ground (song 46): the song record from melody_final.pkl (the pick of record) and the 438 chart -- atmospheric pop, q = 118, four on
the floor, straight, A minor, 120 bars (Q4 C, Q6 A, Q7 A, Q11 A, Q13 A). The record is built from both: the chart (the half-bar chords,
inversions included) and the pick; the bass is written by the routine (bass_v130.py, 538) from the record's chart, kicks and lead.
  voice   the tenor, every line; the last 'flood' in falsetto (B4).
  drums   kick on every beat from intro bar 5; off-beat open hats in the choruses; light closed hats in the verses; claps on 2 and 4 from
          the pre-chorus on; a snare build in each pre-chorus's last bar and the bridge's last two; crash into each chorus.
          The bridge drops the kick (the dry ground) until its last two bars; the outro keeps the kick four bars, then lets it go.
  bass    by the routine (439, 445-448, 516, 517, 538).
  pad     the chord, sidechained to the kick (it breathes on every beat): through everything but the intro's first four bars.
  arp     a pulsing synth arpeggio on the chord's tones: sixteenths in the choruses; eighths in the intro, the verses, the bridge's last bars and the outro's first.
          The verses are filtered as if underwater, opening at each chorus (production note; the record marks 'filtered').
  rain    rain in the intro and the outro (production; a GM FX track).
  hum     a low drone on A: the intro's first bars and the outro, the car's cold hum.
  The outro thins to the hum and rain and ends on one A minor chord, let ring."""
import pickle, sys
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p56"]
import melody_v130_p56 as P
import bass_v130 as BV
M = P.M
import pyphen
F = pickle.load(open("/home/claude/p56/melody_final.pkl", "rb")); c = F["pick"]
BAR = 48; NB = P.NBARS; QB = 118
assert list(P.CHORD2) == list(F["run"]["chords2"]), "the chart drawn on import differs from the run's"
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"little": ["lit", "tle"], "quarter": ["quar", "ter"], "heater": ["heat", "er"], "blowing": ["blow", "ing"], "windows": ["win", "dows"], "window": ["win", "dow"],
        "running": ["run", "ning"], "swimming": ["swim", "ming"], "under": ["un", "der"], "living": ["liv", "ing"], "Every": ["Ev", "ery"], "painted": ["paint", "ed"],
        "sprinkler": ["sprin", "kler"], "rainbow": ["rain", "bow"], "never": ["nev", "er"], "gonna": ["gon", "na"], "again": ["a", "gain"], "water": ["wa", "ter"],
        "honey": ["hon", "ey"], "backbone": ["back", "bone"], "garden": ["gar", "den"], "after": ["af", "ter"], "couldn't": ["could", "n't"], "nothing": ["noth", "ing"],
        "library": ["li", "brar", "y"], "aground": ["a", "ground"], "Noah": ["No", "ah"], "missing": ["miss", "ing"], "empty": ["emp", "ty"], "drifted": ["drift", "ed"],
        "away": ["a", "way"]}
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
H2 = list(P.CHORD2)                                                                       # 438: the chord of each half-bar
def roman(ch):
    base = ch.split("/")[0]; return M.ROMAN.get(base, "?") + ("/" + ch.split("/")[1] if "/" in ch else "")
bars = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, k=k, n=nb, chord=H2[2 * b], chord2=H2[2 * b + 1], roman=roman(H2[2 * b]), start=b * BAR, len=BAR, qbpm=QB, key="A minor", stop=False))
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); t, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], dur=n["dur"], midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"], text=t, hyph=hy,
                     stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="voice", falsetto=bool(n.get("falsetto"))))
def tones(ch): return M.CH[ch][1]
def chord3(ch, lo):
    out, p = [], lo
    while len(out) < 3:
        if p % 12 in tones(ch): out.append(p)
        p += 1
    return out
drums, pad, arp, rain, hum = [], [], [], [], []
def ev(lst, on, dur, p, vel, art="", **kw): lst.append(dict(on=on, dur=dur, p=p if isinstance(p, list) else [p], vel=vel, art=art, **kw))
DR = dict(kick=36, clap=39, snare=38, ohh=46, chh=42, crash=49)
for b in bars:
    sec, kind, st, k, n = b["sec"], b["kind"], b["start"], b["k"], b["n"]
    last = kind == "Outro" and k == n - 1
    if last:
        ev(pad, st, BAR, chord3("Am", 57), 58, "ring"); ev(hum, st, BAR, [45], 50, "ring"); ev(rain, st, BAR, [60], 50, "rain"); continue
    lift = 14 if sec == "Last Chorus" else 6 if kind == "Chorus" else -10 if kind == "Verse" else -4 if kind in ("Bridge", "Outro") else 0   # 9.12
    kick = not (kind == "Intro" and k < 4) and not (kind == "Bridge" and k < n - 2) and not (kind == "Outro" and k >= 4)
    if kick: [ev(drums, st + e, 3, DR["kick"], (100 if e == 0 else 92) + min(lift, 8)) for e in (0, 12, 24, 36)]
    if kick and kind == "Chorus": [ev(drums, st + e, 3, DR["ohh"], 70 + lift) for e in (6, 18, 30, 42)]
    if kick and kind in ("Verse", "Intro", "Outro"): [ev(drums, st + e, 3, DR["chh"], 52 + lift) for e in (6, 18, 30, 42)]
    if kind in ("Pre", "Chorus") or (sec == "Verse 2" and k >= 2): [ev(drums, st + e, 3, DR["clap"], 94 + min(lift, 10)) for e in (12, 36)]
    if (kind == "Pre" and k == n - 1) or (kind == "Bridge" and k >= n - 2):
        [ev(drums, st + e, 3, DR["snare"], 58 + e // 2, "build") for e in range(0, 48, 6 if (kind == "Bridge" and k == n - 2) else 3)]
    if kind == "Chorus" and (k == 0 or (sec == "Last Chorus" and k == 8)): ev(drums, st, 3, DR["crash"], 100 + min(lift, 10))
    for h in (0, 1):                                                                       # the pad: the half-bar's chord, sidechained (a swell on each beat)
        ch = H2[2 * (st // BAR) + h]
        if not (kind == "Intro" and k < 4):
            for e in (0, 12):
                ev(pad, st + 24 * h + e, 11, chord3(ch, 57) + ([chord3(ch, 57)[0] + 12] if kind == "Chorus" else []), (48 if kind != "Bridge" else 56) + lift // 2,
                   "pad sidechained" + (" filtered" if kind in ("Verse", "Pre") else ""))
        if kind in ("Intro", "Chorus") or (kind == "Verse" and True) or (kind == "Outro" and k < 4) or (kind == "Bridge" and k >= n - 4):
            step_ = 3 if kind == "Chorus" else 6
            tn = chord3(ch, 64); seq = tn + [tn[1]]
            for j, e in enumerate(range(0, 24, step_)):
                ev(arp, st + 24 * h + e, step_ - 1, [seq[j % 4] + (12 if (kind == "Chorus" and j % 8 == 7) else 0)], (64 if step_ == 3 else 54) + lift // 2,
                   "arp" + (" filtered" if kind == "Verse" else ""))
    if kind == "Intro" or (kind == "Outro"): ev(rain, st, BAR, [60], 46 if kind == "Intro" else 54, "rain")
    if (kind == "Intro" and k < 4) or (kind == "Outro" and k >= 4): ev(hum, st, BAR, [45, 52], 44, "hum")
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); continue
        out.append(e)
    return out
drums = tidy(drums); pad = tidy(pad); arp = tidy(arp); rain = tidy(rain); hum = tidy(hum)
plan = [(nm, nb, P.BAR0[nm], "4/4") for nm, _, nb in P.FORM]
secs = NB * 4 * 60 / QB
rec = dict(title="Dry Ground", nbars=NB, bars=bars, chords2=H2, bass8=dict(F["run"]["bass8"]), plan=plan, lead=lead, drums=drums, pad=pad, arp=arp, rain=rain, hum=hum,
           slot="twelfth of a beat", bar=BAR, qbpm=QB, feel=P.FEEL, seconds=secs, tw_sec=60 / QB / 12, fp=c["fp"],
           order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"], meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()},
           judge={k: c["judge"][k] for k in ("combined", "content", "order")}, plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"],
           kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()}, rerun=F["run"]["rerun"], text=TEXT, lift=c["info"]["lift"], registers=c["meta"]["registers"],
           palettes=c["meta"]["palettes"], outside_target=c["meta"]["outside_target"], carriers=c["meta"]["carriers"],
           design=dict(gates=P.DESIGN_GATES, slots={s: P.slots_of(s) for s in P.SUNG}, falsetto=P.FALSETTO), chart438=F["run"]["rerun"].get("chart438"))
B, tries = BV.write_bass(rec, 33, (9, "minor"), "46")
last_b = (NB - 1) * BAR
B = [e for e in B if e["on"] < last_b] + [dict(on=last_b, dur=BAR, p=[33], vel=84, art="ring")]   # the last bar: the A, let ring
rec["bass"] = B; rec["bass_written_by"] = "bass_v130.py write_bass (439, 445-448, 516, 517, 538; v130)"; rec["bass_tries"] = tries
pickle.dump(rec, open("/home/claude/p56/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s;", len(lead), "sung;", {k: len(v) for k, v in dict(drums=drums, bass=B, pad=pad, arp=arp, rain=rain, hum=hum).items()}, "bass tries", tries)
    for sec in P.SUNG:
        for i, ws in enumerate(TEXT[sec]): print(sec, i, " ".join(t + ("-" if h else "") for t, h in ws))
