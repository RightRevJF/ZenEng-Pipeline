"""Song 41 made for real (the writer's Q21-Q25): the pick from the design run, read line by line against the shortlist's fourth and seventh,
and taken as drawn (no hand edits). The pick, e6ba46e75684, is also 255's pick of record (the composite's first inside the judge's top half).
  Its hook leaps a fourth to C4 on 'WA-ter', turns through B3-A3-B3 and climbs to 'sing' on D4, beat 1 over G, held two beats. 'Now it only
  shines' rocks G3-A3 over the F chord and pushes 'shines' down to D3 ahead of the G. 'living water doesn't shine' climbs B3-C4 and
  through B-flat to E4 on 'shine', over C. The bridge sits around C3, under the verse's D3, and the verses talk on D3.
  The other two read: 95e182108e88 has the strongest climb (C4 three times to D4) but mutters its bridge on G2-A2 ('what's a river sound
  like' on G2 five times); f2d6305361d4 holds F#3 against the F chord on 'only' (bar 27) and leaps a seventh onto 'water' at the peak."""
import sys, pickle, copy
sys.argv = ["x", "1", "design"]; sys.path[:0] = ["/home/claude/p41"]
import melody_p41d as P
D = pickle.load(open("/home/claude/p41/melody_p41d_design.pkl", "rb")); Dr = pickle.load(open("/home/claude/p41/melody_p41d_design_r.pkl", "rb"))
assert D["order_fp"] == Dr["order_fp"]
PICK = "e6ba46e75684"
assert D["pick"]["fp"] == PICK
c = copy.deepcopy(D["pick"])
for _p in ("V", "C"): P.KNOBS[_p].update(D["knobs"][_p])
cert, meas = P.evaluate(c); fails = P.design_fails(c)
print("evaluate:", cert or "passes", "| design gates:", fails or "pass", "| soft", c["info"]["soft"], "| lift", c["info"]["lift"])
assert cert is None and not fails
c["judge"] = P.judge(c["notes"]); c["meas"] = meas; c["hand_edits"] = []
short = [x["fp"] for x in D["alive"] if x["fp"] in set(D["short"])]
c["picked_from"] = dict(run="design", order=D["order_fp"], rank_in_shortlist=short.index(PICK) + 1, rule="255's pick, read against shortlist 2-7 by ear")
pickle.dump(dict(pick=c, run=dict(order_fp=D["order_fp"], survivors=D["survivors"], made=D["made"], deaths=dict(D["deaths"]), rerun=D["rerun"], knobs=D["knobs"])),
            open("/home/claude/p41/melody_final_d.pkl", "wb"))
print(PICK, "judge", round(c["judge"]["combined"], 3), "composite", meas["composite"])
