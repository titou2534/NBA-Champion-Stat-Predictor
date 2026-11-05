import pandas as pd, numpy as np
df=pd.read_csv('analysis/team_seasons.csv')
df['ShotDiff']=df['eFG%']-df['oeFG%']
g=df.groupby('Season')
def z(s,sign=1): return g[s].transform(lambda x:(x-x.mean())/x.std())*sign
df['zO']=z('ORtg'); df['zD']=z('DRtg',-1); df['zN']=z('NRtg'); df['zShot']=z('ShotDiff'); df['zAge']=z('Age'); df['zW']=z('WinPct')
cands={
 'NRtg only':           df.zN,
 'SRS only':            z('SRS'),
 'Win% only':           df.zW,
 'ShotDiff only':       df.zShot,
 'NRtg + balance':      df.zN + 0.5*np.minimum(df.zO,df.zD),
 'NRtg + ShotDiff':     df.zN + 0.5*df.zShot,
 'NRtg+bal+age':        df.zN + 0.5*np.minimum(df.zO,df.zD) + 0.25*df.zAge,
 'NRtg+shot+bal+age':   df.zN + 0.5*df.zShot + 0.5*np.minimum(df.zO,df.zD) + 0.25*df.zAge,
}
tr=df.Season.between(2007,2026)
for k,v in cands.items():
    r=v.groupby(df.Season).rank(ascending=False)[tr & df.Champion]
    print(f'{k:20s} #1:{(r==1).sum():2d}  top3:{(r<=3).sum():2d}  top5:{(r<=5).sum():2d}  avg:{r.mean():.2f}  worst:{int(r.max())}')
print('\nweight sensitivity (balance w, age w) -> top3 / top5 / avg rank')
for wb in (0.25,0.5,0.75,1.0):
    for wa in (0,0.15,0.25,0.4):
        v=df.zN+wb*np.minimum(df.zO,df.zD)+wa*df.zAge
        r=v.groupby(df.Season).rank(ascending=False)[tr&df.Champion]
        print(f'  bal={wb:.2f} age={wa:.2f}: {(r<=3).sum():2d} {(r<=5).sum():2d} {r.mean():.2f}')
v=df.zN+0.5*np.minimum(df.zO,df.zD)+0.25*df.zAge
df['CRI']=v
r=v.groupby(df.Season).rank(ascending=False)
print('\nholdout 2006 champion rank:', int(r[(df.Season==2006)&df.Champion].iloc[0]))
df['CRI_rank']=r
print(df[tr&df.Champion][['Season','Team','CRI','CRI_rank']].round(2).to_string(index=False))
print('\nwho was #1 when the champ was not:')
top=df[tr&(df.CRI_rank==1)&~df.Champion][['Season','Team']]; print(top.to_string(index=False))
