# Netflix Catalog — Exploratory Data Analysis

An EDA of the Netflix catalog built around a production-company brief: research movies from the 1990s.

Three views:
1. **Duration vs release year** — a 2D density plot showing how movie lengths shifted across decades.
2. **Genre output per year** — which genres dominate the catalog, year by year, since 1970.
3. **The 1990s question** — median duration in 1990 and a compound boolean filter counting short (<90 min) action movies of that decade.

Charts land in `images/`.

**Data:** `netflix_data.csv` from a DataCamp guided project (not redistributed here).

**Stack:** Python · Pandas · NumPy · Seaborn
