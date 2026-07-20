# Crime patterns in Los Angeles — when, where and against whom
#
# Supporting the LAPD brief: find the peak crime hour, the area with most night
# crime, victim age groups, and the season with most incidents.
# Data: crimes.csv, a modified version of the public Los Angeles Open Data set
# (DataCamp guided project, not redistributed).

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

crimes = pd.read_csv(
    "crimes.csv",
    parse_dates=["Date Rptd", "DATE OCC"],
    dtype={"TIME OCC": str},
)

# --- 1. Peak crime hour -------------------------------------------------------

crimes["TIME OCC HOUR"] = crimes["TIME OCC"].str.slice(0, 2).astype(int)
crimes_hours = crimes["TIME OCC HOUR"].value_counts().sort_index()
peak_crime_hour = crimes_hours.idxmax()
print(f"Peak crime hour: {peak_crime_hour}:00")

sns.barplot(x=crimes_hours.index, y=crimes_hours.values)
plt.title("Crimes by hour of day")
plt.xlabel("Hour (24h)")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/crimes_by_hour.png", dpi=150)
plt.show()

# --- 2. Area with most night crime (10pm-3:59am) ------------------------------

night_crimes = crimes[(crimes["TIME OCC HOUR"] >= 22) | (crimes["TIME OCC HOUR"] < 4)]
night_crime_by_area = night_crimes.value_counts("AREA NAME").sort_index()
peak_night_crime_location = night_crime_by_area.idxmax()
print(f"Area with most night crime: {peak_night_crime_location}")

# --- 3. Victims by age group --------------------------------------------------

crimes["Vict Age Label"] = pd.cut(
    crimes["Vict Age"],
    bins=[0, 17, 25, 34, 44, 54, 64, np.inf],
    labels=["0-17", "18-25", "26-34", "35-44", "45-54", "55-64", "65+"],
)
victim_ages = crimes.groupby("Vict Age Label")["Vict Age"].count()
print(victim_ages)

sns.barplot(x=victim_ages.index, y=victim_ages.values, palette="ch:start=.2,rot=-.3")
plt.title("Crime victims by age group")
plt.xlabel("Age group")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/victims_by_age.png", dpi=150)
plt.show()

# --- 4. Crimes by season ------------------------------------------------------

crimes["DATE OCC Month"] = crimes["DATE OCC"].dt.month
crimes["Season"] = pd.cut(
    crimes["DATE OCC Month"],
    bins=[1, 4, 7, 10, 12],
    labels=["Spring", "Summer", "Fall", "Winter"],
    right=False,
)
crimes_season = crimes.value_counts("Season")
print(crimes_season)

sns.barplot(x=crimes_season.index, y=crimes_season.values)
plt.title("Crimes by season")
plt.xlabel("Season")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("images/crimes_by_season.png", dpi=150)
plt.show()
