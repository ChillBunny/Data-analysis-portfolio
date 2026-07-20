# Crime Patterns in Los Angeles

Analysis of a large public crime dataset (LA Open Data) to support resource allocation: when crimes happen, where night crime concentrates, and which age groups are most affected.

Four answers:
1. **Peak crime hour** — parsed from 24h military time.
2. **Area with most night crime** (10pm-3:59am) — compound time filters.
3. **Victims by age group** — binning with `pd.cut` into 7 brackets.
4. **Crimes by season** — month-to-season binning.

Charts land in `images/`.

**Data:** `crimes.csv`, a modified version of the public Los Angeles Open Data set (DataCamp guided project, not redistributed here).

**Stack:** Python · Pandas · NumPy · Seaborn
