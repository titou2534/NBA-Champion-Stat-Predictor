import pandas as pd, numpy as np
df=pd.read_csv('analysis/team_seasons.csv')
def cri(d):
    z=lambda s,sg=1:(d[s]-d[s].mean())/d[s].std()*sg
    return z('NRtg')+0.5*np.minimum(z('ORtg'),z('DRtg',-1))+0.25*z('Age')
def vnr(d):
    z=lambda s:(d[s]-d[s].mean())/d[s].std()
    return z('NRtg')+0.25*z('Age')+0.25*z('AST')
for n,f in (('CRI',cri),('VNR',vnr)):
    df[n]=df.groupby('Season',group_keys=False).apply(f)
    df[n+'_rk']=df.groupby('Season')[n].rank(ascending=False).astype(int)
h=df[df.Season.between(2007,2026)&df.Champion]
for n in ('CRI','VNR'):
    r=h[n+'_rk']; print(f'{n}: #1 {(r==1).sum()}  top3 {(r<=3).sum()}  top5 {(r<=5).sum()}  avg {r.mean():.2f}  worst {r.max()}')
print(h[['Season','Team','CRI_rk','VNR_rk']].to_string(index=False))
cur=df[df.Season==2027].set_index('Team'); prev=df[df.Season==2026].set_index('Team')
w=cur.G/(cur.G+20); b=pd.DataFrame(index=cur.index)
for s in ['ORtg','DRtg','AST']: b[s]=w*(cur[s]-cur[s].mean())+(1-w)*(prev[s].reindex(cur.index)-prev[s].mean())
b['NRtg']=b.ORtg-b.DRtg; b['Age']=cur.Age
o=pd.DataFrame({'W':cur.W,'L':cur.L,'CRI':cri(b),'VNR':vnr(b)})
o['CRI_rk']=o.CRI.rank(ascending=False).astype(int); o['VNR_rk']=o.VNR.rank(ascending=False).astype(int)
print('\nG',cur.G.min(),'-',cur.G.max()); print(o.sort_values('CRI',ascending=False).round(2).head(9).to_string())
