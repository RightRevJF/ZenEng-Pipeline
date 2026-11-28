"""One pop 3/4 arm read whole into one JSON: the record's switches, forms fired and deaths; pop_read's marks; K3 by how made; the share of marked lines drawn fresh; the run mend's chord share; the source lines; lines beginning late; count (a) and the pool.  python3 studies/other_metres/read_pop_arm.py LYRIC.json DIR -> prints JSON."""
import os, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [HERE]
import count_k3_by_made as K, count_sources as CS, count_after_251 as CA, read_package as RP
def find(o, key):
    if isinstance(o, dict):
        if key in o: return o[key]
        for v in o.values():
            r = find(v, key)
            if r is not None: return r
def run(script, *a): return json.loads(subprocess.run([sys.executable, os.path.join(HERE, script)] + list(a), capture_output=True, text=True, check=True).stdout)
if __name__ == "__main__":
    lyr, d = sys.argv[1], sys.argv[2]; rec = os.path.join(d, os.path.basename(lyr).replace(".json", ".song.json")); R = json.load(open(rec)); L = json.load(open(lyr)); sp = R["spec"]
    tmp = os.path.join(d, "pop_read.json"); subprocess.run([sys.executable, os.path.join(HERE, "pop_read.py"), lyr, "words=" + d], env=dict(os.environ, OUT=tmp), capture_output=True, check=True)
    wa = run("why_again_fresh.py", rec, "300"); mend = run("count_run_mend.py", rec, "300")
    out = dict(switches={k: sp.get(k) for k in ("again_words", "source_words", "source_stressed", "early_entries", "early_from_table")}, judge_ran=R["judge7"].get("pass_the_gate") is not None, forms_fired={k: v for k, v in (find(R, "stats") or {}).items() if "749.25" in k or k.startswith("834")}, deaths=R["melody"]["deaths"], made=R["melody"]["made"],
               read=json.load(open(tmp))["words"], k3_by_how_made=K.read(rec)["by_how_made"], share_drawn_fresh=round(wa["drawn_fresh_712"] / wa["tries_to_sing_a_marked_line_again"], 4), mend={a: b for a, b in mend.items() if a != "counts"}, sources=CS.read(rec), lines_beginning_after_their_bar_line=RP.late(rec), count_a=CA.count_a(L, R), count_b=CA.count_b(L, R))
    print(json.dumps(out, indent=1))
