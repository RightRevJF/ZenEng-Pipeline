import pickle, sys, melody_p35 as M
r = pickle.load(open('/home/claude/p35/melody_result.pkl', 'rb')); idx = int(sys.argv[1]) if len(sys.argv) > 1 else 0; c = r['alive'][idx]
N = 'C Db D Eb E F Gb G Ab A Bb B'.split(); nm = lambda p: N[p % 12] + str(p // 12 - 1)
print(c['fp'], c['plan'], c['meas']['composite'])
for ln in M.LINES:
    ns = [n for n in c['notes'] if n['line'] == ln]; w = M.WORDS[0][ln]
    print(ln, ' '.join(f"{w[n['syl']][0][:6]}:{nm(n['p'])}@{n['on'] // 36 + 1}.{n['on'] % 36 // 12 + 1}{'/' + str(n['dur']) if n['dur'] != 12 else ''}" for n in ns))
prev = None; out = []
for h in c['harm']:
    k = (h['chord'], h['bass'])
    if k != prev: out.append(f"{h['on'] // 36 + 1}.{h['on'] % 36 // 12 + 1}:{h['chord']}/{nm(h['bass'])}")
    prev = k
print(' '.join(out)); print(round(len(out) / 24, 2), 'chords a bar')
