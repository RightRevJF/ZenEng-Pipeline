"""Every reading the test report prints, from the frozen pick and the controls (melody_main.pkl, melody_ctlA.pkl, melody_ctlB.pkl)."""
import sys, pickle, json, collections, math
import numpy as np
sys.argv = ["x", "1", "main"]; sys.path.insert(0, "/home/claude/p36")
import melody_p36 as M
R = {m: pickle.load(open(f"/home/claude/p36/melody_{m}.pkl", "rb")) for m in ("main", "ctlA", "ctlB")}
T = M.T
pick = R["main"]["alive"][0]
ctl_pick = R["ctlA"]["alive"][0]
NAMES = ["C", "D♭", "D", "E♭", "E", "F", "G♭", "G", "A♭", "A", "B♭", "B"]
def nm(p): return f"{NAMES[p % 12]}{p // 12 - 1}"

def designs(c):
    d = M.phrase_designs(c["notes"]); out8 = {}; out16 = {}
    for k, v in d["at8"].items(): out8[k] = dict(label=v["label"], u2=(round(v["u2"][1], 2), round(v["u2"][2], 2)), u3=(round(v["u3"][1], 2), round(v["u3"][2], 2)), u4_returns_u2=v["u4_returns_u2"], second_half_closes=v["second_half_closes"])
    for k, v in d["at16"].items(): out16[k] = dict(label=v["label"], u2=(round(v["u2"][1], 2), round(v["u2"][2], 2)), u3=(round(v["u3"][1], 2), round(v["u3"][2], 2)), u4_returns_u2=v["u4_returns_u2"], u42=(round(v["u42"][1], 2), round(v["u42"][2], 2)), second_half_closes=v["second_half_closes"])
    return dict(at8=out8, at16=out16, stock8=d["stock8"], stock16=d["stock16"])

def core(c):
    ns = c["notes"]; ps = [n["p"] for n in ns]
    rep = M.repetition(ns); iv = M.interval_shares(ps)
    return dict(pitch_bits=M.pitch_bits(ps), intervals=iv, exact=rep["exact"], repetition=rep, designs=designs(c), rhythm_bits=M.rhythm_bits(ns),
                returns=[(r[0], r[1], round(r[2], 2), round(r[3], 2)) for r in M.returns_related(c)], range=(nm(min(ps)), nm(max(ps))), notes=len(ns))

# ---- text setting (149, 150, 151) ----
def syllables(c):
    out = []
    for ln in dict.fromkeys(n["line"] for n in c["notes"]):
        sec, i = ln.split(":"); i = int(i); sy = M.LINES[sec][i]; ns = [n for n in c["notes"] if n["line"] == ln]
        for j in range(len(sy)):
            sn = [n for n in ns if n["syl"] == j]
            if not sn: continue
            w = sy[j][0]; first = j == 0 or sy[j - 1][0] != w; single = first and (j == len(sy) - 1 or sy[j + 1][0] != w)
            out.append(dict(line=ln, j=j, word=w, stress=sy[j][1], initial=first, single=single, on=sn[0]["on"], dur=sum(n["dur"] for n in sn),
                            notes=len(sn), last=(j == len(sy) - 1), p=max(n["p"] for n in sn)))
    return out
def level(t):
    t %= M.BAR
    return 1.0 if t == 0 else 0.75 if t == 24 else 0.5 if t % 12 == 0 else 0.25 if t % 6 == 0 else 0.0
def text_setting(c):
    S = syllables(c); poly = [s for s in S if not s["single"]]
    ini = [s for s in poly if s["initial"]]; lat = [s for s in poly if not s["initial"]]; sng = [s for s in S if s["single"]]
    mel = [s for s in S if s["notes"] >= 2]
    lines = list(dict.fromkeys(n["line"] for n in c["notes"]))
    fl = []; off = 0
    for ln in lines:
        ns = [n for n in c["notes"] if n["line"] == ln]; fl.append(ns[-1]["dur"] / np.median([n["dur"] for n in ns]))
        off += ns[0]["on"] % M.BAR != 0
    ps = [n["p"] for n in c["notes"]]; top = max(ps); tn = [n for n in c["notes"] if n["p"] == top][0]
    ts = [s for s in S if s["line"] == tn["line"] and s["j"] == tn["syl"]][0]
    med = np.median([n["dur"] for n in c["notes"]])
    return dict(initial_strength=np.mean([level(s["on"]) for s in ini]), later_strength=np.mean([level(s["on"]) for s in lat]),
                single_strength=np.mean([level(s["on"]) for s in sng]),
                initial_on_downbeat=np.mean([s["on"] % M.BAR == 0 for s in ini]), later_on_downbeat=np.mean([s["on"] % M.BAR == 0 for s in lat]),
                dur_ratio_initial_over_later=np.mean([s["dur"] for s in ini]) / np.mean([s["dur"] for s in lat]),
                stressed_over_unstressed_in_words=np.mean([s["dur"] for s in poly if s["stress"]]) / np.mean([s["dur"] for s in poly if not s["stress"]]),
                melisma_rate=len(mel) / len(S), melisma_at_phrase_end=sum(1 for s in mel if s["last"]) / max(1, len(mel)),
                final_lengthening=float(np.median(fl)), phrase_starts_off_downbeat=off / len(lines), syllables=len(S), phrases=len(lines),
                summit=dict(pitch=nm(top), word=ts["word"], syllable_stressed=ts["stress"], line=tn["line"], dur_over_median=tn["dur"] / med,
                            at=f"bar {tn['on'] // M.BAR + 1}, beat {(tn['on'] % M.BAR) / 12 + 1:.2f}", position=c["notes"].index(tn) / len(c["notes"]),
                            at_phrase_end=tn is [n for n in c["notes"] if n["line"] == tn["line"]][-1]))

# ---- rhythm (158) ----
def rhythm(c):
    ns = c["notes"]; on = {n["on"] for n in ns}; N = len(ns)
    pos = [n["on"] % M.BAR for n in ns]
    iois = [b["on"] - a["on"] for a, b in zip(ns, ns[1:]) if b["line"] == a["line"]]
    def share(v): return sum(1 for x in iois if x == v) / len(iois)
    npvi = 100 * np.mean([abs(a - b) / ((a + b) / 2) for a, b in zip(iois, iois[1:])])
    bars = M.bar_cells(ns); nb = sum(1 for v in bars.values() if v)
    return dict(on_downbeat=sum(p == 0 for p in pos) / N, on_other_beats=sum(p % 12 == 0 and p != 0 for p in pos) / N,
                on_eighth_offbeat=sum(p % 12 == 6 for p in pos) / N, on_sixteenth=sum(p % 6 == 3 for p in pos) / N, pushed=M.pushed_share(ns),
                ioi_sixteenth=share(3), ioi_eighth=share(6), ioi_dotted_eighth=share(9), ioi_quarter=share(12), ioi_dotted_quarter=share(18),
                ioi_half=share(24), npvi=npvi, onsets_per_bar=N / nb, notes_per_second=M.density(ns),
                distinct_bar_rhythms_per_bar=M.repetition(ns)["distinct_rhythms"] / M.repetition(ns)["bars"])

# ---- declamation (161) ----
def declamation(c):
    rows = []
    for ln in dict.fromkeys(n["line"] for n in c["notes"]):
        ns = [n for n in c["notes"] if n["line"] == ln]; st = [n for n in ns if n["stress"]]
        if not st: continue
        parts = collections.OrderedDict()
        for n in st:
            b = n["on"] // M.BAR; r = n["on"] % M.BAR
            parts.setdefault(b, []).append(str(r // 12 + 1) if r % 12 == 0 else f"{r / 12 + 1:.2f}".rstrip("0").rstrip("."))
        last = st[-1]["on"] % M.BAR
        rows.append(dict(line=ln, schema=" | ".join(" ".join(v) for v in parts.values()), last_strong=last in (0, 24), last_on_downbeat=last == 0,
                         starts_before_downbeat=ns[0]["on"] % M.BAR != 0, span=ns[-1]["on"] // M.BAR - ns[0]["on"] // M.BAR + 1))
    sch = collections.Counter(r["schema"] for r in rows)
    return dict(rows=rows, last_strong=np.mean([r["last_strong"] for r in rows]), last_on_downbeat=np.mean([r["last_on_downbeat"] for r in rows]),
                starts_before=np.mean([r["starts_before_downbeat"] for r in rows]), spans=collections.Counter(r["span"] for r in rows), top_schemas=sch.most_common(5))

# ---- harmony (173) and sections (176) ----
def harmony():
    ch = M.CHORD; sung = M.CHORD
    seq = [ch[0]] + [b for a, b in zip(ch, ch[1:]) if b != a]
    before = collections.Counter(a for a, b in zip(seq, seq[1:]) if b == "Eb")
    moves = collections.Counter()
    for a, b in zip(seq, seq[1:]):
        d = (M.CH[b][0] - M.CH[a][0]) % 12
        moves["up a fourth / down a fifth" if d == 5 else "down a fourth / up a fifth" if d == 7 else "by step" if d in (1, 2, 10, 11) else "by third" if d in (3, 4, 8, 9) else "tritone"] += 1
    tot = sum(moves.values())
    return dict(vocabulary=sorted(set(ch), key=lambda x: "Eb Bb Cm Ab Db Fm".split().index(x)), roman={k: M.ROMAN[k] for k in set(ch)},
                before_tonic={M.ROMAN[k]: v for k, v in before.items()}, root_motion={k: v / tot for k, v in moves.items()},
                chords_per_bar=len(seq) / len(ch), changes_per_bar=sum(1 for a, b in zip(ch, ch[1:]) if a != b) / len(ch),
                tonic_time=ch.count("Eb") / len(ch), sevenths=0.0, inverted=0.0, distinct=len(set(ch)))
def sections():
    out = []; seen = set(); prev_last = None
    for nm_, kind, nb in M.FORM:
        b0 = M.BAR0[nm_]; ch = M.CHORD[b0:b0 + nb]
        new = [x for x in dict.fromkeys(ch) if x not in seen]
        out.append(dict(section=nm_, bars=nb, first=M.ROMAN[ch[0]], last=M.ROMAN[ch[-1]], tonic_time=ch.count("Eb") / nb,
                        changes_per_bar=(1 + sum(1 for a, b in zip(ch, ch[1:]) if a != b)) / nb, distinct=len(set(ch)),
                        new_chords=[M.ROMAN[x] for x in new], join=(M.ROMAN[prev_last] + " → " + M.ROMAN[ch[0]]) if prev_last else "—"))
        seen |= set(ch); prev_last = ch[-1]
    return out

def deaths_table():
    main = R["main"]; a = R["ctlA"]; b = R["ctlB"]
    rows = []
    for g in M.NEW_GATES:
        rows.append(dict(gate=g, deaths=main["deaths"].get(g, 0) + sum(v for k, v in main["deaths"].items() if k.startswith(g.split(" (")[0]) and k != g),
                         would=main["would"][g], ctlA=a["would"][g], ctlB=b["would"][g], constructed=M.CONSTRUCTED.get(g)))
    return rows

def spread(m):
    sp = R[m]["spread"]; return {k: (float(np.percentile(v, 5)), float(np.median(v)), float(np.percentile(v, 95))) for k, v in sp.items()}

out = dict(pick_fp=pick["fp"], pick_meas=pick["meas"], pick_plans=pick["meta"]["plans"], pick_shifts={f"{k[0]} line {k[1] + 1}": v for k, v in pick["meta"]["shifts"].items()},
           pick=core(pick), ctl=core(ctl_pick), ctl_fp=ctl_pick["fp"], ctl_meas=ctl_pick["meas"], ctl_plans=ctl_pick["meta"]["plans"],
           spread_main=spread("main"), spread_ctlA=spread("ctlA"), spread_ctlB=spread("ctlB"),
           flagged_main=sum(1 for c in R["main"]["alive"] if c["meas"]["flag_p25"]), survivors=dict((m, R[m]["survivors"]) for m in R),
           deaths={m: dict(R[m]["deaths"]) for m in R}, would={m: dict(R[m]["would"]) for m in R}, ret_fail={m: dict(R[m]["ret_fail"]) for m in R},
           order={m: R[m]["order_fp"] for m in R}, rerun={m: R[m]["rerun"] for m in R},
           text=text_setting(pick), text_ctl=text_setting(ctl_pick), rhythm=rhythm(pick), decl=declamation(pick), harmony=harmony(), sections=sections(),
           outer=M.outer(pick["notes"]), outer_ctl=M.outer(ctl_pick["notes"]), keyword=M.keyword_chord(pick["notes"]), chord_tones=M.chord_tone_share(pick["notes"]),
           legs=M.sequences(pick["notes"]), deaths_table=deaths_table(), completable=M.chords_completable(pick["notes"]))
# the flagged survivors' share of all survivors, and the pick's place among them
pickle.dump(out, open("/home/claude/p36/readings.pkl", "wb"))
if __name__ == "__main__" or True:
    P = out["pick"]; Cc = out["ctl"]
    print("pick", out["pick_fp"], "comp", out["pick_meas"]["composite"], "| control first pick", out["ctl_fp"], "comp", out["ctl_meas"]["composite"])
    for lab, x in (("pick", P), ("control", Cc)):
        iv = x["intervals"]
        print(f"{lab:8s} pitch {x['pitch_bits']:.3f}  repeat {iv['repeat']:.3f} step {iv['step']:.3f} third {iv['third']:.3f} 4/5 {iv['fourth_fifth']:.3f} >5th {iv['larger']:.3f} desc {iv['descending']:.3f}  exact {x['exact']:.3f}  stock8 {x['designs']['stock8']:.2f} stock16 {x['designs']['stock16']:.2f} range {x['range']}")
        for k, v in x["designs"]["at8"].items(): print("     8:", k, v)
        for k, v in x["designs"]["at16"].items(): print("    16:", k, v)
    print("spread main", {k: tuple(round(z, 3) for z in v) for k, v in out["spread_main"].items()})
    print("spread ctlA", {k: tuple(round(z, 3) for z in v) for k, v in out["spread_ctlA"].items()})
    print("text", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in out["text"].items()})
    print("rhythm", {k: round(float(v), 3) for k, v in out["rhythm"].items()})
    d = out["decl"]; print("decl last strong", round(d["last_strong"], 3), "downbeat", round(d["last_on_downbeat"], 3), "starts before", round(d["starts_before"], 3), d["spans"], d["top_schemas"])
    print("harmony", out["harmony"]); [print("  ", s) for s in out["sections"]]
    print("outer", {k: round(v, 3) for k, v in out["outer"].items()})
    print("outer ctl", {k: round(v, 3) for k, v in out["outer_ctl"].items()})
    print("keyword", round(out["keyword"][0], 3), "chord tones / nct resolved", [round(x, 3) for x in out["chord_tones"]], "legs", out["legs"], "192 bad", out["completable"])
    for r in out["deaths_table"]: print("  ", r)
    print("returns", P["returns"])
