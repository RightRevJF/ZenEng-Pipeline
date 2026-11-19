"""The CoCoPops parser with one change: a note that begins a tie ('[8B') is read (its '[' set aside), not dropped. Writes corpora/cocopops_notes_ties.csv.gz (not committed); set LUTHIER_COCOPOPS_NOTES to it to build the tables with ties read."""
import sys, re, os
from pathlib import Path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lib", "luthier")); import cocopops_parse as CP
import pandas as pd
_orig = CP.recip_dur
def recip_dur(tok): return _orig(tok.lstrip("[({&"))
CP.recip_dur = recip_dur
rows = []; n = 0
for f in sorted(Path(sys.argv[1]).glob("*.hum")):
    try: r = CP.parse_file(f)
    except Exception as e: print("skip", f.name, e); continue
    if len(r) >= 30: rows += r; n += 1
D = pd.DataFrame(rows); D.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "corpora", "cocopops_notes_ties.csv.gz"), index=False); print("songs", n, "notes", len(D))
