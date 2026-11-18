"""Luthier v15, stage 5b (Module 27.96; fixes 825-832): the band, a harmony voice, the song's edges and the checks that need no ear, in any metre.

    import band; band.arrange(rec, genre="pop", lead="guitar")      # rec: a record from song_from_lyric.write; adds rec["parts"], rec["levels"], rec["band_checks"]

Every choice is read from a kept table where one exists, and says so where one does not:
  825 edges      intro and outro in kept seconds at the song's tempo (studies/edges: 13.3 s in; a cold ending's outro 19.5 s, capped at eight bars); edges() below
  826 levels     a section's level is its role's kept piano density over the chorus's (POP909 by role): intro .61, verse .78, bridge .94, break .86, chorus 1, outro .75
  827 drums      4/4: the genre's commonest kept kick and snare bars and eighth-note hats (LPD by genre); drums enter at the intro's second bar (kept median);
                 fills at the kept rate (3 bars in 100), on the last bar before a chorus. Other metres have no kept drum table: kick on the bar's first beat,
                 snare on its other beats, hats on the eighths - a rule, flagged in the record.
  828 chords     the lead instrument's commonest kept bar rhythm; in a chorus the commonest that is busier (kept choruses are denser than verses). 4/4 from the
                 genre tables; other metres from the kept piano accompaniments of that metre (the Lieder table: art song, the only kept accompaniment by metre).
                 Three notes of the chord inside the instrument's kept register, under the sung note, nearest the last voicing, inside the low-interval limits.
  829 harmony    a second voice in the choruses, in the lead's rhythm and words, below it: each note's interval class drawn at the kept shares for a voice below
                 the lead in popular two-voice scores (PDMX: thirds 25, fifths 15, octaves 13, unisons 13, fourths 10, sixths 9 in a hundred), chord tones on
                 the beats, the nearest move preferred, no two perfect fifths or octaves in a row.
  830 the break  kept songs have a mid-song instrumental 61 times in a hundred, eight bars at the median, after a chorus; the engine writes one after the second
                 chorus when a sung section follows, on the verse's chords (kept: its own 48, the verse's 30, the chorus's 20; 'its own' waits for the solo writer).
  831 checks     low-interval limits, accompaniment above or a second from the sung note, the harmony voice's intervals and parallels against the kept,
                 crossings, sung phrases over eight seconds, the bass and the kick together.
Deterministic for a seed. Ticks are twelfths of a quarter note."""
import json, os, random, collections, math
HERE = os.path.dirname(os.path.abspath(__file__)); ST = os.path.join(HERE, "..", "..", "studies")
LPD = json.load(open(os.path.join(ST, "arrangement", "lpd_band_tables.json")))["by_genre"]; TEX = json.load(open(os.path.join(ST, "arrangement", "pop909_texture.json")))["by_role"]
EDG = json.load(open(os.path.join(ST, "edges", "edges_tables.json")))["all"]; VOX = json.load(open(os.path.join(ST, "voices", "voices_pdmx_results.json")))["popular | 2 voices, both with words"]
SOLO = json.load(open(os.path.join(ST, "solos", "solos_results.json")))
LIED = json.load(open(os.path.join(HERE, "..", "..", "tables", "metre_atlas", "accompaniment_lieder.json")))["by_metre"]
LOW_LIMIT = {1: 60, 2: 60, 3: 53, 4: 53, 5: 46, 6: 47, 7: 34, 8: 41, 9: 41, 10: 41, 11: 41}       # Module 9.14
ROLE = {"intro": "intro", "verse": "A", "chorus": "B", "bridge": "other sung", "pre": "other sung", "solo": "instrumental", "outro": "outro"}
DR = dict(kick=36, snare=38, hat=42, tom_hi=48, tom_mid=45, tom_lo=41)
ICLASS = {0: "unison", 3: "3rd", 4: "3rd", 5: "4th", 7: "5th", 8: "6th", 9: "6th", 12: "octave"}

def edges(bpm, metre_beats, compound=False):
    """825: bars in and out. bpm counts the metre's beat."""
    bar_s = 60.0 / bpm * metre_beats; even = lambda x: max(2, int(round(x / 2.0)) * 2)
    return even(EDG["intro_s"][1] / bar_s), min(8, even(EDG["outro_s_cold"][1] / bar_s))
def break_after(form):
    """830: index of the section a mid-song instrumental follows, or None"""
    ch = [i for i, (n, k, b) in enumerate(form) if k == "chorus"]
    if len(ch) >= 2 and any(k in ("verse", "chorus", "bridge") for _, k, _ in form[ch[1] + 1:]): return ch[1]
    return None
def levels(form):
    top = TEX["B"]["piano_per_beat"][1]; return {n: round(TEX[ROLE.get(k, "A")]["piano_per_beat"][1] / top, 2) for n, k, b in form}

def _pat16(p, barlen): return [i * barlen // 16 for i, c in enumerate(p) if c == "x"]
def chord_patterns(metre, inst, genre, barlen):
    """[(onsets in the bar, kept share)], commonest first, empty bars left out"""
    if metre == "4/4": return [(_pat16(p, barlen), w) for p, w in LPD[genre][inst]["rhythm"] if "x" in p], "the genre's kept bars for the instrument (LPD)"
    L = LIED.get(metre)
    if L: return [(list(dict.fromkeys(p)), c) for p, c in L["rh_patterns"] if p], "kept piano accompaniments in this metre (Lieder; art song)"
    return [([0], 1)], "no kept table: one chord a bar"
def drum_bar(metre, genre, barlen, beats):
    if metre == "4/4":
        D = LPD[genre]["drums"]; kick = next(p for p, w in D["kick"] if "x" in p); snare = next(p for p, w in D["snare"] if "x" in p)
        return _pat16(kick, barlen), _pat16(snare, barlen), list(range(0, barlen, 6)), "the genre's commonest kept kick and snare bars, eighth-note hats (LPD)"
    return [0], [b for b in beats if b], list(range(0, barlen, 6)), "no kept drum table for this metre: kick on the first beat, snare on the others, hats on the eighths (a rule)"

def arrange(rec, genre="pop", lead="guitar", seed=1):
    rng = random.Random(f"band {seed}"); BAR, BEATS = rec["bar"], rec["beats"]; metre = rec["metre"]; inst = "piano" if lead in ("piano", "keys", "organ", "synthesizer", "strings") else "guitar"
    G = LPD[genre][inst]; tonic = rec["key"]["tonic_midi"] % 12; form = [tuple(f) for f in rec["form"]]; LV = levels(form); parts = collections.defaultdict(list); notes_ = rec["melody"]["notes"]
    import chord_writer as C
    # the chord sounding at every tick a chord begins
    starts = []; b = 0; sec_of_bar = []
    for n, k, nb in form:
        for bar in rec["roman"][n]:
            bar = bar.split(); at = C.place(bar, BAR, BEATS)
            for j, rn in enumerate(bar): starts.append((b * BAR + at[j], rn))
            sec_of_bar.append((n, k)); b += 1
    NB = b; st_t = [t for t, _ in starts]
    def chord(t):
        import bisect; return starts[max(0, bisect.bisect_right(st_t, t) - 1)][1]
    def tones(rn): return {(x + tonic) % 12 for x in C.tones(rn)}
    sung = collections.defaultdict(list)
    for n in notes_:
        for t in range(n["on"], n["on"] + max(3, n["dur"]), 3): sung[t].append(n["midi"])
    def sung_in(t0, t1): return [p for t in range(t0 - t0 % 3, t1, 3) for p in sung.get(t, [])]
    # 828 the chordal part
    pats, src_c = chord_patterns(metre, inst, genre, BAR); verse_p = pats[0][0]; cap_on = G["onsets_a_bar"][2] if metre == "4/4" else 10 ** 6; chorus_p = next((p for p, w in pats if len(verse_p) < len(p) <= cap_on), verse_p)      # busier, but inside the kept 75th of onsets a bar
    lo, hi = int(G["low"][1]), int(G["high"][1]); held = G["held"][1]; prev = None
    def voicing(rn, cap):
        nonlocal prev
        pool = [q for q in range(lo, min(hi, cap) + 1) if q % 12 in tones(rn)]
        if len(pool) < 3: pool = [q for q in range(lo - 7, min(hi, cap) + 1) if q % 12 in tones(rn)]
        best = None
        for i in range(len(pool)):
            for j in range(i + 1, len(pool)):
                for k in range(j + 1, len(pool)):
                    v = (pool[i], pool[j], pool[k])
                    if v[2] - v[0] > 12 or len({q % 12 for q in v}) < 3: continue
                    if any(0 < y - x < 12 and x < LOW_LIMIT[y - x] for x, y in zip(v, v[1:])): continue
                    cost = sum(abs(x - y) for x, y in zip(v, prev)) if prev else -v[2] * 0.01
                    if best is None or (cost, v) < best: best = (cost, v)
        if best is None: return None
        prev = best[1]; return list(best[1])
    for bi in range(NB):
        n, k = sec_of_bar[bi]; pat = chorus_p if k == "chorus" else verse_p; vel = int(48 + 34 * LV[n]); t0 = bi * BAR
        cuts = sorted(set(pat) | {t - t0 for t in st_t if t0 <= t < t0 + BAR})
        for j, x in enumerate(cuts):
            t = t0 + x; t1 = t0 + (cuts[j + 1] if j + 1 < len(cuts) else BAR); s = sung_in(t, t1); v = voicing(chord(t), (min(s) - 1) if s else hi)
            if v: parts["chords"].append(dict(on=t, dur=max(3, int((t1 - t) * held)), p=v, vel=vel))
    # 827 drums
    kick, snare, hats, src_d = drum_bar(metre, genre, BAR, BEATS); enter = int(LPD[genre]["drums_enter_bar"][1]); fills = []; intro_bars = form[0][2] if form[0][1] == "intro" else 0
    want = max(1, int(round(LPD[genre]["drums"]["fill_rate"][1] * NB))); before_chorus = [bi for bi in range(NB - 1) if sec_of_bar[bi + 1][1] == "chorus" and sec_of_bar[bi][1] != "chorus"]
    fills = set(before_chorus[:: max(1, len(before_chorus) // want)][:want]) if before_chorus else set()
    for bi in range(NB):
        if bi < min(enter, max(0, intro_bars - 1)): continue
        n, k = sec_of_bar[bi]; vel = int(60 + 36 * LV[n]); t0 = bi * BAR
        if bi in fills:
            half = BAR // 2
            for x in kick + snare + hats:
                if x < half: parts["drums"].append(dict(on=t0 + x, dur=3, p=[DR["kick"] if x in kick else DR["snare"] if x in snare else DR["hat"]], vel=vel))
            steps = list(range(half, BAR, 6))
            for j, x in enumerate(steps): parts["drums"].append(dict(on=t0 + x, dur=3, p=[DR[["snare", "tom_hi", "tom_mid", "tom_lo"][min(3, j * 4 // max(1, len(steps)))]]], vel=vel + j))
            continue
        for x in kick: parts["drums"].append(dict(on=t0 + x, dur=3, p=[DR["kick"]], vel=vel))
        for x in snare: parts["drums"].append(dict(on=t0 + x, dur=3, p=[DR["snare"]], vel=vel))
        for x in hats: parts["drums"].append(dict(on=t0 + x, dur=3, p=[DR["hat"]], vel=vel - 26 + (6 if x in BEATS else 0)))
    # 829 the harmony voice, in the choruses, below the lead
    below = {k: v for k, v in VOX["below"].items()}; scale = {(x + tonic) % 12 for x in rec["spec"]["scale"]}; hv = []; last = None; lastiv = None; lastlead = None
    for n in notes_:
        if "horus" not in n["sec"]: last = None; lastiv = None; lastlead = None; continue
        ct = tones(chord(n["on"])); onbeat = (n["on"] % BAR) in BEATS; cands = []
        for iv, cls in ICLASS.items():
            p = n["midi"] - iv
            if p % 12 not in scale and p % 12 not in ct: continue
            if onbeat and p % 12 not in ct and iv != 0: continue
            if lastiv in (7, 12) and iv == lastiv and last is not None and p != last and rng.random() > 0.3: continue      # perfect fifths and octaves in a row kept rare (kept: 9 motions in 100)
            w = below.get(cls, 0.01) / (2 if cls in ("3rd", "6th") else 1)                                     # a class of two sizes shares its weight
            if last is not None:
                w *= math.exp(-abs(p - last) / 6.0)                                                            # the nearest move
                if n["midi"] == lastlead and p == last and iv: w *= 8.0                                               # the lead holds: the harmony holds (kept: static 23 in 100)
                elif n["midi"] != lastlead and iv and ICLASS[iv] == ICLASS.get(lastiv): w *= 3.0                     # the lead moves: the harmony moves with it (kept: parallel 28 in 100)
            cands.append((p, iv, w))
        if not cands: last = None; lastiv = None; continue
        p, iv, _ = rng.choices(cands, [c[2] for c in cands])[0]; hv.append(dict(on=n["on"], dur=n["dur"], p=[p], vel=70, text=n["text"], lead=n["midi"])); last = p; lastiv = iv; lastlead = n["midi"]
    parts["harmony"] = hv
    parts["bass"] = [dict(on=x["on"], dur=x["dur"], p=[x["midi"]], vel=int(62 + 30 * LV[sec_of_bar[min(NB - 1, max(0, x["on"] // BAR))][0]])) for x in rec["bass"]]
    rec["parts"] = {k: v for k, v in parts.items()}; rec["levels"] = LV
    rec["band_sources"] = dict(chords=src_c, drums=src_d, harmony="kept shares of a voice below the lead, popular two-voice scores (PDMX)", levels="kept piano density by role over the chorus's (POP909)",
                               chord_patterns=dict(verse=verse_p, chorus=chorus_p), fills=sorted(fills), genre=genre, instrument=inst)
    rec["band_checks"] = checks(rec, chord, tones); return rec

def checks(rec, chord, tones):
    """831"""
    BAR, BEATS = rec["bar"], rec["beats"]; P = rec["parts"]; ns = rec["melody"]["notes"]; out = {}
    ch = P.get("chords", []); low = sum(1 for e in ch for x, y in zip(sorted(e["p"]), sorted(e["p"])[1:]) if 0 < y - x < 12 and x < LOW_LIMIT[y - x]); out["chord voicings inside the low-interval limits"] = low == 0
    def acc_at(t): return [q for e in ch if e["on"] <= t < e["on"] + e["dur"] for q in e["p"]]
    above = second = 0
    for n in ns:
        a = acc_at(n["on"]); above += any(q > n["midi"] for q in a); second += any(0 < abs(q - n["midi"]) <= 2 for q in a)
    out["sung notes with accompaniment above them, share"] = round(above / len(ns), 3); out["sung notes with accompaniment a second away, share"] = round(second / len(ns), 3)
    hv = P.get("harmony", [])
    if hv:
        ivs = [e["lead"] - e["p"][0] for e in hv]; cls = collections.Counter(ICLASS[i] for i in ivs); n = len(ivs)
        out["harmony voice: interval classes, written / kept below the lead"] = {k: [round(cls[k] / n, 3), VOX["below"].get(k)] for k in ("3rd", "5th", "octave", "unison", "4th", "6th")}
        par = sum(1 for a, b, x, y in zip(ivs, ivs[1:], hv, hv[1:]) if a == b and a in (7, 12, 0) and x["p"][0] != y["p"][0] and y["on"] - x["on"] < BAR)
        mot = collections.Counter();
        for x, y in zip(hv, hv[1:]):
            if y["on"] - x["on"] >= BAR: continue
            dl, dh = y["lead"] - x["lead"], y["p"][0] - x["p"][0]; mot["static" if dl == 0 and dh == 0 else "oblique" if dl == 0 or dh == 0 else "contrary" if dl * dh < 0 else "parallel" if dl == dh else "similar"] += 1
        m = sum(mot.values()) or 1
        out["harmony voice: parallel perfect fifths, octaves and unisons a hundred motions, written / kept"] = [round(100 * par / m, 1), VOX["parallel_P5_P8_per_100"]]
        out["harmony voice: motion, written / kept"] = {k: [round(mot[k] / m, 3), VOX["motion"].get(k if k != "parallel" else "parallel exact")] for k in ("static", "oblique", "contrary", "parallel", "similar")}
        out["harmony voice crosses the lead"] = sum(e["p"][0] > e["lead"] for e in hv); out["harmony voice a second from the lead"] = sum(0 < e["lead"] - e["p"][0] <= 2 for e in hv)
    spt = 60.0 / rec["bpm"] / (18 if rec["metre"] in ("6/8", "9/8", "12/8") else 12); phrases = []; start = ns[0]["on"]
    for a, b in zip(ns, ns[1:]):
        if b["on"] - (a["on"] + a["dur"]) >= 12: phrases.append((a["on"] + a["dur"] - start) * spt); start = b["on"]
    phrases.append((ns[-1]["on"] + ns[-1]["dur"] - start) * spt)
    out["sung phrases, seconds (median, longest)"] = [round(sorted(phrases)[len(phrases) // 2], 1), round(max(phrases), 1)]; out["sung phrases over eight seconds"] = sum(p > 8 for p in phrases)
    kicks = {e["on"] for e in P.get("drums", []) if e["p"] == [DR["kick"]]}; bs = P.get("bass", [])
    out["kicks with a bass note on them, share"] = round(sum(any(b["on"] == t for b in bs) for t in kicks) / max(1, len(kicks)), 3)
    dens = collections.defaultdict(list)
    for name, kind, nb in rec["form"]: dens[kind].append(1)
    return out

def midi(rec, path):
    import mido
    tpq = 480; f = 40; mid = mido.MidiFile(ticks_per_beat=tpq); bpm = rec["bpm"] * (1.5 if rec["metre"] in ("6/8", "9/8", "12/8") else 1.0); off = rec["bar"]
    meta = mido.MidiTrack(); mid.tracks.append(meta); num, den = (int(x) for x in rec["metre"].split("/")); meta.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm))); meta.append(mido.MetaMessage("time_signature", numerator=num, denominator=den))
    def track(name, prog, chan, evs):
        tr = mido.MidiTrack(); mid.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=name)); msgs = []
        if chan != 9: tr.append(mido.Message("program_change", program=prog, channel=chan))
        for e in evs:
            for p in e["p"]: msgs += [((e["on"] + off) * f, 1, p, e.get("vel", 80)), ((e["on"] + off + e["dur"]) * f - 1, 0, p, 0)]
        last = 0
        for t, kind, p, v in sorted(msgs): tr.append(mido.Message("note_on" if kind else "note_off", note=p, velocity=v, channel=chan, time=max(0, t - last))); last = max(last, t)
    track("voice", 52, 0, [dict(on=n["on"], dur=n["dur"], p=[n["midi"]], vel=96) for n in rec["melody"]["notes"]]); P = rec["parts"]
    track("harmony voice", 53, 1, P.get("harmony", [])); track("chords", 25 if rec["band_sources"]["instrument"] == "guitar" else 0, 2, P.get("chords", [])); track("bass", 33, 3, P.get("bass", [])); track("drums", 0, 9, P.get("drums", []))
    if P.get("break"): track("lead", 27 if rec["band_sources"]["instrument"] == "guitar" else 0, 4, P["break"])
    mid.save(path)
