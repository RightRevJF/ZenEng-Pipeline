"""538's reading on song 46: the record's bass (bass_v130.py, 538) beside v129's routine on the same record (538 off), each section's eight
bars read with Window 144's measures and 445-448's tests; 538's cells (bar rhythms; rhythm and figure; rhythm, figure and articulation)."""
import pickle, json, sys
sys.path[:0] = ["/home/claude/p56", "/home/claude/p55"]
import bass_v130 as B130, bass_v129 as B129
rec = pickle.load(open("/home/claude/p56/song_record.pkl", "rb"))
old, _ = B129.write_bass(rec, 33, (9, "minor"), "46")
new = rec["bass"]
RES = {}
for lab, B in (("v129 routine (538 off)", old), ("v130 routine (538), the record", new)):
    rows = B130.read_song(rec, B)
    RES[lab] = dict(summary=B130.summary(rows), windows=rows, root_at_changes=B130.root_at_changes(B, rec["chords2"], rec["nbars"]))
json.dump(RES, open("/home/claude/p56/records/bass_readings_v130.json", "w"), indent=1, default=str)
for lab, x in RES.items():
    W = [w for w in x["windows"] if w.get("tests")]
    print(lab, "windows passing every test:", sum(1 for w in W if not any(v is False for v in w["tests"].values())), "of", len(W))
    print("   cells538 (four-kick windows):", [(w["sec"], w["cells538"]["rhythms"], w["cells538"]["rhythm_and_articulation"], w["cells538"]["rhythm_and_figure"], w["cells538"]["rhythm_figure_articulation"]) for w in W if w.get("four")])
