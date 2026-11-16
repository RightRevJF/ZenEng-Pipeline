"""Song 54: 730's own rule (luthier_judge5.pick: the least charge, then nearest the kept medians within 0.02) over the clean survivors of the
main run that sing no two syllables on one onset (749.1; the rule song 51's re-pick used). The judge's pick d48480b70b0d sings 'coffee'
and 'can' on one onset in verse 4 (a note of no length), which no singer can do."""
import pickle, collections, sys
sys.path[:0] = ["/home/claude/p64"]
import luthier_judge5 as J5
D = pickle.load(open("/home/claude/p64/runl7/melody_l7_p64_main.pkl", "rb"))
alive = [b for b in D["all"] if not b["fails"] and not b["info"]["soft"]]
def two_on_one(b):
    c = collections.Counter(o for o, d, p, s, l, st, sy in b["notes"]); return any(v > 1 for v in c.values()) or any(d <= 0 for o, d, p, s, l, st, sy in b["notes"])
ok = [b for b in alive if not two_on_one(b)]
pk, R = J5.pick([(b["fp"], [(o, p, s) for o, d, p, s, l, st, sy in b["notes"]]) for b in ok])
RD = dict(R)
print(f"clean survivors {len(alive)}; with two syllables on one onset {sum(two_on_one(b) for b in alive)}; eligible among the rest {sum(1 for r in RD.values() if r['eligible for the pick'])}")
print("re-pick:", pk, {k: RD[pk][k] for k in ("charge", "distance from the kept medians")})
pickle.dump(dict(pick=pk, n_clean=len(alive), n_two=sum(two_on_one(b) for b in alive), n_ok=len(ok), eligible=sum(1 for r in RD.values() if r["eligible for the pick"])), open("/home/claude/p64/repick.pkl", "wb"))
