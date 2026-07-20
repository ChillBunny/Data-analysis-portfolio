# Visualizing the history of Nobel Prize winners (1901-2023)
#
# Who wins, where they're born, how female representation evolved by decade and
# category, the first woman laureate, and the repeat winners.
# Data: nobel.csv from the Nobel Prize API (included).

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

nobel = pd.read_csv("nobel.csv")

print("=== Dataset overview ===")
print(f"Prizes: {nobel.shape[0]:,} | Years: {nobel['year'].min()}-{nobel['year'].max()}")

# --- 1. Most awarded gender and birth country ---------------------------------

top_gender = nobel["sex"].value_counts().index[0]
top_country = nobel["birth_country"].value_counts().index[0]
print(f"\nMost awarded gender: {top_gender}")
print(f"Most common birth country: {top_country}")

country_counts = nobel["birth_country"].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=country_counts.values, y=country_counts.index, palette="crest", hue=country_counts.index, legend=False)
plt.title("Top 10 birth countries of Nobel laureates (1901-2023)")
plt.xlabel("Laureates")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/top_countries.png", dpi=150)
plt.close()

# --- 2. Decade with the highest RATIO of US-born winners ----------------------
# (ratio of US-born to total winners per decade, not absolute counts)

nobel["decade"] = (np.floor(nobel["year"] / 10) * 10).astype(int)
nobel["us_born"] = nobel["birth_country"] == "United States of America"
us_ratio = nobel.groupby("decade")["us_born"].mean()
max_decade_usa = int(us_ratio.idxmax())
print(f"\nDecade with highest ratio of US-born winners: {max_decade_usa}s "
      f"({us_ratio.max():.1%} of that decade's laureates)")

plt.figure(figsize=(10, 5))
sns.barplot(x=us_ratio.index, y=us_ratio.values, color="#2C4E80")
plt.title("Share of US-born Nobel laureates per decade")
plt.xlabel("Decade")
plt.ylabel("US-born ratio")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("images/us_ratio_by_decade.png", dpi=150)
plt.close()

# --- 3. Decade + category with the highest proportion of female laureates -----

nobel["female_winner"] = nobel["sex"] == "Female"
prop_female = nobel.groupby(["decade", "category"], as_index=False)["female_winner"].mean()

max_row = prop_female[prop_female["female_winner"] == prop_female["female_winner"].max()]
max_female_dict = {int(max_row["decade"].values[0]): max_row["category"].values[0]}
print(f"\nDecade+category with highest female proportion: {max_female_dict} "
      f"({float(max_row['female_winner'].values[0]):.1%})")

# Heatmap: female share per decade and category
heat = prop_female.pivot(index="category", columns="decade", values="female_winner")
plt.figure(figsize=(12, 5))
sns.heatmap(heat, annot=True, fmt=".0%", cmap="RdPu", cbar_kws={"label": "Female share"})
plt.title("Female share of Nobel laureates by decade and category")
plt.xlabel("Decade")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/female_share_heatmap.png", dpi=150)
plt.close()

# Overall female share per decade (trend line)
female_by_decade = nobel.groupby("decade")["female_winner"].mean()
plt.figure(figsize=(10, 5))
plt.plot(female_by_decade.index, female_by_decade.values, marker="o", color="#B03A66")
plt.title("Female share of Nobel laureates per decade (all categories)")
plt.xlabel("Decade")
plt.ylabel("Female share")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("images/female_share_trend.png", dpi=150)
plt.close()

# --- 4. First woman to receive a Nobel Prize ----------------------------------

first_woman = nobel[nobel["sex"] == "Female"].sort_values("year").iloc[0]
print(f"\nFirst female laureate: {first_woman['full_name']} "
      f"({first_woman['category']}, {first_woman['year']})")

# --- 5. Repeat winners --------------------------------------------------------

names = nobel["full_name"]
repeat_list = names[names.duplicated(keep=False)].drop_duplicates().to_list()
print(f"\nIndividuals or organizations with more than one Nobel Prize ({len(repeat_list)}):")
for name in repeat_list:
    print(f"  - {name}")

print("\nCharts saved to images/")
