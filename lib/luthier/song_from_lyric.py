"""Luthier v14, stage 5a (Module 27.95; fixes 812-816): a song from its lyric, with nothing chosen by hand.

    python3 lib/luthier/song_from_lyric.py songs/p65/lyric55.json [builds, default 1000] [chord drafts, default 12]

The lyric file holds the words by section and five settings: metre, bpm (beats a minute; in 6/8 the dotted quarter), voice, lead instrument, mode.
Everything else is the engine's:
  syllables and stresses      lib/carol/lyricsearch.py
  bars a line (763)           lib/luthier/slots.py, one or two bars; a section of an odd count of bars rests a bar at its end
  the form                    the sections in the lyric's order, four bars in and four out
  returns (712, 780)          a later verse sings the first verse's lines again; a line whose words return is copied
  registers (814)             on the tonic: the verse from the tonic to a sixth above, the chorus from a third to a ninth above (settings, for stage 6)
  chords (800-809)            lib/luthier/chord_writer.py: drafts, the pick on kept chord readings
  melody (790, 812)           lib/luthier/metre_engine.py; a 4/4 song is read against the kept pop songs (tables/metre_atlas/4-4_pop_sung.json)
  key (804)                   from the pick's range, the voice and the lead instrument
  bass (813)                  the root where a chord begins; one note a beat; the fifth on the mid-bar beat of a held chord; a step toward the next root before a change
Writes <lyric>.song.json (the record: chords, melody, bass, key, every reading) and <lyric>.song.mid. The same lyric and seed give the same song."""
import json, sys, os, re, copy, hashlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "carol")]
import chord_writer as C, metre_engine as M, slots as SL, lyricsearch as LS, band as BD
EARLY = True     # 834: a line that opens on a stress comes in before the bar line at the kept share, one time in five
SCALES = {"major": [0, 2, 4, 5, 7, 9, 11], "minor": [0, 2, 3, 5, 7, 8, 10]}
def kind_of(name):
    n = name.lower()
    for k, v in (("pre", "pre"), ("verse", "verse"), ("chorus", "chorus"), ("refrain", "chorus"), ("tag", "chorus"), ("bridge", "bridge"), ("intro", "intro"), ("outro", "outro")):
        if k in n: return v
    return "verse"
def syllables(line, flags):
    """the lexicon's reading; a word it does not hold is read from its stem, or by its vowel groups with the first stressed, and flagged (819)"""
    for _ in range(12):
        try: return LS.syllables(line)
        except KeyError as e:
            w = e.args[0]; ph = None
            for suf, add in (("ed", " D"), ("s", " Z"), ("ing", " IH0 NG"), ("ly", " L IY0"), ("d", " D"), ("es", " IH0 Z"), ("er", " ER0"), ("in'", " IH0 N")):
                if w.endswith(suf):
                    try: ph = LS.phones(w[:-len(suf)]) + add; break
                    except KeyError: pass
            if ph is None: n = max(1, len(re.findall(r"[aeiouy]+", re.sub(r"e$", "", w)))); ph = " ".join(["AH1"] + ["AH0"] * (n - 1))
            LS.OVERRIDE[w] = (ph,); flags.append(f"'{w}' is not in the lexicon; read as {ph}")
    raise KeyError(line)
def base(name): return re.sub(r"^(Last|Final)\s+", "", re.sub(r"\s*\d+$", "", name))
def plan(L):
    """lyric -> the melody spec without chords, and the form"""
    metre = L.get("metre", "4/4"); T = json.load(open(os.path.join(M.ATLAS, metre.replace("/", "-") + "_sung.json"))); beats = len(T["beats"])
    sung = []; slots = {}; how = {}; first = {}; texts = {}; n_in, n_out = BD.edges(L["bpm"], beats); form = [("Intro", "intro", n_in)]; flags = []      # 825
    for name, lines in L["sections"]:
        sy = [[(w, bool(st)) for w, v, st, fn in syllables(ln, flags)] for ln in lines]; k = kind_of(name)
        pr = SL.propose([len(x) for x in sy], L["bpm"], beats); sl = [max(1, min(4, r["whole bars proposed"])) for r in pr]
        for i, r in enumerate(pr):
            if r["whole bars proposed"] > 2: flags.append(f"{name} line {i + 1}: a slot of {min(4, r['whole bars proposed'])} bars, past the kept two-bar windows: set by weighted placement (760)")
        sung.append([name, "Chorus" if k == "chorus" else "Bridge" if k == "bridge" else "Verse", sy]); slots[name] = sl; n = sum(sl); form.append((name, k, n + n % 2))
        src = first.get(base(name))
        for i, ln in enumerate(lines):
            key = re.sub(r"[^a-z ]", "", ln.lower()).strip()
            if key in texts and len(sy[i]) == len(texts[key][2]): how[f"{name}:{i}"] = ["copy", texts[key][0], texts[key][1]]          # the words return: the line is copied
            elif src is not None and i < len(src): how[f"{name}:{i}"] = ["again", first_name[base(name)], i]
            texts.setdefault(key, (name, i, sy[i]))
        if src is None: first[base(name)] = lines; first_name[base(name)] = name
    form.append(("Outro", "outro", n_out)); br = BD.break_after(form)
    if br is not None: form.insert(br + 1, ("Break", "solo", 8))                                # 830
    spec = dict(title=L["title"], metre=metre, seed=L.get("seed", 1), scale=[(x + 0) % 12 for x in SCALES[L.get("mode", "major")]], sung=sung, slots=slots, how=how,
                registers={"Verse": [64, 60, 69], "Chorus": [68, 63, 74], "Bridge": [65, 60, 71]}, clash_rule=True, borrow=dict(rhythm=0.0, figure=0.6), early_entries=EARLY)      # 818: kept songs sing six bars in ten on a rhythm already sung
    if metre == "4/4": spec["table"] = "4-4_pop_sung"
    return spec, form, flags
first_name = {}
def bass(form_bars, tonic_midi, barlen, beats, mode):
    """813. form_bars: [(bar index, [roman chords])]; returns [(on, dur, midi)] in twelfths, the tonic at tonic_midi (28 to 39)."""
    ev = []; half = barlen // 2 if barlen // 2 in beats else None; flat = []
    for b, bar in form_bars:
        at = C.place(bar, barlen, beats)
        for j, rn in enumerate(bar): flat.append((b * barlen + at[j], rn))
    def root(rn):
        pc = (tonic_midi + root_pc(rn)) % 12; return min((r for r in range(28, 46) if r % 12 == pc), key=lambda r: (abs(r - 37.5), r))     # the bass guitar's low E up; nearest the kept median pitch (35.5 to 39.5)
    for i, (t0, rn) in enumerate(flat):
        t1 = flat[i + 1][0] if i + 1 < len(flat) else t0 + barlen; r = root(rn); nxt = root(flat[i + 1][1]) if i + 1 < len(flat) else r
        ons = [t for t in range(t0, t1) if (t % barlen) in beats]
        for j, t in enumerate(ons):
            p = r
            if j == len(ons) - 1 and j > 0 and nxt != r: p = nxt + (1 if nxt < r else -1) if abs(nxt - r) > 2 else r           # a step into the next root
            elif j > 0 and half is not None and t % barlen == half and t1 - t0 >= barlen: p = r - 5 if r - 5 >= 28 else r + 7   # the fifth on the mid-bar beat of a held chord
            ev.append((t, (ons[j + 1] if j + 1 < len(ons) else t1) - t, p))
    return ev
def root_pc(rn):
    m = re.match(r"(b|#)?(VII|III|IV|VI|II|V|I|vii|iii|iv|vi|ii|v|i)", rn); return (C.DEG[m.group(2).upper()] + (-1 if m.group(1) == "b" else 1 if m.group(1) == "#" else 0)) % 12
def write(L, N=1000, K=12):
    spec, form, flags = plan(L); mode = L.get("mode", "major"); W = C.Writer(mode, chromatic=L.get("chromatic", 1.0)); drafts = []
    names = [(base(n) + " 9" if n != base(n) and not re.search(r"\d+$", n) else n, k, b) for n, k, b in form]; wn = {f[0]: w[0] for f, w in zip(form, names)}      # a last chorus returns the chorus (801)
    for seed in range(1, K + 1):
        pl = W.song(names, seed=seed * 1000 + L.get("seed", 1), require=L.get("require")); pl = {n: pl[wn[n]] for n, _, _ in form}; c, d, r = W.charge(list(pl.values())); drafts.append((c, d, seed, pl, r))
    least = min(x[0] for x in drafts); c, d, seed, pl, cr = min((x for x in drafts if x[0] <= least + 0.05), key=lambda x: (x[1], x[2]))              # 809
    if "Break" in pl:                                                                        # 830: the break on the first verse's chords
        v1 = next((pl[n] for n, k, b in form if k == "verse"), None)
        if v1: pl["Break"] = [v1[i % len(v1)] for i in range(8)]
    spec["chords"] = {}; spec["form"] = []
    for n, k, b in form:
        bars = []
        for bar in pl[n]:
            for x in bar: spec["chords"][x] = sorted((t + 0) % 12 for t in C.tones(x))
            bars.append(bar[0] if len(bar) == 1 else list(bar))
        spec["form"].append([n, bars])
    E = M.Engine(spec); run = E.run(N, L.get("seed", 1))
    if not run["survivors"]: return dict(error="no build survived", deaths=run["deaths"], flags=flags, spec=spec)
    notes = run["pick"]["notes"]; lo, hi = min(n["p"] for n in notes) - 60, max(n["p"] for n in notes) - 60
    keys = C.choose_key(lo, hi, L.get("voice", "tenor"), L.get("lead", "guitar"), mode)
    if not keys: return dict(error="the melody does not fit the voice in any key", range=[lo, hi], flags=flags)
    key = keys[0]; shift = key["tonic_midi"] - 60; tonic = key["key"]; bt = 24 + key["tonic_midi"] % 12; bt = bt + 12 if bt < 28 else bt
    fb = []; b = 0
    for n, k, nb in form:
        for bar in pl[n]: fb.append((b, list(bar))); b += 1
    bs = bass(fb, bt, E.BAR, E.BEATS, mode)
    rec = dict(title=L["title"], metre=spec["metre"], bpm=L["bpm"], key=key, other_keys=keys[1:3], flags=flags, form=[[n, k, nb] for n, k, nb in form],
               chords={n: [" ".join(C.name(x, tonic) for x in bar) for bar in pl[n]] for n, _, _ in form}, roman={n: [" ".join(bar) for bar in pl[n]] for n, _, _ in form},
               chord_pick=dict(draft=seed, drafts=K, charge=round(c, 3), readings=cr, kept=W.Q),
               melody=dict(made=run["made"], survivors=run["survivors"], deaths=run["deaths"], pick=run["pick"]["fp"], charge=run["pick"]["charge"], median_charge=run["median_charge"], readings=run["pick"]["readings"],
                           kept=run["kept_quartiles"], uncharged=run["uncharged"], entries=run["entries"], stressed_on_beat=run["pick"]["stressed_on_beat"], stats=run["stats"],
                           notes=[dict(on=n["on"], dur=n["dur"], midi=n["p"] + shift, sec=n["sec"], line=n["line"], text=n["text"], stress=n["stress"]) for n in notes]),
               bass=[dict(on=t, dur=dd, midi=p) for t, dd, p in bs], bar=E.BAR, beats=E.BEATS, spec=spec, chord_tones={x: sorted((t + key["tonic_midi"]) % 12 for t in C.tones(x)) for x in spec["chords"]})
    rec["checks"] = checks(rec, fb, key["tonic_midi"], E); BD.arrange(rec, genre=L.get("genre", "pop"), lead=L.get("lead", "guitar"), seed=L.get("seed", 1))
    if any(n == "Break" for n, _, _ in form):                                                # 830: the lead instrument plays the first verse's tune over the break
        b0 = sum(nb for n, k, nb in form[:[n for n, _, _ in form].index("Break")]) * E.BAR; vname = next(n for n, k, b in form if k == "verse"); v0 = sum(nb for n, k, nb in form[:[n for n, _, _ in form].index(vname)]) * E.BAR
        rec["parts"]["break"] = [dict(on=n["on"] - v0 + b0, dur=n["dur"], p=[n["midi"] + (12 if L.get("lead", "guitar") == "guitar" else 0)], vel=88) for n in rec["melody"]["notes"] if n["sec"] == vname and n["on"] - v0 < 8 * E.BAR - 6]
    return rec
def checks(rec, fb, tonic_midi, E):
    """815: what can be checked without ears"""
    ns = rec["melody"]["notes"]; bs = rec["bass"]; on = [n["on"] for n in ns]
    chord_at = {}
    for b, bar in fb:
        at = C.place(bar, E.BAR, E.BEATS)
        for j, rn in enumerate(bar): chord_at[b * E.BAR + at[j]] = rn
    starts = sorted(chord_at)
    def ch(t): return chord_at[max(x for x in starts if x <= max(t, 0))]
    tp = tonic_midi % 12; beat_notes = [n for n in ns if (n["on"] % E.BAR) in E.BEATS]; tone = lambda n: (n["midi"] - tp) % 12 in C.tones(ch(n["on"]))
    clash = [n for n in ns if n["dur"] >= E.BEAT and not tone(n) and any(((n["midi"] - tp) % 12 - x) % 12 in (1, 11) for x in C.tones(ch(n["on"])))]
    return {"no two sung notes on one onset": all(b > a for a, b in zip(on, on[1:])), "no sung note of no length": all(n["dur"] > 0 for n in ns),
            "the melody inside the voice": [min(n["midi"] for n in ns), max(n["midi"] for n in ns)], "sung notes on a beat that are chord tones, share": round(sum(tone(n) for n in beat_notes) / max(1, len(beat_notes)), 3),
            "sung notes a beat long or more a semitone from a chord tone": len(clash), "bass notes": len(bs), "the bass on the root where a chord begins": all(any(b["on"] == t and (b["midi"] - tp) % 12 == root_pc(rn) for b in bs) for t, rn in chord_at.items()),
            "the bass under the voice everywhere": max(b["midi"] for b in bs) < min(n["midi"] for n in ns), "bass register": [min(b["midi"] for b in bs), max(b["midi"] for b in bs)]}
def midi(rec, path):
    import mido
    tpq = 480; f = 40; mid = mido.MidiFile(ticks_per_beat=tpq); bpm = rec["bpm"] * (1.5 if rec["metre"] in ("6/8", "9/8", "12/8") else 1.0)
    def track(name, prog, chan, evs):
        tr = mido.MidiTrack(); mid.tracks.append(tr); tr.append(mido.MetaMessage("track_name", name=name)); tr.append(mido.Message("program_change", program=prog, channel=chan)); msgs = []
        for t, d, p, v in evs: msgs += [(t * f, 1, p, v), ((t + d) * f - 1, 0, p, 0)]
        last = 0
        for t, kind, p, v in sorted(msgs): tr.append(mido.Message("note_on" if kind else "note_off", note=p, velocity=v, channel=chan, time=max(0, t - last))); last = max(last, t)
    meta = mido.MidiTrack(); mid.tracks.append(meta); num, den = (int(x) for x in rec["metre"].split("/")); meta.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm))); meta.append(mido.MetaMessage("time_signature", numerator=num, denominator=den))
    off = rec["bar"]                                                                         # a bar of room for a pickup
    track("voice", 52, 0, [(n["on"] + off, n["dur"], n["midi"], 92) for n in rec["melody"]["notes"]])
    track("bass", 33, 1, [(b["on"] + off, b["dur"], b["midi"], 80) for b in rec["bass"]])
    pads = []; b = 0; tm = rec["key"]["tonic_midi"] % 12
    for n, k, nb in rec["form"]:
        for bar in rec["roman"][n]:
            bar = bar.split(); at = C.place(bar, rec["bar"], rec["beats"])
            for j, rn in enumerate(bar):
                t0 = b * rec["bar"] + at[j]; t1 = b * rec["bar"] + (at[j + 1] if j + 1 < len(at) else rec["bar"])
                for x in C.tones(rn):
                    p = 48 + (x + tm) % 12; pads.append((t0 + off, t1 - t0, p if p >= 50 else p + 12, 52))
            b += 1
    track("chords", 0, 2, pads); mid.save(path)
if __name__ == "__main__":
    L = json.load(open(sys.argv[1])); N = int(sys.argv[2]) if len(sys.argv) > 2 else 1000; K = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    rec = write(L, N, K); out = sys.argv[1].replace(".json", "") + ".song.json"; json.dump(rec, open(out, "w"), indent=1, default=float)
    if "error" in rec: print(rec["error"], rec.get("deaths"), rec.get("flags")); sys.exit(1)
    BD.midi(rec, out.replace(".json", ".mid")); m = rec["melody"]
    print(f"{rec['title']} in {rec['metre']}, key {rec['key']['key']} ({rec['key']['lowest']}-{rec['key']['highest']}{', ' + rec['key']['capo'] if rec['key']['capo'] else ''}); chord draft {rec['chord_pick']['draft']} of {rec['chord_pick']['drafts']}, charge {rec['chord_pick']['charge']}")
    print(f"melody: {m['survivors']} of {m['made']} survive; pick {m['pick']} charge {m['charge']} (median build {m['median_charge']:.2f}); deaths {m['deaths']}")
    for n, k, nb in rec["form"]: print(f"  {n}: " + " | ".join(rec["chords"][n]))
    print("checks:", rec["checks"]); print("band:", rec["band_sources"]); print("levels:", rec["levels"]); print("band checks:", rec["band_checks"]); print("flags:", rec["flags"])
