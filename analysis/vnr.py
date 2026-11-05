# Veteran Net Rating (VNR): net rating, nudged toward older rosters that share the ball
import pandas as pd, numpy as np
df=pd.read_csv('analysis/team_seasons.csv')
def vnr(d):
    z=lambda s:(d[s]-d[s].mean())/d[s].std()
    return z('NRtg')+0.25*z('Age')+0.25*z('AST')
df['VNR']=df.groupby('Season',group_keys=False).apply(vnr)
df['VNR_rk']=df.groupby('Season').VNR.rank(ascending=False).astype(int)
df['NRtg_rk']=df.groupby('Season').NRtg.rank(ascending=False,method='min').astype(int)
h=df[df.Season.between(2006,2026)]
ch=h[h.Champion].set_index('Season')[['Team','VNR_rk','NRtg_rk','W','NRtg']]
top=h[h.VNR_rk==1].set_index('Season')[['Team','W','NRtg']].add_prefix('VNR#1_')
print(ch.join(top).to_string())
print('champ #1 in VNR 2007-26:',(ch.loc[2007:].VNR_rk==1).sum(),'/20')
# 2026-27 with same 20-game prior blend as predict.py
cur=df[df.Season==2027].set_index('Team'); prev=df[df.Season==2026].set_index('Team')
w=cur.G/(cur.G+20); b=pd.DataFrame(index=cur.index)
for s in ['NRtg','AST']: b[s]=w*(cur[s]-cur[s].mean())+(1-w)*(prev[s].reindex(cur.index)-prev[s].mean())
b['Age']=cur.Age
print('\ngames played:',cur.G.min(),'-',cur.G.max())
print(pd.DataFrame({'W':cur.W,'L':cur.L,'NRtg_now':cur.NRtg,'VNR':vnr(b)}).sort_values('VNR',ascending=False).round(2).head(8).to_string())
