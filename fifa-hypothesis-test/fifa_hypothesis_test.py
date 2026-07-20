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

# Goal distributions are not normal, so: Mann-Whitney U (non-parametric), one-sided
p_value = pg.mwu(x=women_results["total"], y=men_results["total"], alternative="greater")

alpha = 0.1
if p_value["p-val"][0] < alpha:
    print("Reject H0: women's matches score significantly more goals.")
    result_dict = {"p_val": p_value["p-val"][0], "result": "reject"}
else:
    print("Fail to reject H0: not enough evidence that women's matches score more goals.")
    result_dict = {"p_val": p_value["p-val"][0], "result": "fail to reject"}

print(result_dict)

# Visual comparison of the two distributions
plt.figure(figsize=(8, 5))
plt.boxplot(
    [women_results["total"], men_results["total"]],
    labels=["Women's World Cup", "Men's World Cup"],
)
plt.ylabel("Total goals per match")
plt.title("Goals per match: Women's vs Men's FIFA World Cups (2002+)")
plt.tight_layout()
plt.savefig("images/goals_distribution.png", dpi=150)
plt.show()
