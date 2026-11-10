"""print the v3 pick (or alive[k]) line by line: syllable, pitch, bar.beat, length, chord."""
import sys, pickle
k = int(sys.argv[1]) if len(sys.argv) > 1 else 0; mode = sys.argv[2] if len(sys.argv) > 2 else "main"
sys.argv = [sys.argv[0], "1", mode]
exec(open('/home/claude/p36/melody_v3_p36.py').read().split('if __name__ == "__main__":')[0])
d = pickle.load(open(f'/home/claude/p36/melody_v3_{mode}.pkl', 'rb')); c = d['alive'][k]
NAMES = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
nm = lambda p: NAMES[p % 12] + str(p // 12 - 1)
on = {n['on'] for n in c['notes']}
print(c['fp'], c['meta']['plans'], c['meas']['composite'])
for sec in SUNG:
    for i, (_, txt) in enumerate(M.WORDS_OF[sec]):
        ns = [n for n in c['notes'] if n['line'] == f'{sec}:{i}']; sy = LINES[sec][i]
        row = []
        for n in ns:
            b, r = divmod(n['on'], BAR); w = sy[n['syl']][0] if not n['slur'] else '~'
            row.append(f"{w}{'*' if n['stress'] else ''}:{nm(n['p'])}@{b+1}.{r/12+1:g}/{n['dur']}[{M.chord_for(n,on)}]")
        print(f"{sec} {i+1} ({line_bars(sec,i)} bars): {txt}\n   " + '  '.join(row))
