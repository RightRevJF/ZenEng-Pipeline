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
import json, math, sys, os, re, copy, hashlib
import random as _r_
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE, os.path.join(HERE, "..", "carol")]
import chord_writer as C, metre_engine as M, slots as SL, lyricsearch as LS, band as BD
FAMILY = {"pop": "other", "rock": "other", "folk": "other", "soul / r&b": "soul", "gospel": "soul", "blues": "soul", "country": "country"}
DEGREE_POWER = 0.5     # 846: fitted so the written degree shares meet the kept
WORD_PITCH = [3.0, 2.0, 0.2]     # 847: weights for the stressed syllable of a word standing higher than, level with, lower than the other; fitted to the kept 44 / 36 / 20
WORD_SHORT = 4.0      # 891 (749.66): the charge on each stressed syllable a line sung again would leave a sixteenth long
WORD_LENGTH = 2.0     # 885: fitted so the builds' fit by length meets the kept median (0.13)
WORD_PLACE = 0.75    # 913 (749.90): refitted after 912, with every kept rhythm on offer, so the builds' fit by place meets the kept median (it was 1.5 when twelve rhythms were on offer)
AIM_REPEATS = False   # 920: whether the aim also sets how many lines are sung again (tried: it lowers rhythm scaling; tried again in Window 190 with 929 in: the builds' bars sung again move by 0.03 and a random pool pick fails the rule 7 times in 100, see studies/v33_trials)
AIM_POWER = 1.0       # 920: how hard a song's repeats, steps and leaps lean toward its kept song's shares
CENTRE_FOLLOWS = 0.5                                   # 927: a part's centre rises half as far as its top
PLANT_PEAK = os.environ.get("LUTHIER_PLANT_PEAK", "1") != "0"      # 950 (the environment switch is for studies/sounder_pools only)
PEAK_CLIMB = {"1": True, "2": "fallback", "3": "line"}.get(os.environ.get("LUTHIER_PEAK_CLIMB", "0"), False)      # 749.182: a trial (studies/the_draw): the line that carries the planted peak holds no leap past an octave
PEAK_TRIES = int(os.environ.get("LUTHIER_PEAK_TRIES", "60"))      # 950's draws for the carrying line; 240 in the trial of 749.191 (studies/the_peak_line)
OCTAVE_TAIL = os.environ.get("LUTHIER_OCTAVE_TAIL", "0") == "1"      # 749.191: a trial (studies/the_peak_line)
PITCH_CEILING = True   # 956
OCTAVE_GATE = {"ban": True, "one": "one", "off": False}[os.environ.get("LUTHIER_OCTAVE", "ban")]     # 959 (749.160); "one" is the trial form of 749.176, not built (the environment switches here and below are for studies/v48_trials)
TITLE_STRESS = {"off": False, "inside": "inside"}[os.environ.get("LUTHIER_TITLE", "off")]   # 961 (749.162): a setting, not a default: it passed over 7 in 10 of the living builds of songs 54 and 49, whose title lines end on a weak syllable
VARY_RETURNS = True    # 962 (749.167)
VERSE_CLOSER = {"off": None, "0": None}.get(os.environ.get("LUTHIER_VERSE_CLOSER", "off"), os.environ.get("LUTHIER_VERSE_CLOSER", "off"))      # 958 (749.142), off by default from v46 (749.153): song 49, the hold-out, lost words' fit under it. A lyric may ask for it ("verse_closer": true, or a form's name); the environment switch is for studies
VERSE_SHARES = os.path.join(HERE, "..", "..", "studies", "lever_range", "result.json")      # the trial form "shares" (749.153) reads the kept shares from the study; a kept table is made only if the form is built
CHOOSE_RANGE = True    # 951, 954: the choice among the builds past every gate takes no tune narrower than a floor under the range the words ask
RANGE_OVER = 1.0   # 927: semitones the tops are set over the kept song's range
RUN_TOP = 10          # 926: the longest run of one pitch a song may take from its kept song (the kept 90th percentile)
MOVE_FIT = (40, 6, 400)   # 930, 934 (749.108, 749.115): builds past the gates a round asks for, rounds at most, and tries a round at most, to fit the step, leap and repeat weights to the aimed song (None: the fixed weights below)
BORROW_FIT = None        # 943 (749.109): (40, 200) = builds past the gates a setting asks for, and tries at most, to fit the borrows to the aimed song. OFF: it passed its trial outside the engine and held on the hold-out, and in the engine the pools fell under the soundness standard (studies/verse_match/RESULT.md). None: FIGURE_BORROW for every song, as before
SHAPE_FROM = "the song"   # 944 (Window 196): "the song" = its shape from its own words and the engine's theory; "a kept song" = one kept song drawn and its numbers taken (920 to 943), kept for the record
BORROW_FIT_SONG = None   # 944: (40, 200) fits the two borrows to what the song's own words ask for bars sung again. OFF: tried in Window 196, the pools fell under the standard, as in Window 195 (studies/shape_from_the_song)
BORROW_GRID = ((0.0, 0.0), (0.8, 0.0), (1.0, 0.0), (0.5, 0.5), (0.0, 1.0))   # (figure borrow, rhythm borrow)
BORROW_WORDS = 0.03      # 943: how far under the old setting's words' fit a setting may stand and still be chosen
FIT_EDGE = 0.03          # 941 (749.121): how far past the kept 10th to 90th a round's fresh lines may read and still count as at the band's edge
MOVE_FIT_SEED = __import__("os").environ.get("LUTHIER_FIT_SEED", "")   # a different trial seed, for the stability check only (749.115)
MOVE_STEP = 1.2; MOVE_LEAP = 1.6; REG_SPREAD = 50.0      # 927 (749.100)
FIGURE_MEMORY = 8.0   # 923: how much a note that completes a four-interval figure already sung is favoured (1 = not at all; tried 1, 4, 8, 16: the builds' share of figures sung again rises to 8 and no further)
FIGURE_BORROW = 0.8   # 919 (749.97): raised from 0.6 so the builds' bars on a figure already sung meet the kept median (0.474)
WORD_STEP = 1.5; WORD_AGAIN = 8.0     # 882: each note split or dropped when a line is sung again costs this much of the fit's score, so a line of the same count keeps its tune.
#  879, 880: fitted so the builds' shares (a function word on the bar's first beat, the step up from a light word to a stressed one) and their fits meet the kept
ONE_BAR = 0.09   # 911 (749.89): recounted on the mended parse (a silence of one bar to two, per eight bars: 0.386 old, 0.35 with ties read)
_ONE_BAR_BEFORE_911 = 0.1    # 876: a fresh two-bar line sung in one bar with the next bar silent, one time in ten (kept: a one-bar silence 0.2 times in eight bars)
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
    closer_ = {}; closer_form_ = None
    sung = []; slots = {}; how = {}; first = {}; texts = {}; n_in, n_out = BD.edges(L["bpm"], beats); form = [("Intro", "intro", n_in)]; flags = []      # 825
    for name, lines in L["sections"]:
        sy = [[(w, bool(st)) for w, v, st, fn in syllables(ln, flags)] for ln in lines]; k = kind_of(name)
        pr = SL.propose([len(x) for x in sy], L["bpm"], beats); sl = [max(1, min(4, r["whole bars proposed"] if not (r["whole bars proposed"] == 1 and r["kept share in one bar or less"] < 0.5) else 2)) for r in pr]      # 869 (749.63): one bar only where half of kept lines that long fit in one
        vc_ = VERSE_CLOSER or ("apart" if L.get("verse_closer") is True else L.get("verse_closer") or None)
        if vc_ and k == "verse" and metre == "4/4" and L.get("verse_closer", True) is not False:      # 4/4 only: the kept figures are 4/4's                                                          # 958 (749.142; studies/busy_sections): the verse sung closer. Verse lines of 6 to 8 syllables that would take two bars take one: the shortest first, none side by side, an even count, as many as bring the verse nearest the kept middle of notes a bar (4.59). Kept verses run 4.6 notes a bar and 1.15 times their choruses; Luthier gave every such line two bars
            cand_ = sorted([i for i, r in enumerate(pr) if 6 <= r["syllables"] <= 8 and sl[i] == 2], key=lambda i: (pr[i]["syllables"], i)); n1_ = len(cand_) if vc_ == "all" else len(cand_) // 2 if vc_ == "half" else int(round(pr[cand_[0]]["kept share in one bar or less"] * len(cand_))) if cand_ else 0
            if vc_ == "aim": n1_ = min(range(0, len(cand_) + 1, 2), key=lambda m_: abs(sum(len(x) for x in sy) / max(1, sum(sl) - m_) - 4.59))
            if vc_ == "apart":
                def take_(m_):
                    got_ = []
                    for i in cand_:
                        if len(got_) < m_ and not any(abs(i - j) == 1 for j in got_) and not (i > 0 and sl[i - 1] == 1) and not (i + 1 < len(sl) and sl[i + 1] == 1): got_.append(i)
                    return got_[:len(got_) - len(got_) % 2]
                best_ = min((take_(m_) for m_ in range(0, len(cand_) + 1, 2)), key=lambda g_: abs(sum(len(x) for x in sy) / max(1, sum(sl) - len(g_)) - 4.59)); cand_ = best_; n1_ = len(best_)
            if vc_ == "shares":                                                              # the trial of 749.153: each candidate line carries s, the kept share of verse lines that long taking one bar at the song's tempo; a verse takes round(sum of s) lines, the highest s first (shorter, then earlier, on a tie), none beside one already taken
                bs_ = 240.0 / L["bpm"]; band_ = "fast (bar under 1.8 s)" if bs_ < 1.8 else "slow (bar 2.6 s or more)" if bs_ >= 2.6 else "middle"; KS_ = json.load(open(VERSE_SHARES))["verse"]
                s_ = {i: KS_[str(pr[i]["syllables"])]["by_tempo"][band_]["one_bar_or_less"] for i in cand_}; want_ = int(round(sum(s_.values()))); got_ = []
                for i in sorted(cand_, key=lambda i: (-s_[i], pr[i]["syllables"], i)):
                    if len(got_) < want_ and not any(abs(i - j) == 1 for j in got_) and not (i > 0 and sl[i - 1] == 1) and not (i + 1 < len(sl) and sl[i + 1] == 1): got_.append(i)
                cand_ = got_; n1_ = 2 * len(got_)                                              # no even count asked: a verse of an odd count of bars rests a bar at its end, as every section does
                for i in cand_: sl[i] = 1
                closer_[name] = sorted(i + 1 for i in cand_); closer_form_ = vc_
                continue_ = True
            else: continue_ = False
            if not continue_:
                for i in cand_[:n1_ - n1_ % 2]: sl[i] = 1
                closer_[name] = sorted(i + 1 for i in cand_[:n1_ - n1_ % 2]); closer_form_ = vc_
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
    form.append(("Outro", "outro", n_out)); br = BD.break_after(form); bar_s = 60.0 / L["bpm"] * beats
    if br is not None and (sum(b for _, _, b in form) + 8) * bar_s <= BD.EDG["length"][2]: form.insert(br + 1, ("Break", "solo", 8))        # 830; 842: only while the song stays inside the kept songs' middle half of lengths
    elif br is not None: flags.append("no break: with one the song would run past the kept 75th of lengths")
    if sum(b for _, _, b in form) * bar_s > BD.EDG["length"][2]:                               # 888: a song past the kept 75th of lengths takes the kept lower quartiles of bars in and out
        n_in2, n_out2 = BD.edges(L["bpm"], beats, q=0); form[0] = ("Intro", "intro", min(n_in, n_in2)); form[-1] = ("Outro", "outro", min(n_out, n_out2)); flags.append(f"888: the song runs long: {form[0][2]} bars in and {form[-1][2]} out (the kept lower quartiles)")
    # 877: where the voice stays out. Kept songs hold a median of two silences of two bars or more (quartiles 1, 2, 3), three in five of them between sections,
    # 2 bars 29 times in a hundred, 4 bars 18, 8 bars or more 36. The break is one; the others are turns of two or four bars after a chorus that is not the last.
    rs_ = _r_.Random(f"silences {L.get('seed', 1)} {L['title']}"); want = rs_.choices([1, 2, 3], [0.25, 0.5, 0.25])[0] - (1 if any(n == "Break" for n, _, _ in form) else 0)
    chs = [i for i, (n, k, b) in enumerate(form) if k == "chorus" and any(k2 in ("verse", "chorus", "bridge") for _, k2, _ in form[i + 1:]) and form[i + 1][0] != "Break"]
    for j, i in enumerate(sorted(rs_.sample(chs, min(max(0, want), len(chs))), reverse=True)):
        tb = rs_.choices([2, 4], [0.62, 0.38])[0]                                              # 918 (749.95; amends 916): each turn at the kept split whatever the length, and one of four bars at the least in a song that has a turn:
        if j == 0 and tb == 2 and not any(n_.startswith("Turn") and b_ == 4 for n_, _, b_ in form): tb4_ = True          # a two-bar silence seldom empties a four-bar stretch, and those are what a kept song's rhythm scaling follows
        else: tb4_ = False
        form.insert(i + 1, (f"Turn {len(chs) - j}", "solo", tb))
    turns_ = [q for q, (n_, k_, b_) in enumerate(form) if n_.startswith("Turn")]
    if turns_ and not any(form[q][2] == 4 for q in turns_): form[turns_[0]] = (form[turns_[0]][0], "solo", 4)
    if sum(b for _, _, b in form) * bar_s > BD.EDG["length"][2] and not any(f.startswith("888: the song runs long") for f in flags):      # 916: read again once the turns are in, so the bars in and out give way before a turn does
        n_in2, n_out2 = BD.edges(L["bpm"], beats, q=0); form[0] = ("Intro", "intro", min(form[0][2], n_in2)); form[-1] = ("Outro", "outro", min(form[-1][2], n_out2)); flags.append(f"888: the song runs long: {form[0][2]} bars in and {form[-1][2]} out (the kept lower quartiles)")
    secs_ = round(sum(b for _, _, b in form) * bar_s)                                          # 894 (749.69): one length, counted once, after the form is final
    if secs_ > BD.EDG["length"][2]: flags.append(f"the song runs {secs_} seconds, past the kept 75th ({BD.EDG['length'][2]}): the lyric is long for its tempo; at this tempo it would need about {int(round((secs_ - BD.EDG['length'][2]) / (2 * bar_s)))} fewer two-bar lines, or about {int(math.ceil(L['bpm'] * secs_ / BD.EDG['length'][2]))} beats a minute")
    RP = json.load(open(os.path.join(HERE, "..", "..", "tables", "register_plan.json"))); R_ = RP["registers"]; import random as _r; V = C.VOICES[L.get("voice", "tenor")]
    room_ = [x for x in RP["lifts"] if -3 <= x <= V[1] - V[0] - 12]; lift = int(round(_r.Random(f"plan {L.get('seed', 1)} {L['title']}").choice(room_ or RP["lifts"])))      # 907 (749.84): the lift drawn from the kept lifts the voice has room for, not drawn from all and clamped
    AIM_ = None
    if metre == "4/4" and L.get("aim", True):                                                  # 925 (749.98): the kept song the aim is drawn from (920) is drawn first, and the lift is that song's own where it has a verse and a chorus
        KR0_ = json.load(open(os.path.join(HERE, "..", "..", "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]; AIM_ = _r.Random(f"aim {L.get('seed', 1)} {L['title']}").randrange(len(KR0_["rows"]))
        if SHAPE_FROM == "the song":                                                           # 944: no kept song is drawn. The chorus's lift over the verse is the kept songs' middle lift: the theory's "the top is the chorus's", which holds in three kept songs in four (studies/shape_from_the_song)
            import statistics as _st0; AIM_ = None; lift = int(round(_st0.median([x for x in KR0_["lifts"] if x is not None])))
        elif KR0_.get("lifts") and KR0_["lifts"][AIM_] is not None: lift = int(round(KR0_["lifts"][AIM_]))
    lift = max(-3, min(lift, V[1] - V[0] - 12)); T0 = 60                                           # 838: the registers on the tonic, from the kept quartiles; the lift clamped to the voice
    vf, vc, vt = R_["verse"]["floor"][1], R_["verse"]["centre"][1], R_["verse"]["top"][1]                                               # the kept medians: floor on the tonic, centre a third above, top a sixth above
    reg = {"Verse": [T0 + vc, T0 + vf, T0 + vt], "Chorus": [T0 + vc + lift, T0 + max(-3, min(lift, max(0, lift - 1))), T0 + vt + lift], "Bridge": [T0 + R_["bridge"]["centre"][1], T0 + R_["bridge"]["floor"][1], T0 + R_["bridge"]["top"][1]]}
    vary = [name for name, lines in L["sections"] if lines and all(how.get(f"{name}:{i}", ["fresh"])[0] == "copy" for i in range(len(lines)))]      # 839: only a section that would return note for note
    reg = {k: [int(round(x)) for x in v] for k, v in reg.items()}; tw = [w for w, _, _, _ in LS.syllables(L["title"])] if L.get("title") else []
    hooks = [f"{name}:{i}" for name, lines in L["sections"] for i, ln in enumerate(lines) if tw and " ".join(tw) in " ".join(w for w, _, _, _ in LS.syllables(ln))]     # 840: the lines that sing the title
    spec = dict(title=L["title"], metre=metre, seed=L.get("seed", 1), scale=[(x + 0) % 12 for x in SCALES[L.get("mode", "major")]], sung=sung, slots=slots, how=how,
                registers=reg, plan=dict(lift=lift, note="838: the chorus's centre over the verse's, drawn from the kept songs' own lifts; 925: the lift of the kept song the aim is drawn from, where it has one"), hooks=hooks, vary_returns=vary, gates=[dict(type="plan lift", lift=lift, within=2), dict(type="hook beat", at_least=0.5)], clash_rule=True, borrow=dict(rhythm=0.0, figure=FIGURE_BORROW), early_entries=EARLY)      # 818: kept songs sing six bars in ten on a rhythm already sung
    if closer_: spec["verse_closer"] = dict(form=closer_form_, lines_given_one_bar=closer_, note="958: verse lines of 6 to 8 syllables given one bar; off unless the lyric asks (749.153)")
    if metre == "4/4": spec["table"] = "4-4_pop_sung"
    if metre == "4/4" and L.get("aim", True):                                                  # 920 (749.94): one kept song drawn from the title's seed, as 838 draws the lift; its readings are this song's targets
        KR_ = json.load(open(os.path.join(HERE, "..", "..", "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]; AT_ = json.load(open(os.path.join(HERE, "..", "..", "tables", "metre_atlas", "4-4_pop_sung.json")))["readings_quartiles"]
        ri_ = _r.Random(f"aim {L.get('seed', 1)} {L['title']}").randrange(len(KR_["rows"])); tr_ = dict(zip(KR_["names"], KR_["rows"][ri_])); shape_ = None
        if SHAPE_FROM == "the song":                                                           # 944 (Window 196): the song's shape from the song itself. No one kept song is its model.
            import numpy as _np6, words_to_shape as _WS                                         # How much it repeats and how wide it ranges: from its own words, by the link found in the kept songs as a body (studies/words_to_shape).
            col_ = lambda c_: [r_[KR_["names"].index(c_)] for r_ in KR_["rows"]]; q_ = lambda c_, p_: float(_np6.percentile(col_(c_), p_))      # How it moves: the middle of what every kept melody does (the paper's invariants, Module 0.4), unless the writer asks otherwise.
            tr_ = {c_: q_(c_, 50) for c_ in KR_["names"]}; own_, feat_ = _WS.from_sung(sung, minor=L.get("mode", "major") == "minor"); tr_.update(own_); mv_ = L.get("movement")
            fam_ = FAMILY.get(L.get("genre", "pop"), "other"); rf_ = json.load(open(_WS.TABLE)).get("repeated_notes_by_family") or {}
            if fam_ not in rf_: raise SystemExit(f"952 (749.131): tables/kept_words_to_shape.json has no middle of repeated notes for the genre family {fam_!r}; run lib/luthier/make_kept_words_to_shape.py")      # 947 (749.129): of the three movements only repeated notes differ by genre family in kept songs; that one is the family's middle
            tr_["repeated notes"] = float(rf_[fam_])
            if mv_ == "smooth": tr_["moves by step"] = q_("moves by step", 75); tr_["moves by leap"] = q_("moves by leap", 25)
            elif mv_ == "leaping": tr_["moves by leap"] = q_("moves by leap", 75); tr_["moves by step"] = q_("moves by step", 25)
            elif mv_ == "chant": tr_["repeated notes"] = q_("repeated notes", 75); tr_["longest run of one pitch"] = q_("longest run of one pitch", 75)
            elif mv_ not in (None, "the engine's"): raise SystemExit(f"movement: {mv_!r} is not one of smooth, leaping, chant")
            ri_ = None; shape_ = dict(shape_from="the song", from_its_words={c_: round(v_, 3) for c_, v_ in own_.items()}, words=feat_, movement=mv_ or "the engine's: the kept middle; repeated notes at the genre family's middle", family=fam_, note="944: repetition and range from the song's own words; movement at the kept middle unless the writer chooses smooth, leaping or chant")
        tg_ = {k_: tr_[k_] for k_ in ("repeated notes", "moves by step", "moves by leap", "range", "bars on a figure already sung", "bars on a rhythm already sung", "distinct rhythms over bars", "longest run of one pitch")}
        spec["target"] = dict(kept_song_row=ri_, kept_song=(KR_.get("song_names") or [None] * (ri_ + 1))[ri_] if ri_ is not None else None, readings=tg_, power=AIM_POWER, run=int(max(3, min(RUN_TOP, round(tg_["longest run of one pitch"])))), moves=dict(step=MOVE_STEP, leap=MOVE_LEAP, spread=REG_SPREAD))      # 926 (749.99): a pitch may repeat as long as the kept song's longest run; 927 (749.100): the moves' own lean taken out
        if shape_:
            import statistics as _st1; spec["target"].update(shape_); spec["target"]["melisma_share"] = round(_st1.median([x for x in KR_["melismas"] if x is not None]), 2)      # the kept middle share of syllables on two notes
        elif KR_.get("melismas") and KR_["melismas"][ri_] is not None:                           # 932 (749.110): the song's melismas, syllables in a hundred, are the aimed song's own, inside the kept 10th to 90th
            import numpy as _np4; m10_, m90_ = (float(x) for x in _np4.percentile([x for x in KR_["melismas"] if x is not None], (10, 90))); spec["target"]["melisma_share"] = round(max(m10_, min(m90_, float(KR_["melismas"][ri_]))), 2); spec["target"]["kept_song_melisma_share"] = KR_["melismas"][ri_]
        if AIM_REPEATS: spec["borrow"]["figure"] = round(max(0.3, min(1.0, FIGURE_BORROW * (tg_["bars on a figure already sung"] + 0.05) / (AT_["bars on a figure already sung"][1] + 0.05))), 3)      # more or less of its lines sung again, as the kept song repeats more or less
        if AIM_REPEATS: spec["borrow"]["rhythm"] = round(max(0.0, min(0.3, 1.0 - spec["borrow"]["figure"], tg_["bars on a rhythm already sung"] - AT_["bars on a rhythm already sung"][1])), 3)      # and, where the kept song repeats its rhythms more than most, some lines take an earlier line's rhythm with new notes
        rg_ = spec["registers"]; span_ = max(rg_[k_][2] for k_ in ("Verse", "Chorus")) - min(rg_[k_][1] for k_ in ("Verse", "Chorus")); want_ = min(float(tg_["range"]), V[1] - V[0]) + RANGE_OVER      # 927 (749.100; amends 920): the tops set so the song's span, floor to top, is the kept song's range (and a little over, since a line seldom reaches its top), inside the voice
        dr_ = int(round(max(-5, min(9, want_ - span_))))
        for k_ in ("Verse", "Chorus", "Bridge"): rg_[k_][2] = min(rg_[k_][2] + dr_, rg_["Verse"][1] + (V[1] - V[0])) if rg_[k_][2] + dr_ > rg_[k_][0] + 1 else rg_[k_][0] + 2
        for k_ in ("Verse", "Chorus", "Bridge"): rg_[k_][0] = max(rg_[k_][1] + 2, min(rg_[k_][2] - 2, rg_[k_][0] + int(round(dr_ * CENTRE_FOLLOWS))))      # and each part's centre follows its top, so the line can reach it
        if PLANT_PEAK and spec["target"].get("from_its_words"): spec["target"]["peak"] = dict(range=float(spec["target"]["from_its_words"]["range"]), tries=PEAK_TRIES, **({"climb": PEAK_CLIMB} if PEAK_CLIMB else {})); spec["target"]["choose_range"] = (lambda a_, q_: dict(asked=a_, floor=round(a_ + q_, 2), note="954: no chosen tune narrower than the asking plus the kept 25th of range less the asking (held out by artist)"))(float(spec["target"]["from_its_words"]["range"]), float(json.load(open(_WS.TABLE))["range_less_the_asking_held_out"]["p10_25_50_75_90"][1])) if CHOOSE_RANGE else None      # 950: the peak planted as a note in the first fresh chorus line that reaches it
        spec["target"]["moves"]["spread"] = round(REG_SPREAD * max(0.6, min(2.5, (float(tg_["range"]) / AT_["range"][1]) ** 2)), 1)      # and a line keeps to its register as closely as a song of that range would
    if L.get("mode", "major") == "major":                                                    # 846: degrees by genre family and section, from the kept major songs (studies/genre)
        GR = json.load(open(os.path.join(HERE, "..", "..", "studies", "genre", "genre_results.json"))); fam = FAMILY.get(L.get("genre", "pop"), "other"); DS = GR["degree_share"]
        rs = _r.Random(f"blue {L.get('seed', 1)} {L['title']}"); bluesong = rs.random() < GR["families"][fam if fam in GR["families"] else "all"]["b3_songs"] and L.get("blue_notes", True) is not False      # 963 (749.168): a lyric may turn the blue-note draw off ("blue_notes": false)
        def prof(key):
            d_ = DS.get(key) or DS[f"all/{fam}"]; out = {k: (v if k not in ("3", "10") else (v / GR["families"][fam]["b3_songs"] if bluesong else 0.0)) for k, v in d_.items() if k not in ("1", "6", "8")}; m_ = max(out.values()); return {k: round((v / m_) ** DEGREE_POWER, 4) for k, v in out.items()}
        spec["degrees"] = dict(tonic=0, blue=[3, 10] if bluesong else [], family=fam, blue_song=bluesong, weights={"Verse": prof(f"secfam/verse|{fam}"), "Chorus": prof(f"secfam/chorus|{fam}"), "all": prof(f"all/{fam}")})
    if L["metre"] == "4/4":                                                                   # 879-882 (way 3): the kept songs' use of a word's weight, where a kept table of it stands (4/4)
        spec["stressed on the beat, at least"] = json.load(open(os.path.join(HERE, "..", "..", "tables", "kept_line_ends.json")))["stressed_syllables_on_a_beat_by_song_5_10_25_50_75"][1]      # 911: 731's floor is the kept 10th by song, tie starts read (0.35; it was 0.4 by hand)
        spec["all_windows"] = True                                                            # 912: every kept two-bar rhythm may be drawn, not the sixty commonest
        import page_gate as PG_; spec["page_gate"] = dict(floor=PG_.table()["floor"]["plainness"], memory=FIGURE_MEMORY)
        if PITCH_CEILING: spec["pitch_ceiling"] = {k_: v_["ceiling"] for k_, v_ in json.load(open(os.path.join(HERE, "..", "..", "tables", "kept_commonest_pitch.json")))["parts"].items()}      # 956 (749.134): a build whose verses or choruses put more of their notes on one pitch than nine kept songs in ten is passed over      # 922, 923: the page gate as a floor (tables/kept_page_gate.json), 4/4
        spec["no_leap_past_an_octave"] = OCTAVE_GATE; spec["title_stress"] = L.get("title_stress", TITLE_STRESS) if L.get("title_stress", TITLE_STRESS) == "inside" else bool(L.get("title_stress", TITLE_STRESS))      # 959 on in 4/4; 961 where the lyric asks ("title_stress": true)
        if OCTAVE_TAIL: spec["octave_tail"] = json.load(open(os.path.join(HERE, "..", "..", "tables", "kept_octave_tail.json")))      # 749.191: a trial form, off
        spec["line_ends"] = True                                                              # 899: the kept line ends (tables/kept_line_ends.json), 4/4
        import word_weight as WW_; spec["word_weight"] = dict(place=WORD_PLACE, step=WORD_STEP, again_cost=WORD_AGAIN, length=WORD_LENGTH, last_note=True, short_stress=WORD_SHORT, gate=WW_.table()["fit_percentiles_10_25_50_75_90"][0])
    else: flags.append("the words' weights are not read: no kept table of them outside 4/4")
    spec["word_pitch"] = WORD_PITCH; spec["judge"] = 7; spec["one_bar_share"] = ONE_BAR; spec["kept_rests"] = [[12, 15, 18, 24, 36, 48], [0.2, 0.15, 0.1, 0.25, 0.15, 0.15]]      # 870: the kept rests after a line (10th percentile a quarter, 25th 15 twelfths, median a half, 75th a whole)
    flags[:] = list(dict.fromkeys(flags))                                                      # 902 (749.81): each flag once
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
    spec, form, flags = plan(L); mode = L.get("mode", "major"); W = C.Writer(mode, chromatic=L.get("chromatic", 1.0)); W.loop_less = {"gentle": "gentle", "median": True}.get(os.environ.get("LUTHIER_LOOP", "off"), L.get("chords") == "loop_less"); drafts = []      # 749.184: the switch is off unless it names a form.      # 960 (749.159): a setting, off unless the lyric asks
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
    E = M.Engine(spec); E.as_sung = lambda ns_: melisma_notes(ns_, L, set(spec["scale"]), key="p", how=spec.get("how"), cap=(spec.get("target") or {}).get("run"), share=(spec.get("target") or {}).get("melisma_share"))[0]      # 914 (749.91): the words' gate reads each build with its melismas placed
    BORROW_FIT_ = BORROW_FIT or (BORROW_FIT_SONG if (spec.get("target") or {}).get("shape_from") == "the song" else None)
    if spec.get("target") and BORROW_FIT_ and spec.get("borrow") and spec.get("word_weight"):    # 943 (749.109): the two borrows fitted to the aimed song. A song aimed at a kept song that sings its bars again much borrows more; one aimed low borrows less.
        import random as _r5, numpy as _np5, collections as _c5, word_weight as _W5              # Tried outside the engine first, its rule written first, and it held on the hold-out (studies/verse_match).
        tg5_ = spec["target"]; F5_, R5_ = "bars on a figure already sung", "bars on a rhythm already sung"; aim5_ = {c_: float(tg5_["readings"][c_]) for c_ in (F5_, R5_)}; wd5_ = {c_: max(1e-9, E.Q[c_][2] - E.Q[c_][0]) for c_ in (F5_, R5_)}; tr5_ = []
        for f5_, r5_ in BORROW_GRID:
            spec["borrow"] = dict(rhythm=r5_, figure=f5_); rng5_ = _r5.Random(f"943 {L.get('seed', 1)} {L['title']}"); rows5_ = []; tries5_ = 0
            while len(rows5_) < BORROW_FIT_[0] and tries5_ < BORROW_FIT_[1]:
                c5_, e5_ = E.build(rng5_); tries5_ += 1
                if e5_ or E.gates(c5_): continue
                s5_ = sorted(E.as_sung(c5_["notes"]), key=lambda n_: n_["on"]); x5_ = E.readings(s5_); rows5_.append((x5_[F5_], x5_[R5_], _W5.fit([n_ for n_ in s5_ if n_.get("melisma") != "second"], E.BAR, E.BEAT, parts=True)["all"]))
            if len(rows5_) < 8: tr5_.append(dict(figure=f5_, rhythm=r5_, tries=tries5_, builds=len(rows5_))); continue
            m5_ = [float(_np5.median([x[k_] for x in rows5_])) for k_ in range(3)]
            tr5_.append(dict(figure=f5_, rhythm=r5_, tries=tries5_, builds=len(rows5_), bars_on_a_figure_already_sung=round(m5_[0], 3), bars_on_a_rhythm_already_sung=round(m5_[1], 3), words_fit=round(m5_[2], 3), gap=round(abs(m5_[0] - aim5_[F5_]) / wd5_[F5_] + abs(m5_[1] - aim5_[R5_]) / wd5_[R5_], 3)))
        base5_ = next((x for x in tr5_ if (x["figure"], x["rhythm"]) == (FIGURE_BORROW, 0.0) and "gap" in x), None)
        ok5_ = [x for x in tr5_ if "gap" in x and (base5_ is None or x["words_fit"] >= base5_["words_fit"] - BORROW_WORDS)]      # the fit may not buy bars with the words
        pick5_ = min(ok5_, key=lambda x: x["gap"]) if ok5_ else dict(figure=FIGURE_BORROW, rhythm=0.0)
        spec["borrow"] = dict(rhythm=pick5_["rhythm"], figure=pick5_["figure"]); E.stats = _c5.Counter()
        tg5_["borrow_fit"] = dict(aim=aim5_, settings=tr5_, kept=dict(figure=pick5_["figure"], rhythm=pick5_["rhythm"]), note="943: five settings of the two borrows on short trial runs; kept, the one nearest the aimed song on bars on a figure already sung and on a rhythm already sung together (each gap in kept middle-half widths), among those whose words' fit is no more than 0.03 under the old setting's")
    if spec.get("target") and MOVE_FIT:                                                       # 930 (749.108): the step and leap weights fitted to this song, as 885 fitted the words' weights: short trial runs, each weight scaled until the builds' median meets the aimed song's
        import random as _r3, numpy as _np3, collections as _c3                              # 936 (749.113): and the weight on a repeated note with them
        tg3_ = spec["target"]; mv3_ = tg3_["moves"]; mv3_.setdefault("repeat", 1.0); KR3_ = json.load(open(os.path.join(HERE, "..", "..", "tables", "metre_atlas", "kept_readings.json")))["4-4_pop_sung"]
        W3_ = (("step", "moves by step", 3.0, 0.02, (0.3, 6.0)), ("leap", "moves by leap", 1.5, 0.01, (0.3, 5.0)), ("repeat", "repeated notes", 2.0, 0.02, (0.2, 5.0)))      # weight, the check it moves, how hard a round scales it, a floor under the ratio, its limits
        aim3_ = {w_: float(tg3_["readings"][c_]) for w_, c_, *_ in W3_}; tol3_ = {w_: (E.Q[c_][2] - E.Q[c_][0]) / 4.0 for w_, c_, *_ in W3_}
        K10_ = {c_: tuple(float(x) for x in _np3.percentile([r_[KR3_["names"].index(c_)] for r_ in KR3_["rows"]], (10, 90))) for _, c_, *_ in W3_}
        fresh3_ = {}; orig3_ = E.pitches
        def rec3_(rng, ons, U, sec, i, prev, avoid=None, end_off=None):                        # 932 (749.110): which lines were drawn fresh, where the weights act
            ps_ = orig3_(rng, ons, U, sec, i, prev, avoid=avoid, end_off=end_off); fresh3_[(sec, i)] = ps_; return ps_
        E.pitches = rec3_; total3_ = 0; trail3_ = []; in3w_ = {}; out3w_ = {}; inside3_ = lambda r_: all(K10_[c_][0] - FIT_EDGE <= r_["fresh_lines"][w_] <= K10_[c_][1] + FIT_EDGE for w_, c_, *_ in W3_)      # 941: a round counts as inside when its fresh lines are within FIT_EDGE of the band (forty builds read a share to about that), so a weight that has closed on the edge is not thrown away for standing a hair past it
        for round3_ in range(MOVE_FIT[1]):
            rng3_ = _r3.Random(f"930 {L.get('seed', 1)} {L['title']}{MOVE_FIT_SEED}"); rows3_ = []; tries3_ = 0
            while len(rows3_) < MOVE_FIT[0] and tries3_ < MOVE_FIT[2]:                         # 934 (749.115): a round draws until enough builds pass the gates to fit on, with a cap on the tries
                fresh3_.clear(); c3_, e3_ = E.build(rng3_); total3_ += 1; tries3_ += 1
                if e3_ or E.gates(c3_): continue
                by3_ = {}
                for n_ in c3_["notes"]: by3_.setdefault((n_["sec"], n_["line"]), []).append(n_["p"])
                fiv3_ = [abs(b_ - a_) for k_, v_ in by3_.items() if fresh3_.get(k_) == v_ for a_, b_ in zip(v_, v_[1:])]; sh3_ = lambda f_: float(_np3.mean([f_(x) for x in fiv3_])) if fiv3_ else float("nan")
                r3_ = E.readings(sorted(E.as_sung(c3_["notes"]), key=lambda n_: n_["on"])); rows3_.append(dict(step=r3_["moves by step"], leap=r3_["moves by leap"], repeat=r3_["repeated notes"], range=r3_["range"], f_step=sh3_(lambda x: 1 <= x <= 2), f_leap=sh3_(lambda x: x >= 5), f_repeat=sh3_(lambda x: x == 0)))
            if len(rows3_) < 8: break
            med3_ = {w_: float(_np3.median([x[w_] for x in rows3_])) for w_, *_ in W3_}; fr3_ = {w_: float(_np3.nanmedian([x["f_" + w_] for x in rows3_])) for w_, *_ in W3_}
            trail3_.append(dict(step=mv3_["step"], leap=mv3_["leap"], repeat=mv3_["repeat"], tries=tries3_, builds=len(rows3_), median_step=round(med3_["step"], 3), median_leap=round(med3_["leap"], 3), median_repeat=round(med3_["repeat"], 3), median_range=float(_np3.median([x["range"] for x in rows3_])), fresh_lines={w_: round(fr3_[w_], 3) for w_, *_ in W3_}))
            if all(abs(med3_[w_] - aim3_[w_]) <= tol3_[w_] / 2 for w_, *_ in W3_) and inside3_(trail3_[-1]): break
            if round3_ == MOVE_FIT[1] - 1: break
            for w_, c_, pw_, fl_, (lo_, hi_) in W3_:                                             # 941 (749.121): each weight against its own band, and bisected on its own. A weight whose fresh lines leave the kept 10th to 90th
                klo_, khi_ = K10_[c_]; ok_ = klo_ <= fr3_[w_] <= khi_                               # closes on the band's edge between its last value inside and its nearest value outside; the other weights go on toward their aims
                if ok_: in3w_[w_] = mv3_[w_]
                else: out3w_[w_] = mv3_[w_]
                if w_ in in3w_ and w_ in out3w_ and (not ok_ or (aim3_[w_] - med3_[w_]) * (out3w_[w_] - in3w_[w_]) > 0): mv3_[w_] = round((in3w_[w_] * out3w_[w_]) ** 0.5, 3)      # outside: halfway back; inside and the aim still lies toward the outside value: halfway out
                elif ok_: mv3_[w_] = round(max(lo_, min(hi_, mv3_[w_] * ((aim3_[w_] + fl_) / (med3_[w_] + fl_)) ** pw_)), 3)                                                  # inside: toward the aim (930)
                else: mv3_[w_] = round(max(lo_, min(hi_, mv3_[w_] * (((khi_ if fr3_[w_] > khi_ else klo_) + 0.02) / (fr3_[w_] + 0.02)) ** 2.0)), 3)                              # outside, with no value inside yet: drawn back toward the band (932)
            E.MV = (mv3_["step"], mv3_["leap"], E.MV[2], mv3_["repeat"])                         # (the register spread was tried in the fit too and does not move the range: 62 to 400 in song 55, the builds span 15 to 17 throughout)
        in3_ = [r_ for r_ in trail3_ if inside3_(r_)] or trail3_[:1]
        if in3_:                                                                              # 932: the weights kept are those of the round nearest the aim among the rounds whose fresh lines stayed inside the kept 10th to 90th
            best3_ = min(in3_, key=lambda r_: sum(abs(r_["median_" + w_] - aim3_[w_]) / tol3_[w_] for w_, *_ in W3_))
            for w_, *_ in W3_: mv3_[w_] = best3_[w_]
            E.MV = (mv3_["step"], mv3_["leap"], E.MV[2], mv3_["repeat"]); tg3_["moves_fit_kept_round"] = trail3_.index(best3_) + 1
        E.pitches = orig3_; E.stats = _c3.Counter()                                           # 931 (749.112): the record's stats are the run's thousand builds, not the fit's trial builds
        tg3_["moves_fit"] = dict(trial_builds=total3_, fresh_lines_kept_10th_90th={k_: [round(x, 3) for x in v_] for k_, v_ in K10_.items()}, aim=dict(step=aim3_["step"], leap=aim3_["leap"], repeat=aim3_["repeat"], range=float(tg3_["readings"]["range"])), rounds=trail3_, note="930, 932, 934, 936: each round draws until enough builds pass the gates; the living builds' median step, leap and repeated-note shares, as sung, and the fresh lines' own; the weights scaled toward the aimed song's")
    run = E.run(N, L.get("seed", 1))
    if not run["survivors"]: return dict(error="no build survived", deaths=run["deaths"], flags=flags, spec=spec)
    notes = run["pick"]["notes"]; lo, hi = min(n["p"] for n in notes) - 60, max(n["p"] for n in notes) - 60
    vn_ = sorted(n["p"] - 60 for n in notes if E.KIND.get(n["sec"]) == "Verse"); keys = C.choose_key(lo, hi, L.get("voice", "tenor"), L.get("lead", "guitar"), mode, centre=(vn_[len(vn_) // 2] if vn_ else None))
    if not keys: return dict(error="the melody does not fit the voice in any key", range=[lo, hi], flags=flags)
    key = keys[0]; shift = key["tonic_midi"] - 60; tonic = key["key"]; bt = 24 + key["tonic_midi"] % 12; bt = bt + 12 if bt < 28 else bt
    fb = []; b = 0
    for n, k, nb in form:
        for bar in pl[n]: fb.append((b, list(bar))); b += 1
    bs = bass(fb, bt, E.BAR, E.BEATS, mode)
    rec = dict(title=L["title"], metre=spec["metre"], bpm=L["bpm"], key=key, other_keys=keys[1:3], flags=flags, form=[[n, k, nb] for n, k, nb in form],
               chords={n: [" ".join(C.name(x, tonic) for x in bar) for bar in pl[n]] for n, _, _ in form}, roman={n: [" ".join(bar) for bar in pl[n]] for n, _, _ in form},
               chord_pick=dict(draft=seed, drafts=K, charge=round(c, 3), readings=cr, kept=W.Q),
               judge7=run.get("judge7"), melody=dict(made=run["made"], survivors=run["survivors"], deaths=run["deaths"], pick=run["pick"]["fp"], charge=run["pick"]["charge"], median_charge=run["median_charge"], readings=run["pick"]["readings"],
                           kept=run["kept_quartiles"], uncharged=run["uncharged"], entries=run["entries"], stressed_on_beat=run["pick"]["stressed_on_beat"], stats=run["stats"],
                           notes=[dict(on=n["on"], dur=n["dur"], midi=n["p"] + shift, sec=n["sec"], line=n["line"], text=n["text"], stress=n["stress"]) for n in notes]),
               bass=[dict(on=t, dur=dd, midi=p) for t, dd, p in bs], bar=E.BAR, beats=E.BEATS, spec=spec, chord_tones={x: sorted((t + key["tonic_midi"]) % 12 for t in C.tones(x)) for x in spec["chords"]})
    import hashlib as _h                                                                      # 905 (749.82): the record says which kept tables it read
    rec["kept_tables"] = {t: _h.sha1(open(os.path.join(HERE, "..", "..", "tables", t), "rb").read()).hexdigest()[:10] for t in ([f"metre_atlas/{spec.get('table') or spec['metre'].replace('/', '-') + '_sung'}.json", "metre_atlas/kept_readings.json", "register_plan.json"] + (["kept_word_weight.json", "kept_line_ends.json"] if spec.get("word_weight") else []) + (["kept_page_gate.json"] if spec.get("page_gate") else []) + (["kept_commonest_pitch.json"] if spec.get("pitch_ceiling") else []) + (["kept_words_to_shape.json"] if (spec.get("target") or {}).get("shape_from") == "the song" else []))}
    if VARY_RETURNS: rec["melody"]["varied_returns"] = vary_returns(rec)                      # 962 (749.167), before the melismas and the checks, so everything after reads the tune as it will be sung
    melismas(rec, L, E, key["tonic_midi"]); rec["checks"] = checks(rec, fb, key["tonic_midi"], E)
    if rec.get("judge7") and rec["judge7"].get("pick_words_fit") is not None:                  # 898 (749.72): one fit, on the notes as sung (a melisma's second note is not a syllable)
        import word_weight as WW_; rec["judge7"]["pick_words_fit"] = {k: round(v, 3) for k, v in WW_.fit([n for n in rec["melody"]["notes"] if n.get("melisma") != "second"], E.BAR, E.BEAT, parts=True).items()}
    BD.arrange(rec, genre=L.get("genre", "pop"), lead=L.get("lead", "guitar"), seed=L.get("seed", 1))
    if any(n == "Break" for n, _, _ in form):                                                # 830: the lead instrument plays the first verse's tune over the break
        b0 = sum(nb for n, k, nb in form[:[n for n, _, _ in form].index("Break")]) * E.BAR; vname = next(n for n, k, b in form if k == "verse"); v0 = sum(nb for n, k, nb in form[:[n for n, _, _ in form].index(vname)]) * E.BAR
        rec["parts"]["break"] = [dict(on=n["on"] - v0 + b0, dur=n["dur"], p=[n["midi"] + (12 if L.get("lead", "guitar") == "guitar" else 0)], vel=88) for n in rec["melody"]["notes"] if n["sec"] == vname and n["on"] - v0 < 8 * E.BAR - 6]
    return rec
def vary_returns(rec):
    """962 (749.167): a section that returns note for note varies. In each section of the chosen tune whose every line was copied from an earlier one, each line after
    the first lifts its longest held note (a beat or more; a stressed one before an unstressed) a scale step onto a chord tone, with the leaps on either side kept within
    a fifth and never over the tune's highest note (so the planted peak, 950, stays the peak). 839 lifted such a note by chance, about one copied line in four. Written by
    the songwriting session (proposed_v47.vary_returns); the guard on the highest note is added here. Returns the changes."""
    B = rec["bar"]; BT = B // len(rec["beats"]) if rec.get("beats") else B // 4; tonic = rec["key"]["tonic_midi"]; minor = "m" in str(rec["key"]["key"])[1:]
    scale = {(tonic + d) % 12 for d in ((0, 2, 3, 5, 7, 8, 10) if minor else (0, 2, 4, 5, 7, 9, 11))}; how = rec.get("spec", {}).get("how", {}); start = {}; o = 0
    for n, k, b in rec["form"]: start[n] = o; o += b * B
    notes = rec["melody"]["notes"]; top = max(n["midi"] for n in notes); by = {}; out = []
    for n in notes: by.setdefault((n["sec"], n["line"]), []).append(n)
    for sec, _, _ in rec["form"]:
        lines = sorted(i for s_, i in by if s_ == sec)
        if not lines or not all(how.get(f"{sec}:{i}", ["fresh"])[0] == "copy" for i in lines): continue
        for i in lines[1:]:
            ln = sorted(by[(sec, i)], key=lambda n: n["on"]); held = [n for n in ln if n["dur"] >= BT]
            if not held: continue
            n = max(held, key=lambda n: (n.get("stress", False), n["dur"])); j = ln.index(n); bar = (n["on"] - start[sec]) // B; rn = rec["roman"][sec][min(bar, len(rec["roman"][sec]) - 1)].split()
            c_ = rn[0] if len(rn) == 1 or (n["on"] - start[sec]) % B < B // 2 else rn[1]; tones = {(t_ + tonic) % 12 for t_ in C.tones(c_)}
            for q in range(n["midi"] + 1, n["midi"] + 5):
                if q <= top and q % 12 in scale and q % 12 in tones and (j == 0 or abs(q - ln[j - 1]["midi"]) <= 7) and (j == len(ln) - 1 or abs(ln[j + 1]["midi"] - q) <= 7):
                    out.append(dict(section=sec, line=i + 1, word=n["text"], was=n["midi"], now=q)); n["midi"] = q; break
    return out
ORN = json.load(open(os.path.join(HERE, "..", "..", "studies", "ornament", "ornament_results.json")))["CoCoPops Billboard"]
def melisma_notes(ns, L, scale, key="midi", how=None, cap=None, share=None):
    """914 (749.91): 848's draw as a function of the notes alone, so the words' gate can read each build as sung. Returns the notes, the share drawn, the kept share at line ends."""
    """848: after the pick, some syllables take a second note. The song's share is drawn from the kept songs' (quartiles 3.8, 8.6, 16.2 syllables in a hundred); a melisma
    sits on a word's last syllable (kept 94 in 100), two and a half times as often at a line's end (kept 20 against 8), on a note a quarter long or more, and its
    second note is the scale step below (kept: the first move down 59 in 100; two notes 73 in 100). The readings were taken before; the record keeps both."""
    import random as _r2
    rng = _r2.Random(f"melisma {L.get('seed', 1)} {L['title']}"); share_ = rng.choices([ORN["song_q"][0], ORN["song_median"], ORN["song_q"][1]], [0.25, 0.5, 0.25])[0] / 100.0; share = share_ if share is None else share / 100.0      # 932 (749.110): the aimed song's own share, where the song has an aim
    lo = min(n[key] for n in ns); hi_ = max(n[key] for n in ns); cands = []; w = []; ends = []
    for i, n in enumerate(ns):
        nxt = ns[i + 1] if i + 1 < len(ns) else None; line_end = nxt is None or (nxt["sec"], nxt["line"]) != (n["sec"], n["line"]); word_end = line_end or nxt["text"] != n["text"]
        prev = ns[i - 1] if i else None; mono = (prev is None or prev["text"] != n["text"] or (prev["sec"], prev["line"]) != (n["sec"], n["line"])) and word_end
        if word_end and n["dur"] >= 6 and not (mono and not n["stress"]): cands.append(i); w.append((1.0 if n["dur"] >= 12 else 0.25)); ends.append(line_end)      # 875 (749.59): not on a function word; 886: an eighth will do inside a line, a quarter is likelier
    # 886: of kept melismas 20 in a hundred fall on a phrase's last syllable, where 8 syllables in a hundred are a phrase's last: odds 2.9 to 1 for a last syllable. A song here has
    # more line ends (one syllable in seven), so its share of melismas at line ends is those odds applied to its own count of line ends; before, a quarter-long note was asked and line ends took most.
    n_end = sum(1 for i, n in enumerate(ns) if i + 1 == len(ns) or (ns[i + 1]["sec"], ns[i + 1]["line"]) != (n["sec"], n["line"])); e_ = n_end / len(ns)
    odds = (ORN["at_line_end"] / (100.0 - ORN["at_line_end"])) / (ORN["line_end_base"] / (100.0 - ORN["line_end_base"])); p_end = odds * e_ / (odds * e_ + 1 - e_)
    want = min(len(cands), int(round(share * len(ns)))); want_end = min(int(round(p_end * want)), sum(ends)); chosen = set()
    for grp, k_ in ((True, want_end), (False, want - want_end)):
        idx = [j for j in range(len(cands)) if ends[j] == grp]; ww = [w[j] for j in idx]
        for _ in range(min(k_, len(idx))):
            if sum(ww) <= 0: break
            j = rng.choices(range(len(idx)), ww)[0]; chosen.add(cands[idx[j]]); ww[j] = 0.0
    if how:                                                                                  # 919 (749.97): a line that returns note for note returns with its melismas: a copy takes its source's, syllable for syllable
        idx_ = {}
        for i, n in enumerate(ns): idx_.setdefault((n["sec"], n["line"]), []).append(i)
        for (sec_, li_), ii in idx_.items():
            h_ = how.get(f"{sec_}:{li_}")
            if h_ and h_[0] in ("copy", "again") and (h_[1], int(h_[2])) in idx_ and len(idx_[(h_[1], int(h_[2]))]) == len(ii):      # 942 (749.104, second half): a line sung again to new words takes its source's melismas too, where the two have the same number of syllables
                src_ = idx_[(h_[1], int(h_[2]))]; chosen -= set(ii); chosen |= {ii[k_] for k_, q_ in enumerate(src_) if q_ in chosen and ns[ii[k_]]["dur"] >= 6}
    out = []
    for i, n in enumerate(ns):
        if i not in chosen: out.append(n); continue
        q = n[key] - 1
        while q % 12 not in scale: q -= 1
        if cap:                                                                              # 929 (749.106): where the step below would make a run of one pitch past the song's cap, the melisma takes the step above, or is not placed
            fol_ = lambda q_: next((j_ for j_, m_ in enumerate(ns[i + 1:]) if m_[key] != q_), len(ns) - i - 1)
            if 1 + fol_(q) > cap:
                q = n[key] + 1
                while q % 12 not in scale: q += 1
                if q > hi_ or 1 + fol_(q) > cap: out.append(n); continue
        if q < lo - 2: out.append(n); continue
        d1 = max(3, (n["dur"] // 2) // 3 * 3); out.append(dict(n, dur=d1, melisma="first")); out.append(dict(n, **{"on": n["on"] + d1, "dur": n["dur"] - d1, key: q, "text": "", "stress": False, "melisma": "second"}))
    return out, share, round(p_end, 3)
def melismas(rec, L, E, tonic_midi):
    out, share, p_end = melisma_notes(rec["melody"]["notes"], L, {(x + tonic_midi) % 12 for x in rec["spec"]["scale"]}, how=rec["spec"].get("how"), cap=(rec["spec"].get("target") or {}).get("run"), share=(rec["spec"].get("target") or {}).get("melisma_share")); rec["melody"]["notes"] = out; rec["melody"]["melisma_share_drawn"] = round(share, 4); rec["melody"]["melisma_line_end_share_kept_for_this_song"] = p_end
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
    blue_ = set(rec["spec"].get("degrees", {}).get("blue", ()))
    clash = [n for n in ns if n["dur"] >= E.BEAT and not tone(n) and (n["midi"] - tp) % 12 not in blue_ and n.get("melisma") != "second" and any(((n["midi"] - tp) % 12 - x) % 12 in (1, 11) for x in C.tones(ch(n["on"])))]
    return {"no two sung notes on one onset": all(b > a for a, b in zip(on, on[1:])), "no sung note of no length": all(n["dur"] > 0 for n in ns),
            "the melody inside the voice": [min(n["midi"] for n in ns), max(n["midi"] for n in ns)], "sung notes on a beat that are chord tones, share": round(sum(tone(n) for n in beat_notes) / max(1, len(beat_notes)), 3),
            "sung notes a beat long or more a semitone from a chord tone": len(clash), "bass notes": len(bs), "the bass on the root where a chord begins": all(any(b["on"] == t and (b["midi"] - tp) % 12 == root_pc(rn) for b in bs) for t, rn in chord_at.items()),
            "the bass under the voice everywhere": max(b["midi"] for b in bs) < min(n["midi"] for n in ns), "bass register": [min(b["midi"] for b in bs), max(b["midi"] for b in bs)], **style_checks(rec, E)}
def style_checks(rec, E):
    """843: the readings of stage 6a, each beside its kept figure"""
    import statistics as st_
    ns = rec["melody"]["notes"]; by = {}
    for n in ns: by.setdefault(n["sec"], []).append(n)
    med = lambda k: [x["midi"] for s, v in by.items() if kind_of(s) == k for x in v]                 # every note of the kind, as the gate reads it
    v, c = med("verse"), med("chorus"); rests = []
    for s, v_ in by.items():
        span = v_[-1]["on"] + v_[-1]["dur"] - v_[0]["on"]; sung = sum(min(x["dur"], (v_[i + 1]["on"] - x["on"]) if i + 1 < len(v_) else x["dur"]) for i, x in enumerate(v_)); rests.append(1 - sung / max(1, span))
    hk = set(rec["spec"].get("hooks", [])); hs = [n for n in ns if f"{n['sec']}:{n['line']}" in hk and n["stress"]]; bar_s = 60.0 / rec["bpm"] * len(E.BEATS); secs = sum(b for _, _, b in rec["form"]) * bar_s
    c1 = [x for s, v_ in by.items() if s == next((n for n, k, b in rec["form"] if k == "chorus"), None) for x in v_]; ret = []
    for s, v_ in by.items():
        if kind_of(s) == "chorus" and c1 and v_ is not c1 and v_[0]["sec"] != c1[0]["sec"]:
            a = {}; b = {}; s0 = {}; t_ = 0
            for nm_, k_, nb_ in rec["form"]: s0[nm_] = t_; t_ += nb_
            for x in c1: a.setdefault(x["on"] // E.BAR - s0[x["sec"]], []).append((x["on"] % E.BAR, x["midi"]))
            for x in v_: b.setdefault(x["on"] // E.BAR - s0[x["sec"]], []).append((x["on"] % E.BAR, x["midi"]))
            idx = [i for i in range(min(a), min(max(a), max(b)) + 1) if a.get(i) or b.get(i)]
            if idx: ret.append(sum(a.get(i) == b.get(i) for i in idx) / len(idx))
    syl = [n for n in ns if n.get("melisma") != "second"]; mel = [n for n in ns if n.get("melisma") == "first"]; idx = {id(n): i for i, n in enumerate(ns)}; le = we = 0
    for n in mel:
        i = idx[id(n)]; nxt = ns[i + 2] if i + 2 < len(ns) else None; lend = nxt is None or (nxt["sec"], nxt["line"]) != (n["sec"], n["line"]); le += lend; we += lend or nxt["text"] != n["text"]
    lens = sorted(n["dur"] for n in syl); cut = lens[int(len(lens) * 0.75)]; longs = [n for n in syl if n["dur"] >= cut]; deg = {}
    for n in ns: deg[(n["midi"] - rec["key"]["tonic_midi"]) % 12] = deg.get((n["midi"] - rec["key"]["tonic_midi"]) % 12, 0) + 1
    extra = {"syllables on two notes, in a hundred (kept quartiles 3.8, 8.6, 16.2)": round(100 * len(mel) / max(1, len(syl)), 1), "of those, at a line's end (kept 20 in 100 where 8 syllables in 100 end a phrase; for this song's line ends, %s); on a word's end (kept 94)" % round(100 * rec["melody"].get("melisma_line_end_share_kept_for_this_song", 0.2)): [round(100 * le / max(1, len(mel))), round(100 * we / max(1, len(mel)))],
             "long notes on stressed syllables (kept quartiles 0.43, 0.55, 0.65)": round(sum(n["stress"] for n in longs) / max(1, len(longs)), 3),
             "flat third; flat seventh; leading tone, share of notes (kept, this family)": [round(deg.get(3, 0) / len(ns), 3), round(deg.get(10, 0) / len(ns), 3), round(deg.get(11, 0) / len(ns), 3)], "a song with blue notes": rec["spec"].get("degrees", {}).get("blue_song")}
    if rec["metre"] == "4/4":                                                                 # 899, 903: how the lines end and how the last chorus stands, beside the kept
        import word_weight as WW_; KL = json.load(open(os.path.join(HERE, "..", "..", "tables", "kept_line_ends.json"))); D_ = {0: [], 1: [], 2: []}; G_ = []; R_ = []; i0 = 0; st16 = {"again": [0, 0], "other": [0, 0]}
        for j, a in enumerate(syl):
            if j + 1 == len(syl) or (syl[j + 1]["sec"], syl[j + 1]["line"]) != (a["sec"], a["line"]):
                ln = syl[i0:j + 1]; tr = WW_.tier([(x["text"], x["stress"]) for x in ln])[-1]; i0 = j + 1; k_ = ns.index(a); end = a["on"] + a["dur"] + (ns[k_ + 1]["dur"] if a.get("melisma") == "first" else 0); D_[tr].append(end - a["on"])
                if j + 1 < len(syl): G_.append(syl[j + 1]["on"] - a["on"]); R_.append(syl[j + 1]["on"] - end)
                g_ = "again" if rec["spec"]["how"].get(f"{a['sec']}:{a['line']}", ["fresh"])[0] == "again" else "other"
                for x, y in zip(ln, ln[1:]):
                    if x["stress"]: st16[g_][1] += 1; st16[g_][0] += (y["on"] - x["on"]) <= 3
        sh = lambda v, f: round(sum(f(x) for x in v) / len(v), 2) if v else None; gaps = [(b["on"] - a["on"] - a["dur"]) / 12.0 for a, b in zip(ns, ns[1:])]; big = [g for g in gaps if g >= 1]
        extra["line-final syllables an eighth or less: function word, weak syllable, stressed (kept %s)" % KL["an_eighth_or_less_by_tier"]] = [sh(D_[k], lambda x: x <= 6) for k in range(3)]
        extra["line-final syllables a half note or more: function word, weak syllable, stressed (kept %s)" % KL["held_a_half_or_more_by_tier"]] = [sh(D_[k], lambda x: x >= 24) for k in range(3)]
        extra["lines that run on with under a beat of rest (kept songs %s by quartile)" % KL["run_on_share_by_song_quartiles"]] = sh(R_, lambda x: x < 12)
        extra["silences of a beat or more per 100 beats; their median in beats (kept 7.0, 9.1, 11.1; 1.5 to 3.0)"] = [round(100 * len(big) / ((ns[-1]["on"] - ns[0]["on"]) / 12.0), 1), round(st_.median(big), 2) if big else 0]
        extra["stressed syllables a sixteenth long, of syllables: lines sung again; other lines (kept inside lines 0.12)"] = [f"{st16['again'][0]}/{st16['again'][1]}", f"{st16['other'][0]}/{st16['other'][1]}"]
        ch_ = [n_ for n_, k_, b_ in rec["form"] if k_ == "chorus" and by.get(n_) and not n_.startswith("Tag")]
        if len(ch_) >= 2:                                                                     # 903 (749.75): Module 9.12 read as kept songs would pass it: the last chorus at least as long as the first, and longer or higher at the top
            fb_ = {n_: b_ for n_, k_, b_ in rec["form"]}; tag = sum(b_ for n_, k_, b_ in rec["form"][[n_ for n_, _, _ in rec["form"]].index(ch_[-1]) + 1:] if k_ == "chorus")
            extra["9.12: the last chorus's bars (with a tag after it); the first's; its top note; the first's (kept: longer in 67 of 100, higher at the top in 26)"] = [fb_[ch_[-1]] + tag, fb_[ch_[0]], max(x["midi"] for n_ in [ch_[-1]] + [m_ for m_, k_, _ in rec["form"][[q_ for q_, _, _ in rec["form"]].index(ch_[-1]) + 1:] if k_ == "chorus" and by.get(m_)] for x in by[n_]), max(x["midi"] for x in by[ch_[0]])]
    if rec["metre"] == "4/4":                                                                 # 883: the words' fit of the song as sung, beside the kept
        import word_weight as WW_; K_ = WW_.table(); f_ = WW_.fit([n for n in ns if n.get("melisma") != "second"], E.BAR, E.BEAT, parts=True); kq = K_["fit_percentiles_10_25_50_75_90"]
        extra[f"the words' fit: weightier syllables on more salient notes (kept 10th {kq[0]}, quartiles {kq[1]}, {kq[2]}, {kq[3]})"] = round(f_["all"], 3)
        extra["the fit by length, by place in the bar, by height (kept medians %s, %s, %s)" % (K_["fit_by_length"][2], K_["fit_by_place"][2], K_["fit_by_height"][2])] = [round(f_[k], 3) for k in ("length", "place", "height")]
    if rec["spec"].get("page_gate"):                                                          # 922: the page gate read on the song as recorded, each part beside the share of kept tunes it is plainer than
        import page_gate as PG_; T_ = PG_.table(); on_ = [x["on"] for x in ns]; pr_ = PG_.read([x["midi"] for x in ns], [(b_ - a_) / float(E.BEAT) for a_, b_ in zip(on_, on_[1:])] + [1.0], T_)
        extra["the page gate: plainness (floor: the kept 10th percentile, %s; kept middle %s)" % (round(T_["floor"]["plainness"], 2), T_["percentiles_10_25_50_75_90"]["plainness"][2])] = round(pr_["plainness"], 3)
        extra["the page gate: each part, and the share of kept tunes the song is plainer than"] = {c_: [round(pr_[c_], 3), round(PG_.place(pr_[c_], c_, T_))] for c_ in list(PG_.PLAIN) + ["plainness"]}
        fa_ = PG_.figures_again([x["midi"] for x in ns][:120]) if len(ns) >= 120 else None; extra["four-note figures already sung, first 120 notes (kept quartiles %s)" % T_["percentiles_10_25_50_75_90"]["first_120_figures_again"][1:4]] = round(fa_, 3) if fa_ is not None else None
    return {**extra, "the chorus's median over the verse's, semitones (kept quartiles 0, 1, 4)": round(st_.median(c) - st_.median(v), 1) if v and c else None, "the plan's lift": rec["spec"].get("plan", {}).get("lift"),
            "rest share inside sung sections, median (kept quartiles %s)" % ", ".join(str(x) for x in json.load(open(os.path.join(HERE, "..", "..", "tables", "register_plan.json")))["rest_share"][1:4]): round(st_.median(rests), 3), "the title's stressed syllables on a beat (kept 0.73)": round(sum((n["on"] % E.BAR) in E.BEATS for n in hs) / len(hs), 3) if hs else None,
            "title lines": len(hk), "length in seconds (kept quartiles 165, 206, 243)": round(secs), "later choruses: bars the same as the first chorus's, median (kept 0.57; note for note 15 in 100)": round(st_.median(ret), 2) if ret else None}
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
    if sys.argv[1] == "--check":                                                             # 955 (749.136): every song record's kept-table stamps against the tables at hand:  python3 lib/luthier/song_from_lyric.py --check
        import glob, re, hashlib as _h2; bad = []; n_ = 0; old_ = 0
        for q in sorted(glob.glob(os.path.join(HERE, "..", "..", "songs", "*", "*.song.json"))):
            if re.search(r"\.v\d+\.song\.json$", q): old_ += 1; continue                           # a record kept under an earlier version's name stands as that version made it
            kt = json.load(open(q)).get("kept_tables") or {}; n_ += 1
            for t_, h_ in kt.items():
                f_ = os.path.join(HERE, "..", "..", "tables", t_); now_ = _h2.sha1(open(f_, "rb").read()).hexdigest()[:10] if os.path.exists(f_) else "missing"
                if now_ != h_: bad.append(f"{os.path.relpath(q)}: {t_} was {h_}, is {now_}")
        print(f"{n_} records: every stamped table is the table at hand ({old_} records under an earlier version's name not read)" if not bad else "records made with other tables (rerun them, or say why they stand):\n  " + "\n  ".join(bad)); sys.exit(1 if bad else 0)
    L = json.load(open(sys.argv[1])); N = int(sys.argv[2]) if len(sys.argv) > 2 else 1000; K = int(sys.argv[3]) if len(sys.argv) > 3 else 12
    if N == 0:                                                                               # 894: at intake, how long the lyric will run:  python3 song_from_lyric.py lyric.json 0
        spec, form, flags = plan(L); bs = 60.0 / L["bpm"] * len(json.load(open(os.path.join(M.ATLAS, L.get("metre", "4/4").replace("/", "-") + "_sung.json")))["beats"]); secs = round(sum(b for _, _, b in form) * bs)
        print(f"{L['title']}: {sum(len(ls) for _, ls in L['sections'])} lines, {sum(b for _, _, b in form)} bars at {L['bpm']} beats a minute = {secs} seconds (kept songs 165, 206, 243 by quartile)"); [print(" ", f) for f in flags]; sys.exit(0)
    rec = write(L, N, K); out = sys.argv[1].replace(".json", "") + ".song.json"; json.dump(rec, open(out, "w"), indent=1, default=float)
    if "error" in rec: print(rec["error"], rec.get("deaths"), rec.get("flags")); sys.exit(1)
    BD.midi(rec, out.replace(".json", ".mid")); m = rec["melody"]
    print(f"{rec['title']} in {rec['metre']}, key {rec['key']['key']} ({rec['key']['lowest']}-{rec['key']['highest']}{', ' + rec['key']['capo'] if rec['key']['capo'] else ''}); chord draft {rec['chord_pick']['draft']} of {rec['chord_pick']['drafts']}, charge {rec['chord_pick']['charge']}")
    print(f"melody: {m['survivors']} of {m['made']} survive; pick {m['pick']} charge {m['charge']} (median build {m['median_charge']:.2f}); deaths {m['deaths']}")
    for n, k, nb in rec["form"]: print(f"  {n}: " + " | ".join(rec["chords"][n]))
    print("judge 7:", {k: v for k, v in (rec.get("judge7") or {}).items() if k not in ("readings_read_together", "the_old_pick_notes")})
    print("checks:", rec["checks"]); print("band:", rec["band_sources"]); print("levels:", rec["levels"]); print("band checks:", rec["band_checks"]); print("flags:", rec["flags"])
