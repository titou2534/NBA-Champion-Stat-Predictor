import pandas as pd, numpy as np
df=pd.read_csv('analysis/team_seasons.csv'); df=df[df.Season.between(2007,2026)]
lower_better={'DRtg','TOV%','oeFG%','oFT/FGA','TOV','Age'}
stats=['NRtg','SRS','MOV','WinPct','ORtg','DRtg','TS%','eFG%','oeFG%','TOV%','oTOV%','ORB%','DRB%','FTr','FT/FGA','oFT/FGA','3PAr','3P%','AST','STL','BLK','Pace','Age','SOS']
out=[]
for s in stats:
    asc = s in lower_better
    r=df.groupby('Season')[s].rank(ascending=asc,method='min')
    z=df.groupby('Season')[s].transform(lambda x:(x-x.mean())/x.std()) * (-1 if asc else 1)
    c=df.Champion
    out.append((s, r[c].mean(), r[c].median(), r[c].max(), (r[c]<=5).sum(), (r[c]<=10).sum(), z[c].mean(), z[c].min()))
t=pd.DataFrame(out,columns=['stat','avgRank','medRank','worstRank','top5','top10','avgZ','minZ']).sort_values('avgZ',ascending=False)
print(t.round(2).to_string(index=False))
# per-champion ranks on key stats
for s in ['NRtg','ORtg','DRtg']:
    df[s+'_rk']=df.groupby('Season')[s].rank(ascending=(s=='DRtg'),method='min').astype(int)
print(df[df.Champion][['Season','Team','NRtg_rk','ORtg_rk','DRtg_rk']].to_string(index=False))
