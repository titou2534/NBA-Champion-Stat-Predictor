import pandas as pd, numpy as np
df=pd.read_csv('analysis/team_seasons.csv')
def cri(d):
    zs=lambda s,sg=1:(d[s]-d[s].mean())/d[s].std()*sg
    return zs('NRtg')+0.5*np.minimum(zs('ORtg'),zs('DRtg',-1))+0.25*zs('Age')
cur=df[df.Season==2027].set_index('Team'); prev=df[df.Season==2026].set_index('Team')
print('games played this season:', cur.G.min(), '-', cur.G.max())
w=cur.G/(cur.G+20)   # current-season data counts like G games vs a 20-game prior from last season
b=pd.DataFrame(index=cur.index)
for s in ['ORtg','DRtg']:
    # convert to league-relative so eras/seasons line up, then blend
    b[s]=w*(cur[s]-cur[s].mean())+(1-w)*(prev[s].reindex(cur.index)-prev[s].mean())
b['NRtg']=b.ORtg-b.DRtg; b['Age']=cur.Age
out=pd.DataFrame({'G':cur.G,'W':cur.W,'L':cur.L,'NRtg_now':cur.NRtg,'CRI_2026':cri(prev).reindex(cur.index),'CRI_now':cri(cur),'CRI_blend':cri(b)})
out=out.sort_values('CRI_blend',ascending=False).round(2)
out.to_csv('analysis/predictions_2027.csv')
print(out.head(12).to_string())
# title odds: softmax over teams, sharpness (1.85) fit by max likelihood on the 2007-2026 champions
out['TitlePct']=(100*np.exp(1.85*out.CRI_blend)/np.exp(1.85*out.CRI_blend).sum()).round(1)
out.to_csv('analysis/predictions_2027.csv')
print(out[['CRI_blend','TitlePct']].head(10).to_string())
