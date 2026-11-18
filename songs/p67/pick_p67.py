"""Song 57 (Jehovah's Band): the pick of record. The research gates (research_p67.py, Parts 30 and 31: R1 the chorus above the verse,
R2 the chorus repeats itself, R3 typical cells, R4 low variety and surprise, R5 long notes on stressed syllables) read every clean
survivor of the main run; luthier_judge5 (730) picks over those that pass all five, or, if none do, over those that fail fewest. Taken as
drawn, no hand edits. The survivors are the builds with no cause in the run's record (749.35); evaluated again and written to melody_final.pkl with the gate readings of every clean survivor."""
import sys, pickle, copy, io, contextlib, os, json, collections
ARGV = list(sys.argv); sys.argv = ["x", "1", "main"]; sys.path[:0] = ["/home/claude/p67"]
with contextlib.redirect_stdout(io.StringIO()): import melody_l7_p67 as P
import luthier_judge5 as J5, research_p67 as RS
RUN = os.environ.get("RUNPKL", "/home/claude/p67/runl7/melody_l7_p67_main.pkl")
D = pickle.load(open(RUN, "rb"))
def rebuild(b):
    ns = []; last = {}
    for o, d, p, s, l, st, sy in b["notes"]:
        sl = last.get(l) == sy and sy is not None; last[l] = sy
        ns.append(dict(on=o, p=p, syl=sy, slur=sl, stress=st, dur=d, sec=s, line=l))
    return dict(notes=ns, meta=b["meta"], judge=b["judge"], info=b["info"], read=b["read"], lines=b["lines"], fp=b["fp"])
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
P.LK.update(D["line_knobs"])
clean = [rebuild(b) for b in D["all"] if b.get("cause") is None and not b["info"]["soft"]]   # D["all"] holds every build that reached evaluate; the survivors have no cause (749.35)
REEVAL = {c["fp"]: P.evaluate(copy.deepcopy(c))[0] for c in clean}                         # read, not used: a stored build drops 386's moved386, so 267 can fail on it (749.35)
R = RS.Ref(); TITLE = {f"{s}:{i}" for s in P.SUNG for i, (r, _) in enumerate(P.M.WORDS_OF[s]) if r == "hook"}
G = {}
for c in clean: G[c["fp"]] = RS.gates(R, c["notes"], TITLE)
nf = {fp: len(f) for fp, (r, f) in G.items()}; least = min(nf.values())
pool = [c for c in clean if nf[c["fp"]] == least]
pk, RJ = J5.pick([(c["fp"], [(n["on"], n["p"], n["sec"]) for n in c["notes"]]) for c in pool])
RD = dict(RJ)
if pk is None: pk = min(RD, key=lambda i: (RD[i]["charge"], RD[i]["distance from the kept medians"]))
c = copy.deepcopy(next(x for x in pool if x["fp"] == pk))
cert, meas = P.evaluate(c)
print("evaluate:", cert or "passes", "| soft", c["info"]["soft"], "| lift", c["info"]["lift"])
assert cert is None or cert[0] == "returns related (267)", cert                             # 749.35: 267 may fail on a stored build for want of moved386
c["judge"] = P.judge(c["notes"]); c["meas"] = meas; c["hand_edits"] = []
passing = [fp for fp, n in nf.items() if n == 0]
c["picked_from"] = dict(run=os.path.basename(RUN), order=D["order_fp"], rule="research gates R1-R5 (Parts 30, 31), then 730: luthier_judge5.pick over those that pass" + ("" if least == 0 else f" (none passed all five; the {len(pool)} failing fewest, {least})"),
                        judge5_pick_of_run=D["pick"]["fp"], clean=len(clean), reeval_fails_without_moved386={fp: str(v) for fp, v in REEVAL.items() if v}, passing_all=len(passing), pool=len(pool), gates=G[pk])
pickle.dump(dict(pick=c, gates={fp: dict(readings=r, fails=f) for fp, (r, f) in G.items()}, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"],
                 line_knobs=D["line_knobs"], chords2=D["chords2"], bass8=D["bass8"])), open("/home/claude/p67/melody_final.pkl", "wb"))
fails = collections.Counter(x for r, f in G.values() for x in f)
print("clean", len(clean), "| pass all five", len(passing), "| fails by gate", dict(fails), "| pick", pk, G[pk])
