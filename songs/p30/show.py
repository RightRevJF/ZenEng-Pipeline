import pickle, sys
sys.path[:0]=["/home/claude/p30","/home/claude/carol","/home/claude/pop"]
NM=['C','C#','D','Eb','E','F','F#','G','G#','A','Bb','B']
R=pickle.load(open(sys.argv[1] if len(sys.argv)>1 else "melody_result.pkl","rb"))
c = R["alive"][int(sys.argv[2]) if len(sys.argv)>2 else 0] if "alive" in R else R
import importlib.util
exec(open('/home/claude/p30/melody_p30.py').read().split('# ---- rhythm ----')[0].split('CAL = json')[0].replace('import engine_p30','import engine_p30'), globals()) if False else None
SECS_ORDER=["Verse 1","Chorus 1","Verse 2","Chorus 2","Bridge","Chorus 3"]
print(c["fp"], c["meas"]["composite"], c.get("plans",{}))
for s in SECS_ORDER:
    print("==",s)
    cur=None
    for o,d,p,x,i in c[s]:
        if i!=cur: print(f"  L{i+1}:", end=""); cur=i
        print(f" {x[0].upper() if x[2] else x[0]}:{NM[p%12]}{p//12-1}@{o%32 if True else o}/{d}", end="")
        if (o,d,p,x,i)==[n for n in c[s] if n[4]==i][-1]: print()
