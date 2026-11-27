"""Parse ChoCo v1.0.0 (Zenodo 7706751) iReal Pro (forum, playlists) and Wikifonia JAMS into a compact chart cache.
Per chart: id, part, title, artists (as given), genre, key (tonic pc, mode) if given, chords: list of [time, dur, root_pc, bitmap12, bass_pc]."""
import json, csv, os, sys
import mir_eval.chord as mc
R = "/home/claude/dl/choco/smashub-choco-f7dd3ee/partitions"
PC = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def pc(n):
    v = PC[n[0]]
    for ch in n[1:]:
        v += 1 if ch == '#' else -1 if ch == 'b' else 0
    return v % 12
out = []; bad = 0
def load(part, meta, title_k, art_k, genre_k, jdir):
    global bad
    for r in csv.DictReader(open(meta)):
        jid = r['id'].replace('.jams', '')
        p = os.path.join(R, jdir, jid + '.jams')
        if not os.path.exists(p): continue
        d = json.load(open(p)); ch = []; key = None
        for a in d['annotations']:
            if a['namespace'] in ('chord', 'chord_harte') and not ch:
                for o in a['data']:
                    v = o['value']
                    if v in ('N', 'X', None): continue
                    root = None
                    for vv in (v, v.replace('113', '13'), v.split('(')[0]):
                        try:
                            root, bm, bass = mc.encode(vv); break
                        except Exception:
                            root = None
                    if root is None:
                        bad += 1; continue
                    if root < 0: continue
                    ch.append([round(o['time'], 3), round(o['duration'], 3), int(root), [int(x) for x in bm], int((root + bass) % 12)])
            if a['namespace'] == 'key_mode' and a['data'] and key is None:
                v = a['data'][0]['value']
                try:
                    t, m = v.split(':'); key = [pc(t), m]
                except Exception: key = None
        out.append(dict(id=jid, part=part, title=r.get(title_k, '').strip(), artists=r.get(art_k, '').strip(),
                        genre=r.get(genre_k, '') if genre_k else '', key=key, chords=ch))
load('ireal-forum', f'{R}/ireal-pro/choco/forum/meta.csv', 'title', 'artists', 'genre', 'ireal-pro/choco/forum/jams-converted')
load('ireal-playlists', f'{R}/ireal-pro/choco/playlists/meta.csv', 'title', 'artists', 'genre', 'ireal-pro/choco/playlists/jams-converted')
load('wikifonia', f'{R}/wikifonia/choco/meta.csv', 'score_title', 'score_composers', None, 'wikifonia/choco/jams-converted')
json.dump(out, open('/home/claude/dl/choco/charts_run08.json', 'w'))
print(len(out), 'charts; unparsed chord labels', bad, '; with >=8 chords', sum(len(c['chords']) >= 8 for c in out))
