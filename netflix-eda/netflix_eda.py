# Netflix catalog — exploratory data analysis
#
# Three views of the catalog: movie durations across release years, how many
# titles each genre gets per year, and a filtered look at short 1990s action movies.
# Data: netflix_data.csv (DataCamp guided project, not redistributed).

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

netflix_df = pd.read_csv("netflix_data.csv")

# --- 1. Duration vs release year (density) -----------------------------------

sns.kdeplot(
    data=netflix_df,
    x="release_year",
    y="duration",
    shade=True,
    bw_method=0.26,
    cut=0,
)
plt.title("Movie duration by release year")
plt.xlabel("Release year")
plt.ylabel("Duration (minutes)")
plt.ylim(0, 200)
plt.tight_layout()
plt.savefig("images/duration_by_year.png", dpi=150)
plt.show()

# --- 2. Titles per genre per year (1970+) ------------------------------------

grouped_df = (
    netflix_df[["release_year", "genre"]]
    .groupby(["release_year", "genre"])
    .value_counts()
    .reset_index(name="title_count")
)

plt.figure(figsize=(12, 7))
sns.scatterplot(
    data=grouped_df[grouped_df["release_year"] >= 1970],
    x="release_year",
    y="genre",
    hue="title_count",
    size="title_count",
    palette="hls",
)
plt.title("Titles per genre per year on Netflix")
plt.xlabel("Release year")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/genre_by_year.png", dpi=150)
plt.show()

# --- 3. The 1990s question: short action movies ------------------------------

# Median duration of movies released in 1990
release_year_1990 = netflix_df["release_year"] == 1990
duration = int(np.median(netflix_df[release_year_1990]["duration"]))
print(f"Median duration of 1990 movies: {duration} min")

# How many 1990s action movies run under 90 minutes?
short_movie_1990 = (
    (netflix_df["release_year"] >= 1990)
    & (netflix_df["release_year"] < 2000)
    & (netflix_df["type"] == "Movie")
    & (netflix_df["duration"] < 90)
    & (netflix_df["genre"] == "Action")
)
short_movie_count = len(netflix_df[short_movie_1990])
print(f"Short (<90 min) action movies from the 1990s: {short_movie_count}")
