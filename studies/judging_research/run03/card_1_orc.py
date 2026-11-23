import numpy as np
from scipy.optimize import linprog
from scipy.sparse.csgraph import shortest_path

def w1(a,b,D):
    n=len(a); c=D.flatten()
    Aeq=[];beq=[]
    for i in range(n):
        r=np.zeros((n,n)); r[i,:]=1; Aeq.append(r.flatten()); beq.append(a[i])
    for j in range(n):
        r=np.zeros((n,n)); r[:,j]=1; Aeq.append(r.flatten()); beq.append(b[j])
    res=linprog(c,A_eq=np.array(Aeq),b_eq=beq,bounds=(0,None),method='highs')
    return res.fun

def analyse(name,W,labels,alpha=0.0):
    W=np.array(W,float); n=len(W)
    P=W/W.sum(1,keepdims=True)
    Pa=alpha*np.eye(n)+(1-alpha)*P
    A=((W+W.T)>0).astype(float); np.fill_diagonal(A,0)
    D=shortest_path(A,unweighted=True)
    kap={}
    for i in range(n):
        for j in range(n):
            if i<j:
                kap[(i,j)]=1-w1(Pa[i],Pa[j],D)/D[i,j]
    edges={k:v for k,v in kap.items() if D[k]==1}
    ev=np.sort(np.abs(np.linalg.eigvals(Pa)))[::-1]
    g=1-ev[1]
    print(f"{name} alpha={alpha}: edge kappas",{f'{labels[i]}-{labels[j]}':round(v,3) for (i,j),v in edges.items()})
    print(f"   min kappa(all pairs)={min(kap.values()):.3f} min edge={min(edges.values()):.3f} mean edge={np.mean(list(edges.values())):.3f}  gap g={g:.3f}")

# directed 3-cycle I->IV->V->I
C3=[[0,1,0],[0,0,1],[1,0,0]]
C4=[[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,0,0,0]]   # I->V->vi->IV->I
for a in [0,0.5]:
    analyse("directed 3-cycle",C3,["I","IV","V"],a)
    analyse("directed 4-cycle",C4,["I","V","vi","IV"],a)
# hub and spoke: I <-> each of IV,V,vi,ii
H=np.zeros((5,5)); H[0,1:]=1; H[1:,0]=1
for a in [0,0.5]:
    analyse("hub I + 4 spokes",H,["I","IV","V","vi","ii"],a)
# pop loop with a shortcut and a returning weight
S=[[0,3,0,1],[0,0,3,0],[0,0,0,3],[3,0,0,0]]
for a in [0,0.5]:
    analyse("4-loop + I->IV shortcut",S,["I","V","vi","IV"],a)
# complete graph K4 undirected
K=np.ones((4,4))-np.eye(4)
for a in [0,0.5]:
    analyse("all-to-all 4 chords",K,["I","IV","V","vi"],a)
