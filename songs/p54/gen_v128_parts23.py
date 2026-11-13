"""v128 Run 3, Part 2: the patches gen_v128.py adds after Part 1. Each is gated by ON8() on part 2 (ZE_PART), and with it off the chart is the
song's own (one chord a bar), chord_at reads the bar, and no draw is added to the build's generator, so Part 1's runs reproduce from these files.
  438: the chart drawn so that its share of bars with two or more changes and its share of bars holding the last bar's chord lie inside the
       kept middle halves (zeneng_v123_bass_at_the_chord.json), a song with no two-change bar allowed at the kept rate (25% and 37%: 31%).
       The edits are made on each section's chord list, so sections of one kind keep one chart; a section's last bar (its cadence) is kept.
       A held bar takes the chord of the bar before; a bar of two changes takes, on its third beat, the chord a fifth above the next bar's
       root where the song has it, or else the next bar's chord. The chart is drawn once a song, from its own seed ("438 chart <song>").
  440: the bass on the root at every change, or, in a song drawn to have any (the kept 54% of songs have none), on the third or fifth where
       that makes a step to a neighbour, in at most one chord in twelve.
  the chord at the note: chord_at reads the half-bar the note falls in; every reading of a chord takes the chord at the note."""
def P(old, new, count=1, songs=None): return (old, new, count, songs)
CHART = r'''
import random as _rnd8
K438 = json.load(open(f"{H118}/tables/zeneng_v123_bass_at_the_chord.json"))
Q438 = K438["the chart, by song: kept quartiles (438, 440)"]; Z438 = K438["kept songs with no bar of two changes"]
BASS8 = {}                                                                                 # 440: a chord written over its third or fifth: the bass's pitch class
PCN8 = {0: "C", 1: "C#", 2: "D", 3: "Eb", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "Ab", 9: "A", 10: "Bb", 11: "B"}
def bass_of(ch): return BASS8.get(ch, M.CH[ch][0])
def chart_shares(H):
    """438: H, the chord of every half-bar; a change is a half-bar whose chord (root, bass, kind) differs from the one before."""
    ev = collections.Counter()
    for h_ in range(len(H)):
        if h_ == 0 or H[h_] != H[h_ - 1]: ev[h_ // 2] += 1
    nb_ = len(H) // 2
    return sum(1 for v_ in ev.values() if v_ >= 2) / nb_, 1 - len(ev) / nb_, sum(ev.values())
def draw_chart(song):
    """438 and 440: the song's chart drawn once from its own seed; returns the half-bar chart and what was done."""
    r_ = _rnd8.Random(f"438 chart {song}")
    secs = []; b_ = 0
    for nm_, kind_, nb_ in FORM: secs.append((nm_, kind_, b_, nb_)); b_ += nb_
    units = {}; sec_unit = {}
    for nm_, kind_, b0_, nb_ in secs:
        key_ = (kind_, tuple(CHORD[b0_:b0_ + nb_])); units.setdefault(key_, [h_ for c_ in CHORD[b0_:b0_ + nb_] for h_ in (c_, c_)]); sec_unit[nm_] = key_
    def full():
        H_ = []
        for nm_, kind_, b0_, nb_ in secs: H_ += units[sec_unit[nm_]]
        return H_
    s2_0, sh_0, _ = chart_shares(full())
    none2 = r_.random() < (Z438[0] + Z438[1]) / 2
    t2 = 0.0 if none2 else r_.uniform(max(1.0 / NBARS, Q438["bars_with_two_or_more_changes"]["q25"]), Q438["bars_with_two_or_more_changes"]["q75"])
    th = r_.uniform(Q438["bars_with_no_change"]["q25"], Q438["bars_with_no_change"]["q75"])
    names = [c_ for c_ in M.CH if "/" not in c_]; ops = []
    def fifth_above(c_):
        rt_ = (M.CH[c_][0] + 7) % 12; cs_ = [x_ for x_ in names if M.CH[x_][0] == rt_]
        return cs_[0] if cs_ else None
    for it_ in range(400):                                                                   # holds first, toward the drawn share
        s2_, sh_, _ = chart_shares(full())
        if sh_ >= th - 0.5 / NBARS: break
        cand_ = [(k_, j_) for k_, U_ in units.items() for j_ in range(1, len(U_) // 2 - 1)
                 if U_[2 * j_] == U_[2 * j_ + 1] and U_[2 * j_] != U_[2 * j_ - 1] and U_[2 * j_ + 2] != U_[2 * j_ - 1]]
        if not cand_: break
        k_, j_ = r_.choice(sorted(cand_)); U_ = units[k_]; U_[2 * j_] = U_[2 * j_ + 1] = U_[2 * j_ - 1]; ops.append(("hold", k_[0], j_))
    for it_ in range(400):                                                                   # then bars of two changes
        s2_, sh_, _ = chart_shares(full())
        if s2_ >= t2 - 0.5 / NBARS: break
        cand_ = []
        for k_, U_ in units.items():
            for j_ in range(1, len(U_) // 2 - 1):
                a_, nx_ = U_[2 * j_], U_[2 * j_ + 2]
                if U_[2 * j_ + 1] != a_ or a_ == U_[2 * j_ - 1]: continue
                x_ = fifth_above(nx_)
                if x_ is None or x_ in (a_, nx_): x_ = nx_ if nx_ != a_ else None
                if x_ is not None: cand_.append((k_, j_, x_))
        if not cand_: break
        k_, j_, x_ = r_.choice(sorted(cand_)); units[k_][2 * j_ + 1] = x_; ops.append(("two", k_[0], j_, x_))
    inv = []
    if r_.random() >= (0.427 + 0.648) / 2:                                                   # 440: a song with inversions, at most one chord in twelve
        _, _, nev_ = chart_shares(full()); kt_ = r_.randint(1, max(1, nev_ // 12)); got_ = 0
        def bm(a_, b2_): d_ = (b2_ - a_) % 12; return d_ if d_ <= 6 else d_ - 12
        for it_ in range(200):
            cand_ = []
            for k_, U_ in units.items():
                n_sec_ = sum(1 for v_ in sec_unit.values() if v_ == k_)
                if got_ + n_sec_ > kt_: continue
                for h_ in range(1, len(U_) - 1):
                    c_ = U_[h_]
                    if "/" in c_ or c_ == U_[h_ - 1]: continue
                    nx_ = next((U_[q_] for q_ in range(h_ + 1, len(U_)) if U_[q_] != c_), None)
                    if nx_ is None: continue
                    rt_ = M.CH[c_][0]; th_ = next((t_ for t_ in M.CH[c_][1] if (t_ - rt_) % 12 in (3, 4)), None)
                    for bp_ in [x_ for x_ in (th_, (rt_ + 7) % 12) if x_ is not None]:
                        l_, rr_ = abs(bm(bass_of(U_[h_ - 1]), bp_)) in (1, 2), abs(bm(bp_, bass_of(nx_))) in (1, 2)
                        if l_ or rr_: cand_.append((3 if (l_ and rr_) else 1, k_, h_, bp_, n_sec_))
            if not cand_: break
            w_, k_, h_, bp_, n_sec_ = r_.choices(sorted(cand_, key=lambda x_: (x_[1], x_[2], x_[3])), [x_[0] for x_ in sorted(cand_, key=lambda x_: (x_[1], x_[2], x_[3]))])[0]
            U_ = units[k_]; c_ = U_[h_]; nm8 = f"{c_}/{PCN8[bp_]}"
            M.CH[nm8] = M.CH[c_]; BASS8[nm8] = bp_
            for q_ in range(h_, len(U_)):
                if U_[q_] != c_: break
                U_[q_] = nm8
            got_ += n_sec_; inv.append((k_[0], h_, nm8))
            if got_ >= kt_: break
    H_ = full(); s2_, sh_, nev_ = chart_shares(full())
    return H_, dict(targets=dict(two_or_more=round(t2, 3), holding=round(th, 3), none_drawn=none2), before=dict(two_or_more=round(s2_0, 3), holding=round(sh_0, 3)),
                    after=dict(two_or_more=round(s2_, 3), holding=round(sh_, 3), changes=nev_), ops=ops, inversions=inv,
                    kept=dict(two_or_more=(Q438["bars_with_two_or_more_changes"]["q25"], Q438["bars_with_two_or_more_changes"]["q75"]), holding=(Q438["bars_with_no_change"]["q25"], Q438["bars_with_no_change"]["q75"]), none_rate=Z438))
CHART438 = None
if ON8("438"):
    CHORD2, CHART438 = draw_chart(SONG8)
    CHORD[:] = CHORD2[0::2]                                                                 # the bar's first chord (readers of the bar)
else:
    CHORD2 = [h_ for c_ in CHORD for h_ in (c_, c_)]
if ON8("at_note"):
    def _chord_at8(t): return CHORD2[max(0, min(2 * NBARS - 1, t // 24))]                   # the chord at the note: the half-bar it falls in
    M.chord_at = _chord_at8
'''
PATCHES = [
    P('M.FORM, M.PLAN, M.BAR0, M.CHORD, M.NBARS, M.KIND, M.SUNG = FORM, PLAN, BAR0, CHORD, NBARS, KIND, SUNG\n',
      'M.FORM, M.PLAN, M.BAR0, M.CHORD, M.NBARS, M.KIND, M.SUNG = FORM, PLAN, BAR0, CHORD, NBARS, KIND, SUNG\n' + CHART),
    # 440 with 450: a second or seventh from the bass reads the bass, not the root
    P('        if r461 in (1, 2, 10, 11): w *= LK["sb461"]\n', '        if ((p - bass_of(ch)) % 12 if ON8("440") else r461) in (1, 2, 10, 11): w *= LK["sb461"]\n'),
    P('                sb=float(np.mean([x_[0] in (1, 2, 10, 11) for x_ in rel_])))',
      '                sb=float(np.mean([((n_["p"] - bass_of(M.chord_at(n_["on"]))) % 12 if ON8("440") else x_[0]) in (1, 2, 10, 11) for n_, x_ in zip(W_, rel_)])))'),
    # the record: the half-bar chart and what 438 and 440 did
    P('form=FORM, chords=CHORD,', 'form=FORM, chords=CHORD, chords2=CHORD2, bass8=dict(BASS8),'),
    P('    rerun["v128_part"] = V128;', '    rerun["chart438"] = CHART438\n    rerun["v128_part"] = V128;'),
]
