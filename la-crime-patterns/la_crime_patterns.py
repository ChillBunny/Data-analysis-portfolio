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

plt.figure(figsize=(9, 5))
sns.barplot(x=victim_ages.index, y=victim_ages.values, palette="ch:start=.2,rot=-.3", hue=victim_ages.index, legend=False)
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
sns.barplot(x=crimes_season.index, y=crimes_season.values, palette=season_palette, hue=crimes_season.index, legend=False)
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

top_weapons = crimes["Weapon Desc"].value_counts().head(8)
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

vict_sex = crimes["Vict Sex"].value_counts()
print(f"\nVictims by sex:\n{vict_sex}")

plt.figure(figsize=(7, 5))
sns.barplot(x=vict_sex.index, y=vict_sex.values, palette="Set2", hue=vict_sex.index, legend=False)
plt.title("Crime victims by sex (F: female, M: male, X: unknown)")
plt.xlabel("Victim sex")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/victims_by_sex.png", dpi=150)
plt.close()

print("\nCharts saved to images/")
