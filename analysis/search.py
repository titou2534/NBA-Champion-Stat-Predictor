import pandas as pd, numpy as np, itertools
df=pd.read_csv('analysis/team_seasons.csv'); df=df[df.Season.between(2006,2026)].copy()
df['ShotDiff']=df['eFG%']-df['oeFG%']; df['TOVDiff']=df['oTOV%']-df['TOV%']; df['RebDiff']=df['ORB%']+df['DRB%']-100
g=df.groupby('Season'); Z=lambda s,sg=1: g[s].transform(lambda x:(x-x.mean())/x.std())*sg
F={'NRtg':Z('NRtg'),'Shot':Z('ShotDiff'),'Bal':np.minimum(Z('ORtg'),Z('DRtg',-1)),'Age':Z('Age'),'AST':Z('AST'),'3P':Z('3P%'),'TOV':Z('TOVDiff'),'Reb':Z('RebDiff'),'Win':Z('WinPct')}
F=pd.DataFrame(F); seasons=sorted(df.Season.unique()); S=df.Season.values; C=df.Champion.values
grid=[0,0.25,0.5,1]
names=list(F.columns)
def score(w,mask):
    v=F.values@w; hits=0; rks=[]
    for s in seasons:
        if not mask(s): continue
        m=S==s; r=(-v[m]).argsort().argsort()[C[m]][0]+1; rks.append(r); hits+=r==1
    return hits,np.mean(rks)
# restrict to 5 features + NRtg anchor to keep the search small and honest
res=[]
for combo in itertools.product(grid,repeat=5):
    for extra in itertools.combinations(['AST','3P','TOV','Reb','Win'],0):
        pass
    w=np.zeros(len(names)); w[0]=1
    for k,n in zip(combo,['Shot','Bal','Age','AST','3P']): w[names.index(n)]=k
    h,a=score(w,lambda s:2007<=s<=2026); res.append((h,-a,tuple(w)))
res.sort(reverse=True)
for h,a,w in res[:8]: print(h,round(-a,2),dict((n,x) for n,x in zip(names,w) if x))
# leave-one-season-out: pick best weights on 19 seasons, test on held-out one
hits=0
for test in range(2007,2027):
    best=max(((score(np.array(w),lambda s:2007<=s<=2026 and s!=test)),w) for _,_,w in res)[1]
    h,_=score(np.array(best),lambda s:s==test); hits+=h
print('LOSO out-of-sample #1 hits:',hits,'/20')
