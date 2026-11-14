import pickle, sys, numpy as np, collections
sys.path.insert(0,"/home/claude/p58"); import luthier_judge4 as J4
for lab,p in (("B main","runl3/melody_l3p2_p58_main.pkl"),("B ctl","runl3/melody_l3p2_p58_ctl.pkl")):
    D=pickle.load(open(p,'rb')); v=[]
    for b in D['all']:
        ns=sorted([(o,pp,s) for o,d,pp,s,l,st,sy in b['notes']])
        B=J4.barlist(dict(t=np.array([n[0] for n in ns]),p=np.array([n[1] for n in ns]),sec=np.array([n[2] for n in ns])))
        v.append(np.mean([J4._M.so[x[1]]>0 for x in B]))
    print(lab, len(v), round(float(np.mean(v)),3))
