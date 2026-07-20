# Hypothesis Test: Goals in Women's vs Men's FIFA World Cups

A formal statistical answer to a real sports-journalism question: are more goals scored in women's FIFA World Cup matches than in men's?

- **H0:** the mean number of goals is the same.
- **HA:** women's matches score more.
- **Test:** Mann-Whitney U (non-parametric, one-sided), alpha = 0.10.
- **Scope:** official World Cup matches since 2002 (no qualifiers), so era and tournament level are comparable.

The decision comes from the p-value, and the boxplot in `images/` shows the two distributions side by side.

**Data:** `women_results.csv` / `men_results.csv` from a DataCamp guided project (not redistributed here).

**Stack:** Python · Pandas · Pingouin · SciPy · Matplotlib
