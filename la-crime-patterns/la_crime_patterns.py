# Crime patterns in Los Angeles — when, where and against whom
#
# Supporting the LAPD brief: peak crime hour, night-crime hotspots, victim age
# groups and seasonality — expanded with crime types, weapons and victim sex.
# Data: crimes.csv, a modified version of the public Los Angeles Open Data set (included).

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

crimes = pd.read_csv(
    "crimes.csv",
    parse_dates=["Date Rptd", "DATE OCC"],
    dtype={"TIME OCC": str},
)

print("=== Dataset overview ===")
print(f"Records: {crimes.shape[0]:,} | Columns: {crimes.shape[1]}")
print(f"Period of occurrence: {crimes['DATE OCC'].min().date()} - {crimes['DATE OCC'].max().date()}")

# --- 1. Peak crime hour -------------------------------------------------------

crimes["TIME OCC HOUR"] = crimes["TIME OCC"].str.slice(0, 2).astype(int)
crimes_hours = crimes["TIME OCC HOUR"].value_counts().sort_index()
peak_crime_hour = crimes_hours.idxmax()
print(f"\nPeak crime hour: {peak_crime_hour}:00")

plt.figure(figsize=(11, 5))
sns.barplot(x=crimes_hours.index, y=crimes_hours.values, color="#2C4E80")
plt.title("Crimes by hour of day")
plt.xlabel("Hour (24h)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/crimes_by_hour.png", dpi=150)
plt.close()

# --- 2. Night crime hotspots (10pm-3:59am) ------------------------------------

night_crimes = crimes[(crimes["TIME OCC HOUR"] >= 22) | (crimes["TIME OCC HOUR"] < 4)]
night_crime_by_area = night_crimes["AREA NAME"].value_counts()
peak_night_crime_location = night_crime_by_area.idxmax()
print(f"Area with most night crime: {peak_night_crime_location}")

top_night = night_crime_by_area.head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_night.values, y=top_night.index, palette="mako", hue=top_night.index, legend=False)
plt.title("Top 10 areas by night crime (10pm-3:59am)")
plt.xlabel("Night crimes")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/night_crime_areas.png", dpi=150)
plt.close()

# --- 3. Victims by age group --------------------------------------------------

crimes["Vict Age Label"] = pd.cut(
    crimes["Vict Age"],
    bins=[0, 17, 25, 34, 44, 54, 64, np.inf],
    labels=["0-17", "18-25", "26-34", "35-44", "45-54", "55-64", "65+"],
)
victim_ages = crimes.groupby("Vict Age Label", observed=False)["Vict Age"].count()
print(f"\nVictims by age group:\n{victim_ages}")

plt.figure(figsize=(10, 6))
age_colors = sns.color_palette("ch:start=.2,rot=-.3", n_colors=len(victim_ages))
plt.bar(victim_ages.index.astype(str), victim_ages.values, color=age_colors, width=0.7)
plt.title("Crime victims by age group")
plt.xlabel("Age group")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/victims_by_age.png", dpi=150)
plt.close()

# --- 4. Crimes by season ------------------------------------------------------

crimes["DATE OCC Month"] = crimes["DATE OCC"].dt.month
crimes["Season"] = pd.cut(
    crimes["DATE OCC Month"],
    bins=[1, 4, 7, 10, 12],
    labels=["Spring", "Summer", "Fall", "Winter"],
    right=False,
)
crimes_season = crimes["Season"].value_counts()
print(f"\nCrimes by season:\n{crimes_season}")

plt.figure(figsize=(8, 5))
season_palette = {"Spring": "tab:green", "Summer": "tab:red", "Fall": "tab:orange", "Winter": "tab:blue"}
season_colors = [season_palette[s] for s in crimes_season.index]
plt.bar(crimes_season.index.astype(str), crimes_season.values, color=season_colors, width=0.6)
plt.title("Crimes by season")
plt.xlabel("Season")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/crimes_by_season.png", dpi=150)
plt.close()

# --- 5. What crimes? Top 10 crime types ---------------------------------------

top_crimes = crimes["Crm Cd Desc"].value_counts().head(10)
print(f"\nTop 10 crime types:\n{top_crimes}")

plt.figure(figsize=(11, 6))
sns.barplot(x=top_crimes.values, y=top_crimes.index, palette="rocket", hue=top_crimes.index, legend=False)
plt.title("Top 10 crime types in Los Angeles")
plt.xlabel("Reports")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/top_crime_types.png", dpi=150)
plt.close()

# --- 6. Weapons: what's actually used -----------------------------------------

# Label cleanup: the raw LAPD categories come with typos like "6INCHES"
crimes["Weapon Desc Clean"] = crimes["Weapon Desc"].str.replace("6INCHES", "6 INCHES", regex=False)
top_weapons = crimes["Weapon Desc Clean"].value_counts().head(8)
print(f"\nTop 8 weapons (when reported):\n{top_weapons}")

plt.figure(figsize=(11, 5))
sns.barplot(x=top_weapons.values, y=top_weapons.index, palette="flare", hue=top_weapons.index, legend=False)
plt.title("Most common weapons (when a weapon is reported)")
plt.xlabel("Reports")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/top_weapons.png", dpi=150)
plt.close()

# --- 7. Victim sex ------------------------------------------------------------
# Data-quality note: the dictionary only defines F, M and X. A handful of records
# carry other codes (e.g. 'H') — invalid entries, excluded from the chart.

vict_sex_raw = crimes["Vict Sex"].value_counts()
invalid_sex = vict_sex_raw[~vict_sex_raw.index.isin(["F", "M", "X"])]
if len(invalid_sex) > 0:
    print(f"\nData-quality note — invalid sex codes excluded: {invalid_sex.to_dict()}")

vict_sex = vict_sex_raw[vict_sex_raw.index.isin(["F", "M", "X"])]
print(f"\nVictims by sex (valid codes):\n{vict_sex}")

plt.figure(figsize=(7, 5))
sex_colors = sns.color_palette("Set2", n_colors=len(vict_sex))
plt.bar(vict_sex.index.astype(str), vict_sex.values, color=sex_colors, width=0.6)
plt.title("Crime victims by sex (F: female, M: male, X: unknown)")
plt.xlabel("Victim sex")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/victims_by_sex.png", dpi=150)
plt.close()

# --- 8. Victims per capita: weighting by population share ----------------------
# Raw counts are nearly even, but do men and women face the same RISK relative
# to their population size? Weighting by the City of LA population
# (U.S. Census 2020: ~3,898,747 residents; ~50.4% female, ~49.6% male).
# "X: unknown" cannot be weighted — there is no census baseline for "unknown".

LA_POP_TOTAL = 3_898_747
LA_POP_F = round(LA_POP_TOTAL * 0.504)
LA_POP_M = round(LA_POP_TOTAL * 0.496)

per_capita = pd.Series({
    "M": vict_sex["M"] / LA_POP_M * 100_000,
    "F": vict_sex["F"] / LA_POP_F * 100_000,
})
print(f"\nVictims per 100,000 residents (2020-2023 reports, Census 2020 population):")
print(per_capita.round(0))
print(f"Men face {(per_capita['M'] / per_capita['F'] - 1) * 100:.1f}% more victimization per capita than women.")

plt.figure(figsize=(7, 5))
bars = plt.bar(per_capita.index.astype(str), per_capita.values, color=sex_colors[:2][::-1], width=0.5)
for bar, value in zip(bars, per_capita.values):
    plt.text(bar.get_x() + bar.get_width() / 2, value + 40, f"{value:,.0f}", ha="center", fontweight="bold")
plt.suptitle("Victims per 100,000 residents, by sex", fontsize=13, y=0.97)
plt.title("Weighted by each sex's share of LA's population (Census 2020). X excluded: no census baseline for 'unknown'.",
          fontsize=8, color="#555555", pad=12)
plt.xlabel("Victim sex")
plt.ylabel("Victims per 100,000 residents")
plt.tight_layout(rect=[0, 0, 1, 0.94])
plt.savefig("images/victims_per_capita.png", dpi=150)
plt.close()

print("\nCharts saved to images/")
