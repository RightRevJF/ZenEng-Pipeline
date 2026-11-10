"""Song 33: the frozen pick (#1 by the composite among the register gate's survivors; no landing or dull-line flags); no hand edits."""
import pickle
import melody_p33 as M
R = pickle.load(open("/home/claude/p33/melody_result.pkl", "rb"))
c = dict(R["alive"][0])
cert, meas = M.evaluate(c); assert cert is None
c["hand"] = []; c["from"] = c["fp"]; c["by_construction"] = R["by_construction"]
c["search"] = dict(made=R["made"], tries=R["tries"], survivors=R["survivors"], order_fp=R["order_fp"], deaths=dict(R["deaths"]), rerun=R["rerun"], top20=R["top20"],
                   reproduced=True)
pickle.dump(c, open("/home/claude/p33/melody_final.pkl", "wb"))
print("fp", c["fp"], {k: v for k, v in meas.items() if k in ("composite", "tops", "flags_landing", "flags_dull", "longest_s")})
