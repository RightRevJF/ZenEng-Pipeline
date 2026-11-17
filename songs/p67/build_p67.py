"""Jehovah's Band (song 57): the song record, written entirely by the engine and its writers; nothing arranged by hand.
  the melody      the engine's (melody_final.pkl: Luthier v7's search, the research gates, luthier_judge5's pick), taken as drawn
  the chords      the chord writer's (writers/chords.py, chords_p67.json), with 438's chart as the run drew it
  the band        the band writer's (writers/band.py): the genre's kept tables (rock), the lane's parts (organ, rhythm guitar), one
                  song-wide level curve, the jam built from silence (the form, B)
  the bass        bass_v134.py's routine, every section
  the lead guitar the solo writer's (writers/solo.py): the jam, fills in the voice's rests (at most one each four bars, from level 0.5),
                  and the intro's instrumental hook (the chorus's first line, played twice: v7's instrumental hook; Part 30, H5)
A Grateful Dead-style jam, E major, q = 112, 4/4, 128 bars. One singer, the baritone."""
import pickle, sys, random, collections, json
sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p67", "/home/claude/zeneng-pipeline"]
import io as _io, contextlib as _cl
with _cl.redirect_stdout(_io.StringIO()): import melody_l7_p67 as P
import bass_v134 as BV
from writers.band import write_band
from writers.solo import Solo
import pyphen
M = P.M
F = pickle.load(open("/home/claude/p67/melody_final.pkl", "rb")); c = F["pick"]
EB = 48; NB = P.NBARS; QB = 112
assert list(P.CHORD2) == list(F["run"]["chords2"]), "the chart on import differs from the run's"
_PY = pyphen.Pyphen(lang="en_US")
HFIX = {"basement": ["base", "ment"], "attic": ["at", "tic"], "gravel": ["grav", "el"], "honey": ["hon", "ey"], "wasn't": ["was", "n't"],
        "carried": ["car", "ried"], "sitting": ["sit", "ting"], "Jehovah's": ["Je", "ho", "vah's"], "across": ["a", "cross"],
        "keeping": ["keep", "ing"], "angels": ["an", "gels"], "angels'": ["an", "gels'"], "glory": ["glo", "ry"], "Grinning": ["Grin", "ning"],
        "slipped": ["slipped"], "pounding": ["pound", "ing"], "running": ["run", "ning"], "Laughing": ["Laugh", "ing"], "laughing": ["laugh", "ing"],
        "dancing": ["danc", "ing"], "couldn't": ["could", "n't"], "follow": ["fol", "low"], "county": ["coun", "ty"], "sweat-stained": ["sweat-", "stained"],
        "meadow": ["mead", "ow"], "supposed": ["sup", "posed"], "drummer": ["drum", "mer"], "finger": ["fin", "ger"], "angels": ["an", "gels"],
        "daughter's": ["daugh", "ter's"], "daughter": ["daugh", "ter"], "coffee": ["cof", "fee"], "Counted": ["Count", "ed"], "fingers": ["fin", "gers"],
        "didn't": ["did", "n't"], "waitress": ["wait", "ress"], "table": ["ta", "ble"], "shining": ["shin", "ing"], "above": ["a", "bove"],
        "icebox": ["ice", "box"], "linoleum": ["li", "no", "le", "um"], "over": ["o", "ver"], "frying": ["fry", "ing"], "followed": ["fol", "lowed"],
        "picked": ["picked"], "pinched": ["pinched"], "licked": ["licked"], "closed": ["closed"], "rolled": ["rolled"], "drumming": ["drum", "ming"],
        "Sweat": ["Sweat"], "heels": ["heels"], "Leaned": ["Leaned"], "Then": ["Then"], "every": ["ev", "ery"]}
def split_words(text, sy):
    out = []; ws = text.replace('"', "").split()
    for w in ws:
        n = len(P.syl(w)); core = w.rstrip(",;:?")
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
ROLE = {"Intro": "intro", "Verse": "verse", "Chorus": "chorus", "Bridge": "bridge", "Jam": "solo", "Tag": "tag", "Ending": "outro"}
bars = []; t = 0; RS = []
for nm, kind, nb in P.FORM:
    for k in range(nb):
        b = P.BAR0[nm] + k
        bars.append(dict(sec=nm, kind=kind, role=ROLE[kind], k=k, n=nb, b=b, meter="4/4", start=t, len=EB, chord=H2[2 * b], chord2=H2[2 * b + 1],
                         roman=M.ROMAN[H2[2 * b].split("/")[0]], qbpm=QB, key="E major", movement=nm, stop=False))
        RS.append(t); t += EB
REC_END = t
SEC0 = {nm: RS[P.BAR0[nm]] for nm, _, _ in P.FORM}
lead = []
for n in c["notes"]:
    sec, i = n["line"].split(":"); i = int(i); tx, hy = TEXT[sec][i][n["syl"]]
    lead.append(dict(on=n["on"], on_engine=n["on"], dur=n["dur"], midi=n["p"], engine_midi=n["p"], sec=sec, line=i, syl=n["syl"], first=not n["slur"],
                     text=tx, hyph=hy, stress=P.LINES[sec][i][n["syl"]][1], role=M.WORDS_OF[sec][i][0], singer="him"))
CH = {k: (v[0], set(v[1])) for k, v in M.CH.items() if "/" not in k}
for k in set(H2):                                                                            # 440's inversions: the chord's tones, its bass apart
    if k not in CH: CH[k] = (CH[k.split("/")[0]][0], CH[k.split("/")[0]][1])
# ---- the band writer ----
LANE = dict(genre="rock", chords=CH, parts={"organ": "piano", "rhythm": "guitar"}, tune_on_top=False)   # a baritone under organ and guitars: 749.27
rec0 = dict(bars=bars, lead=lead)
parts, BREP = write_band(rec0, LANE, seed="song 57", ramp=("Jam",))
parts = collections.defaultdict(list, {k: list(v) for k, v in parts.items()})
# the jam's entries: before the organ's entry nothing sounds (the silence the form asked for)
# ---- the bass: the routine, every section, on the band's kicks and the voice's rests ----
BKIND = {"Intro": "Intro", "Verse": "Verse", "Chorus": "Chorus", "Bridge": "Bridge", "Jam": "Solo", "Tag": "Tag", "Ending": "Outro"}
ebars = [dict(sec=nm, kind=BKIND[kind], k=k, n=nb, chord=H2[2 * (P.BAR0[nm] + k)], start=(P.BAR0[nm] + k) * EB, len=EB) for nm, kind, nb in P.FORM for k in range(nb)]
erec = dict(bars=ebars, chords2=list(P.CHORD2), drums=list(parts["drums"]), lead=[dict(n, on=n["on_engine"]) for n in lead])
BV.SCALE_AT[0] = None
BB, tries = BV.write_bass(erec, 28, (4, "major"), "57")
JAM0 = P.BAR0["Jam"]; bass_in = BREP["sections"]["Jam"]["entries"].get("bass", 0)
for e in BB:
    x = bars[e["on"] // EB]
    if x["sec"] == "Jam" and x["k"] < bass_in: continue                                       # the jam: the bass enters when the writer says
    parts["bass"].append(dict(e))
for e in parts["bass"]: e["p"] = [q + 12 if q < 28 else q for q in e["p"]]
# ---- the lead guitar: the solo writer ----
SO = Solo(4, CH, seed="song 57", lo=52, hi=84)
LV = BREP["levels"]
def lev(sec, k): a, b = LV[sec]; nb = P.SECLEN[sec]; return a + (b - a) * (k / max(1, nb - 1))
solo_reads = {}
# the intro: the chorus's first line, an octave up, twice (the instrumental hook)
hook = [n for n in lead if n["sec"] == "Chorus 1" and n["line"] == 0]; U = P.line_start("Chorus 1", 0)
for rep in (0, 2):
    for n in hook:
        on = SEC0["Intro"] + rep * EB + (n["on"] - U)
        if 0 <= on < SEC0["Verse 1"]: parts["lead"].append(dict(on=on, dur=n["dur"], p=[n["midi"] + 12], vel=78, art=""))
# the jam: eight-bar windows from the lead's entry
lead_in = BREP["sections"]["Jam"]["entries"].get("lead", 0)
for w0 in range(lead_in, P.SECLEN["Jam"], 8):
    bs = [(SEC0["Jam"] + k * EB, bars[JAM0 + k]["chord"].split("/")[0], bars[JAM0 + k]["chord2"].split("/")[0]) for k in range(w0, min(P.SECLEN["Jam"], w0 + 8))]
    notes, rd = SO.window(bs, lambda j, w0=w0: max(0.15, lev("Jam", w0 + j)))
    solo_reads[f"Jam {w0 + 1}-{w0 + len(bs)}"] = rd
    for on, d, p in notes: parts["lead"].append(dict(on=on, dur=d, p=[p], vel=int(70 + 30 * lev("Jam", (on - SEC0["Jam"]) // EB)), art=""))
# fills in the voice's rests: a rest of a beat or more, level 0.5 or more, at most one each four bars
VON = set()
for n in lead:
    for tt in range(n["on"], n["on"] + n["dur"]): VON.add(tt)
last_fill = -99; fills = []
for x in bars:
    if x["sec"] not in P.SUNG or lev(x["sec"], x["k"]) < 0.5 or x["b"] - last_fill < 4: continue
    for h in (24, 0):
        s0 = x["start"] + h
        if not any(tt in VON for tt in range(s0, s0 + 24)):
            notes, rd = SO.window([(x["start"], x["chord"].split("/")[0], x["chord2"].split("/")[0])], lambda j: lev(x["sec"], x["k"]), tries=12)
            ns = [(on, min(d, s0 + 24 - on), p) for on, d, p in notes if s0 <= on < s0 + 24]
            if ns:
                for on, d, p in ns: parts["lead"].append(dict(on=on, dur=max(3, d), p=[min(p, 76)], vel=72, art=""))
                fills.append(x["b"]); last_fill = x["b"]; break
def tidy(lst):
    lst.sort(key=lambda e: (e["on"], e["p"][0])); out = []
    for e in lst:
        if out and out[-1]["on"] == e["on"] and out[-1]["art"] == e["art"]: out[-1]["p"] = sorted(set(out[-1]["p"] + e["p"])); out[-1]["vel"] = max(out[-1]["vel"], e["vel"]); out[-1]["dur"] = max(out[-1]["dur"], e["dur"]); continue
        out.append(e)
    return out
PARTS = {k: tidy(v) for k, v in parts.items()}
plan = [(nm, nb, SEC0[nm], ["4/4"] * nb, nm) for nm, kind, nb in P.FORM]
secs = sum(x["len"] / 12 * 60 / x["qbpm"] for x in bars)
chords_json = json.load(open("/home/claude/p67/chords_p67.json"))
rec = dict(title="Jehovah's Band", file_title="Jehovah's Band", nbars=NB, bars=bars, chords2=H2, plan=plan, lead=lead, harm=[],
           parts=PARTS, slot="twelfth of a beat", qbpm=QB, feel=P.FEEL, seconds=secs, end=REC_END, level=LV,
           fp=c["fp"], order_fp=F["run"]["order_fp"], survivors=F["run"]["survivors"], built=F["run"]["made"],
           meas={k: (float(v) if isinstance(v, (int, float)) else v) for k, v in c["meas"].items()}, judge={k: c["judge"][k] for k in ("combined", "content", "order")},
           plans=c["meta"]["plans"], hand_edits=c["hand_edits"], picked_from=c["picked_from"], kinds={f"{a}:{b}": v for (a, b), v in c["meta"]["kinds"].items()},
           rerun=F["run"]["rerun"], text=TEXT, registers=c["meta"]["registers"], carriers=c["meta"]["carriers"],
           design=dict(gates=[], half_bars={f"{a}:{b}": v for (a, b), v in P.DESIGN_HALF.items()}, slots={s: P.slots_of(s) for s in P.SUNG}),
           chart438=F["run"]["rerun"].get("chart438"), bass_written_by="bass_v134.py write_bass (every section)", bass_tries=tries,
           writers=dict(chords=chords_json["report"], band=BREP, solo=solo_reads, fills=fills, lane=dict(genre="rock", parts=LANE["parts"])),
           gates=F.get("gates"), research_pick=c["picked_from"].get("gates"))
pickle.dump(rec, open("/home/claude/p67/song_record.pkl", "wb"))
if __name__ == "__main__":
    print(NB, "bars,", f"{secs:.0f} s ({int(secs // 60)}:{secs % 60:04.1f});", len(lead), "sung;", {k: len(v) for k, v in PARTS.items()}, "bass tries", tries)
    print("levels", LV); print("jam entries", BREP["sections"]["Jam"]["entries"]); print("solo", solo_reads); print("fills at bars", fills)
    for k in ("Verse 1", "Chorus 1", "Bridge", "Jam"): print(k, BREP["sections"][k]["patterns"], BREP["sections"][k]["kick"])
