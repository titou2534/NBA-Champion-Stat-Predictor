import re, io, pandas as pd
rows=[]
for y in range(2006,2028):
    h=open(f'raw/NBA_{y}.html').read().replace('<!--','').replace('-->','')
    champ=re.search(r'League Champion</strong>:\s*<a[^>]*>([^<]+)',h)
    def tbl(tid, header=0):
        m=re.search(rf'<table[^>]*id="{tid}".*?</table>',h,re.S)
        return pd.read_html(io.StringIO(m.group(0)),header=header)[0]
    adv=tbl('advanced-team',1)
    adv=adv[[c for c in adv.columns if not str(c).startswith('Unnamed')]]
    adv.columns=['Rk','Team','Age','W','L','PW','PL','MOV','SOS','SRS','ORtg','DRtg','NRtg','Pace','FTr','3PAr','TS%','eFG%','TOV%','ORB%','FT/FGA','oeFG%','oTOV%','DRB%','oFT/FGA','Arena','Attend','Attend/G'][:len(adv.columns)]
    adv=adv[adv.Team.notna() & (adv.Team!='League Average')]
    pg=tbl('per_game-team'); pg=pg[pg.Team.notna() & (pg.Team!='League Average')]
    adv['Team']=adv.Team.str.replace('*','',regex=False).str.strip()
    pg['Team']=pg.Team.str.replace('*','',regex=False).str.strip()
    d=adv.merge(pg[['Team','G','3P%','FG%','AST','STL','BLK','TOV']],on='Team')
    d['Season']=y; d['Champion']=(d.Team==champ.group(1)) if champ else False
    rows.append(d)
df=pd.concat(rows)
num=[c for c in df.columns if c not in('Team','Arena','Champion')]
df[num]=df[num].apply(pd.to_numeric,errors='coerce')
df['WinPct']=df.W/(df.W+df.L)
df.to_csv('analysis/team_seasons.csv',index=False)
print(df.groupby('Season').size().to_string()); print(df[df.Champion][['Season','Team','W','L','SRS','ORtg','DRtg','NRtg']].to_string())
