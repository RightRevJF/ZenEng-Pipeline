"""print a survivor line by line: syllable, pitch, bar.beat, length, chord."""
import sys, pickle
k = int(sys.argv[1]) if len(sys.argv) > 1 else 0; mode = sys.argv[2] if len(sys.argv) > 2 else "main"
sys.argv = [sys.argv[0], "1", mode]
import melody_p37 as P
M = P.M
d = pickle.load(open(f'/home/claude/p37/melody_{mode}.pkl', 'rb')); c = d['alive'][k]
NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
nm = lambda p: NAMES[p % 12] + str(p // 12 - 1)
on = {n['on'] for n in c['notes']}
print(c['fp'], c['meta']['plans'], c['meas']['composite'], c['meta']['targets'])
print('outside both:', c['read']['outside'])
for sec in P.SUNG:
    for i, (_, txt) in enumerate(M.WORDS_OF[sec]):
        if sec in ("Chorus 2",) or (sec == "Chorus 1" and i >= 4): continue
        ns = [n for n in c['notes'] if n['line'] == f'{sec}:{i}']; sy = P.LINES[sec][i]
        row = []
        for n in ns:
            b, r = divmod(n['on'], 48); w = sy[n['syl']][0] if not n['slur'] else '~'
            row.append(f"{w}{'*' if n['stress'] else ''}:{nm(n['p'])}@{b + 1}.{r / 12 + 1:g}/{n['dur']}[{M.chord_for(n, on)}]")
        print(f"{sec} {i + 1}: {txt}\n   " + '  '.join(row))
