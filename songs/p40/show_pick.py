import pickle, sys, collections
D=pickle.load(open(sys.argv[1] if len(sys.argv)>1 else 'melody_main.pkl','rb')); p=D['pick']
NM=['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
def nm(x): return NM[x%12]+str(x//12-1)
sys.path.insert(0,'/home/claude/p40'); import lyric_p40 as L
lines=collections.OrderedDict()
for n in p['notes']: lines.setdefault(n['line'],[]).append(n)
print(p['fp'], p['meta']['registers'], p['meta']['plans'])
for ln,ns in lines.items():
    b0=ns[0]['on']//48
    print(f"{ln:16s} b{b0+1:3d}", " ".join(f"{nm(n['p'])}{'' if not n['slur'] else '~'}@{(n['on']%48)/12:.2g}:{n['dur']}" for n in ns))
