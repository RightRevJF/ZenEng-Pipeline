import pickle, sys
sys.argv=[sys.argv[0]]+sys.argv[1:]
NM=['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
R=pickle.load(open("melody_result.pkl","rb"))
k=int(sys.argv[1]) if len(sys.argv)>1 else 0
c=R["alive"][k]
import melody_p31 as M
print(c["fp"], c["meas"]); print(c["plans"])
for s in M.SINGS:
    print("==",s)
    for ln in M.SECS[s]:
        ns=[n for n in c[s] if n[4]==ln["idx"]]
        print(f"  L{ln['idx']+1} [{' '.join(b['chord'] for b in M.BARS if ln['at']<=b['start']<ln['at']+ln['n'])}]:", " ".join(f"{x[0].upper() if x[2] else x[0]}:{NM[p%12]}{p//12-1}@{o-ln['at']}/{d}" for o,d,p,x,i in ns))
