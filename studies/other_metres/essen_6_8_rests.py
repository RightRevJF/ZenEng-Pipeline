"""Every rest in Essen's 6/8 tunes (music21's copy of the collection), in eighths -> essen_6_8_rests.json.  python3 studies/other_metres/essen_6_8_rests.py"""
import json, os, numpy as np
from music21 import corpus, converter
rests = []; tunes = 0
for p in corpus.getComposer('essenFolksong'):
    try: op = converter.parse(p)
    except Exception: continue
    for sc in (op.scores if hasattr(op, 'scores') else [op]):
        ts = sc.recurse().getElementsByClass('TimeSignature')
        if not ts or any(t.ratioString != '6/8' for t in ts): continue
        tunes += 1; run = 0.0
        for n in sc.flatten().notesAndRests:
            if n.isRest: run += float(n.quarterLength)
            else:
                if run > 0: rests.append(run * 2)
                run = 0.0
a = np.array(rests); json.dump(dict(tunes_in_6_8=tunes, rests=len(a), rests_a_tune=round(len(a) / max(1, tunes), 2), quartiles_in_eighths=[float(x) for x in np.percentile(a, (25, 50, 75))], share_a_bar_or_longer=round(float(np.mean(a >= 6)), 3)), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'essen_6_8_rests.json'), 'w'), indent=1)
