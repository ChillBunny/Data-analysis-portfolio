# Hypothesis test: are more goals scored in women's FIFA World Cup matches than men's?
#
# H0: mean goals in women's international matches = men's
# HA: mean goals in women's international matches > men's
# Significance level: 10% (alpha = 0.10)
#
# Scope: official FIFA World Cup matches (no qualifiers) since 2002-01-01.
# Data: women_results.csv / men_results.csv (DataCamp guided project, not redistributed).

import pandas as pd
import matplotlib.pyplot as plt
import pingouin as pg

women_results = pd.read_csv("women_results.csv")
men_results = pd.read_csv("men_results.csv")

# Filter to World Cup matches since 2002
women_results = women_results[women_results["tournament"] == "FIFA World Cup"]
men_results = men_results[men_results["tournament"] == "FIFA World Cup"]

women_results = women_results[women_results["date"] >= "2002-01-01"]
men_results = men_results[men_results["date"] >= "2002-01-01"]

# Total goals per match
women_results = women_results[["home_score", "away_score"]]
men_results = men_results[["home_score", "away_score"]]

women_results["total"] = women_results["home_score"] + women_results["away_score"]
men_results["total"] = men_results["home_score"] + men_results["away_score"]

# Descriptive statistics
women_mean, men_mean = women_results["total"].mean(), men_results["total"].mean()
women_std, men_std = women_results["total"].std(), men_results["total"].std()
women_n, men_n = len(women_results), len(men_results)

print("=== Descriptive statistics (goals per match) ===")
print(f"Women: n={women_n}, mean={women_mean:.2f}, std={women_std:.2f}")
print(f"Men:   n={men_n}, mean={men_mean:.2f}, std={men_std:.2f}\n")

# Goal distributions are not normal, so: Mann-Whitney U (non-parametric), one-sided
mwu_result = pg.mwu(x=women_results["total"], y=men_results["total"], alternative="greater")

# pingouin renamed the column across versions ('p-val' -> 'p_val'); support both
p_col = "p_val" if "p_val" in mwu_result.columns else "p-val"
p_val = float(mwu_result[p_col].iloc[0])

alpha = 0.1
if p_val < alpha:
    print("Reject H0: women's matches score significantly more goals.")
    result_dict = {"p_val": p_val, "result": "reject"}
else:
    print("Fail to reject H0: not enough evidence that women's matches score more goals.")
    result_dict = {"p_val": p_val, "result": "fail to reject"}

print(result_dict)

# Visual comparison of the two distributions
plt.figure(figsize=(8, 5))
plt.boxplot(
    [women_results["total"], men_results["total"]],
    tick_labels=["Women's World Cup", "Men's World Cup"],
)
plt.ylabel("Total goals per match")
plt.title("Goals per match: Women's vs Men's FIFA World Cups (2002+)")
plt.tight_layout()
plt.savefig("images/goals_distribution.png", dpi=150)
plt.show()
