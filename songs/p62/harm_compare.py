"""Before and after: the harmony readings (harm68.readings) for the old shadow parts and the new lines; writes harmony_compare.json."""
import json, pickle, harm68
B = json.load(open('/home/claude/p62/harmony_before.json')); R = pickle.load(open('/home/claude/p62/song_record.pkl', 'rb'))
def span(lead): return [n for n in lead if n['role'] == 'hook' or n['sec'] == 'Last Chorus']
out = {}
for lab, lead, hi, lo in (('before', B['lead'], B['harm_hi'], B['harm_lo']), ('after', R['lead'], R['harm_hi'], R['harm_lo'])):
    for k, p in (('high', hi), ('low', lo)): out[f"{lab} {k}"] = harm68.readings(span(lead), p)
json.dump(out, open('/home/claude/p62/harmony_compare.json', 'w'))
if __name__ == "__main__":
    for k, v in out.items(): print(k, {a: round(b, 2) if isinstance(b, float) else b for a, b in v.items()})
