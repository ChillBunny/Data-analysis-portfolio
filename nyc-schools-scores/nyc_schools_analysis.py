# NYC public schools — SAT performance
#
# Three key questions from the brief: best math schools, top 10 by total SAT,
# and the borough with the largest spread in results — expanded with
# borough comparisons and score distributions.
# Data: schools.csv (included).

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

schools = pd.read_csv("schools.csv")

print("=== Dataset overview ===")
print(f"Schools: {schools.shape[0]} | Boroughs: {schools['borough'].nunique()}")

# --- 1. Best math schools (>= 80% of the 800 max) -----------------------------

best_math_schools = schools[["school_name", "average_math"]]
best_math_schools = best_math_schools[best_math_schools["average_math"] >= (800 * 0.8)]
best_math_schools = best_math_schools.sort_values(by="average_math", ascending=False)

print(f"\n=== Schools with average math >= 640 (80% of 800) ===")
print(best_math_schools.to_string(index=False))

plt.figure(figsize=(10, 6))
sns.barplot(x=best_math_schools["average_math"], y=best_math_schools["school_name"], palette="crest", hue=best_math_schools["school_name"], legend=False)
plt.title("NYC schools with average math score >= 640 (80% of 800)")
plt.xlabel("Average math score")
plt.ylabel("")
plt.xlim(600, 800)
plt.tight_layout()
plt.savefig("images/best_math_schools.png", dpi=150)
plt.close()

# --- 2. Top 10 schools by total SAT -------------------------------------------

schools["total_SAT"] = schools["average_math"] + schools["average_reading"] + schools["average_writing"]
top_10_schools = schools[["school_name", "total_SAT"]].sort_values(by="total_SAT", ascending=False)[:10]

print(f"\n=== Top 10 schools by total SAT ===")
print(top_10_schools.to_string(index=False))

plt.figure(figsize=(10, 6))
sns.barplot(x=top_10_schools["total_SAT"], y=top_10_schools["school_name"], palette="rocket", hue=top_10_schools["school_name"], legend=False)
plt.title("Top 10 NYC schools by total SAT score")
plt.xlabel("Total SAT (max 2400)")
plt.ylabel("")
plt.xlim(1800, 2200)
plt.tight_layout()
plt.savefig("images/top_10_schools.png", dpi=150)
plt.close()

# --- 3. Which borough has the largest spread (std) in results? ----------------

borough_stats = schools.groupby("borough")["total_SAT"].agg(["count", "mean", "std"]).round(2)
borough_stats = borough_stats.sort_values(by="std", ascending=False)
print(f"\n=== Borough statistics (total SAT) ===")
print(borough_stats)

largest = borough_stats.index[0]
largest_std_dev = pd.DataFrame({
    "borough": [largest],
    "num_schools": [int(borough_stats.loc[largest, "count"])],
    "average_SAT": [borough_stats.loc[largest, "mean"]],
    "std_SAT": [borough_stats.loc[largest, "std"]],
})
print(f"\nBorough with the largest spread:\n{largest_std_dev.to_string(index=False)}")

plt.figure(figsize=(9, 5))
sns.barplot(x=borough_stats.index, y=borough_stats["std"], palette="mako", hue=borough_stats.index, legend=False)
plt.title("Spread of total SAT scores by borough (standard deviation)")
plt.xlabel("")
plt.ylabel("Std of total SAT")
plt.tight_layout()
plt.savefig("images/borough_std.png", dpi=150)
plt.close()

# --- 4. Score distributions by borough ----------------------------------------

plt.figure(figsize=(10, 6))
sns.boxplot(data=schools, x="borough", y="total_SAT", palette="Set2", hue="borough", legend=False)
plt.title("Total SAT distribution by borough")
plt.xlabel("")
plt.ylabel("Total SAT")
plt.tight_layout()
plt.savefig("images/borough_distributions.png", dpi=150)
plt.close()

# --- 5. Are the three sections correlated? ------------------------------------

corr = schools[["average_math", "average_reading", "average_writing"]].corr().round(3)
print(f"\n=== Correlation between SAT sections ===")
print(corr)

plt.figure(figsize=(7, 5))
sns.heatmap(corr, annot=True, cmap="crest", vmin=0.9, vmax=1)
plt.title("Correlation between SAT sections")
plt.tight_layout()
plt.savefig("images/section_correlation.png", dpi=150)
plt.close()

print("\nCharts saved to images/")
