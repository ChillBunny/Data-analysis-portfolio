# Hypothesis Test: Goals in Women's vs Men's FIFA World Cups

![A soccer pitch for an international match.](images/soccer-pitch.jpg)

> **Origin:** this was one of the final projects of my **Data Analyst course at DataCamp**, solved in DataLab. The original notebook is included ([`notebook.ipynb`](./notebook.ipynb)); `fifa_hypothesis_test.py` is the cleaned, runnable version.

## The brief

You're working as a sports journalist at a major online sports media company, specializing in soccer analysis and reporting. You've been watching both men's and women's international soccer matches for a number of years, and your gut instinct tells you that more goals are scored in women's international football matches than men's. This would make an interesting investigative article that your subscribers are bound to love, but you'll need to perform a valid statistical hypothesis test to be sure!

While scoping this project, you acknowledge that the sport has changed a lot over the years, and performances likely vary a lot depending on the tournament, so you decide to limit the data used in the analysis to only official `FIFA World Cup` matches (not including qualifiers) since `2002-01-01`.

You create two datasets containing the results of every official men's and women's international football match since the 19th century, which you scraped from a reliable online source. This data is stored in two CSV files: `women_results.csv` and `men_results.csv`.

The question you are trying to determine the answer to is:

> Are more goals scored in women's international soccer matches than men's?

You assume a **10% significance level**, and use the following null and alternative hypotheses:

- **H₀:** The mean number of goals scored in women's international soccer matches is the same as men's.
- **Hₐ:** The mean number of goals scored in women's international soccer matches is greater than men's.

## Method

1. Filter both datasets to official FIFA World Cup matches since 2002-01-01.
2. Compute total goals per match (home + away).
3. Goal counts are not normally distributed, so the right tool is the **Mann-Whitney U test** (non-parametric), one-sided, via `pingouin.mwu`.
4. Decide against **α = 0.10**.

## Results

```
=== Descriptive statistics (goals per match) ===
Women: n=200, mean=2.98, std=2.02
Men:   n=384, mean=2.51, std=1.65

Reject H0: women's matches score significantly more goals.
{'p_val': 0.0051, 'result': 'reject'}
```

**The verdict: p = 0.0051 < 0.10 → reject H₀.** The gut instinct was right, and now it's backed by statistics: women's FIFA World Cup matches score significantly more goals than men's (about half a goal more per match on average).

![Goals distribution](images/goals_distribution.png)

## Run it

```bash
pip install pandas matplotlib pingouin
python fifa_hypothesis_test.py
```

The boxplot is saved to `images/` automatically. Datasets (`women_results.csv`, `men_results.csv`) contain public international football results and are included.

**Stack:** Python · Pandas · Pingouin · SciPy · Matplotlib
