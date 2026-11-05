# NBA Champion Predictor

Can 20 years of NBA regular-season team stats predict the champion? This project finds what the
2006-07 to 2025-26 champions have in common and builds two metrics from team stats only.

## Findings
- Every champion ranked top 8 in net rating; 18 of 20 were top 11 on both offense and defense.
- Champions skew toward the oldest rosters. Pace, 3-point volume and free-throw rate tell you almost nothing.

## Metrics
All stats are z-scored within their own season so different eras compare fairly.

| Metric | Formula | Champion #1 | Top 3 | Top 5 |
|---|---|---|---|---|
| **CRI** (Championship Readiness Index) | z(NRtg) + 0.5·min(z(ORtg), z(DRtg)) + 0.25·z(Age) | 8/20 | 16/20 | 20/20 |
| **VNR** (Veteran Net Rating) | z(NRtg) + 0.25·z(Age) + 0.25·z(AST) | 11/20 | 18/20 | 19/20 |

- **CRI** is the contender filter: every champion scored ≥ ~1.0 and ranked top 5.
- **VNR** was chosen by searching for the mix that ranks the most champions #1. Leave-one-season-out
  validation gets 7/20, the same as plain net rating, so treat it as descriptive.
- In at least 7 of VNR's 9 misses, the favourite had a key injury or the champion's regular season was
  depressed by rest/missed games.

## Current season
Current-season stats are blended with last season's (last season counts as a 20-game prior).
CRI is converted to title odds with a softmax whose sharpness (1.85) is fit on past champions.

## Usage
```bash
mkdir -p raw && for y in $(seq 2006 2027); do curl -s -A "Mozilla/5.0" -o raw/NBA_$y.html https://www.basketball-reference.com/leagues/NBA_$y.html; sleep 4; done
python3 analysis/build.py      # -> analysis/team_seasons.csv
python3 analysis/compare.py    # CRI vs VNR, history + current season
```

| Script | Purpose |
|---|---|
| `build.py` | Parse season pages into `team_seasons.csv` |
| `explore.py` | Champion rank on 24 stats |
| `metric.py` | CRI backtest and weight sensitivity |
| `predict.py` | CRI title odds -> `predictions_2027.csv` |
| `number_one.py`, `search.py` | Single-stat #1 counts, combo search, leave-one-season-out check |
| `vnr.py` | VNR history, outliers, current scores |
| `compare.py` | Both metrics side by side |

Data: [Basketball-Reference](https://www.basketball-reference.com). Requires Python 3 with pandas and lxml.
