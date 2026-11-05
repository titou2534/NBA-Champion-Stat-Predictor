import pandas as pd, numpy as np, itertools
df=pd.read_csv('analysis/team_seasons.csv'); df=df[df.Season.between(2007,2026)].copy()
# derived "differential" stats (team minus opponent) - four-factor style
df['ShotDiff']=df['eFG%']-df['oeFG%']
df['TOVDiff']=df['oTOV%']-df['TOV%']
df['RebDiff']=df['ORB%']+df['DRB%']-100
df['FTDiff']=df['FT/FGA']-df['oFT/FGA']
df['PythW']=df.PW/(df.PW+df.PL)
lower={'DRtg','TOV%','oeFG%','oFT/FGA','Age'}
stats=['WinPct','PythW','NRtg','SRS','MOV','ORtg','DRtg','eFG%','TS%','oeFG%','ShotDiff','TOVDiff','RebDiff','FTDiff','3P%','AST','Age']
rows=[]
for s in stats:
    r=df.groupby('Season')[s].rank(ascending=s in lower,method='min')
    # also rank within conference isn't in the data; league-wide only
    rows.append((s,(r[df.Champion]==1).sum(),(r[df.Champion]<=2).sum(),(r[df.Champion]<=3).sum()))
print(pd.DataFrame(rows,columns=['stat','#1','top2','top3']).sort_values('#1',ascending=False).to_string(index=False))
