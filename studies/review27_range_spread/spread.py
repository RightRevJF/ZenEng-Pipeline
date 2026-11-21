import runpy,sys,os,numpy as np
import sys, os; os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')); sys.path[:0]=['lib/luthier','studies/words_to_shape']; __file__='studies/words_to_shape/study.py'
sys.argv=['x']; src=open('studies/words_to_shape/study.py').read().split('\n')
exec(compile('\n'.join(src[:21]),'studies/words_to_shape/study.py','exec'))
from sklearn.pipeline import make_pipeline; from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV; from sklearn.model_selection import GroupKFold
ci=(SHAPE+[CHECK]).index("range"); y=Y[:,ci]; p=np.zeros(len(y))
for tr,te in GroupKFold(5).split(X,y,G):
    m=make_pipeline(StandardScaler(),RidgeCV(alphas=np.logspace(-1,3,13))).fit(X[tr],y[tr]); p[te]=m.predict(X[te])
p=np.clip(p,12,26); e=y-p
print("n",len(y),"held-out resid sd",round(e.std(),2),"abs-error quartiles",np.round(np.percentile(abs(e),(25,50,75,90)),2))
print("share of kept songs within 2 of their held-out asking",round(float(np.mean(abs(e)<=2)),3))
for b in (3,4,5): print(" within",b,round(float(np.mean(abs(e)<=b)),3))
print("sd of the askings",round(p.std(),2),"of ranges",round(y.std(),2))
print("signed resid 10,25,50,75,90",np.round(np.percentile(e,(10,25,50,75,90)),2))
import json
asks={'55':18.0,'54':18.8,'58':19.9,'60':19.0,'59':18.8}; first={'55':17,'54':14,'58':11,'60':19,'59':19}; chose={'55':17,'54':17,'58':19,'60':19,'59':19}
for nm,d in (('872 alone',first),('951',chose)):
    r=np.array([d[k]-asks[k] for k in asks]); print(nm,'chosen-asking',np.round(r,1),'mean',round(r.mean(),2),'sd',round(r.std(),2))
