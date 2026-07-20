# Netflix catalog — exploratory data analysis
#
# Built around a production-company brief: research movies from the 1990s.
# Expanded EDA: catalog structure, genres, countries, durations across decades,
# and a focused look at that nostalgic movie decade.
# Data: netflix_data.csv (included).

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

netflix_df = pd.read_csv("netflix_data.csv")

# --- 0. What are we working with? --------------------------------------------

print("=== Dataset overview ===")
print(f"Rows: {netflix_df.shape[0]:,} | Columns: {netflix_df.shape[1]}")
print(f"\nTitles by type:\n{netflix_df['type'].value_counts()}")
print(f"\nRelease years: {netflix_df['release_year'].min()} - {netflix_df['release_year'].max()}")

# --- 1. Duration vs release year (density) -----------------------------------

plt.figure(figsize=(10, 6))
sns.kdeplot(
    data=netflix_df,
    x="release_year",
    y="duration",
    fill=True,
    bw_method=0.26,
    cut=0,
)
plt.title("Movie duration by release year")
plt.xlabel("Release year")
plt.ylabel("Duration (minutes)")
plt.ylim(0, 200)
plt.tight_layout()
plt.savefig("images/duration_by_year.png", dpi=150)
plt.close()

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
plt.close()

# --- 3. Top genres in the catalog --------------------------------------------

genre_counts = netflix_df["genre"].value_counts().head(10)
print(f"\n=== Top 10 genres ===\n{genre_counts}")

plt.figure(figsize=(10, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette="flare", hue=genre_counts.index, legend=False)
plt.title("Top 10 genres in the Netflix catalog")
plt.xlabel("Number of titles")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/top_genres.png", dpi=150)
plt.close()

# --- 4. Top producing countries ----------------------------------------------

country_counts = netflix_df["country"].value_counts().head(10)
print(f"\n=== Top 10 producing countries ===\n{country_counts}")

plt.figure(figsize=(10, 6))
sns.barplot(x=country_counts.values, y=country_counts.index, palette="crest", hue=country_counts.index, legend=False)
plt.title("Top 10 producing countries on Netflix")
plt.xlabel("Number of titles")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/top_countries.png", dpi=150)
plt.close()

# --- 5. Releases per year: how the catalog grew ------------------------------

# The final year of the catalog (2021) is incomplete — cutting it so the
# curve doesn't crash to zero and mislead the reader.
releases_per_year = netflix_df["release_year"].value_counts().sort_index()
releases_per_year = releases_per_year[releases_per_year.index <= 2020]

plt.figure(figsize=(11, 5))
plt.fill_between(releases_per_year.index, releases_per_year.values, color="#B81D24", alpha=0.35)
plt.plot(releases_per_year.index, releases_per_year.values, color="#B81D24")
plt.title("Titles in the catalog by release year (1942-2020; 2021 cut as an incomplete year)")
plt.xlabel("Release year")
plt.ylabel("Number of titles")
plt.tight_layout()
plt.savefig("images/releases_per_year.png", dpi=150)
plt.close()

# --- 6. Movie duration by genre (whole catalog) ------------------------------

top6_genres = netflix_df["genre"].value_counts().head(6).index
movies_top_genres = netflix_df[(netflix_df["type"] == "Movie") & (netflix_df["genre"].isin(top6_genres))]

sample_min, sample_max = movies_top_genres["release_year"].min(), movies_top_genres["release_year"].max()
plt.figure(figsize=(11, 6))
sns.boxplot(data=movies_top_genres, x="genre", y="duration", palette="Set2", hue="genre", legend=False)
plt.title(f"Movie duration by genre (top 6 genres, all movies {sample_min}-{sample_max})")
plt.xlabel("")
plt.ylabel("Duration (minutes)")
plt.tight_layout()
plt.savefig("images/duration_by_genre.png", dpi=150)
plt.close()

print("\nMedian duration by genre (top 6):")
print(movies_top_genres.groupby("genre", observed=True)["duration"].median().sort_values(ascending=False))

# --- 7. The 1990s: the decade the brief asked about --------------------------

movies_90s = netflix_df[
    (netflix_df["release_year"] >= 1990)
    & (netflix_df["release_year"] < 2000)
    & (netflix_df["type"] == "Movie")
]

# Median duration of movies released in 1990
release_year_1990 = netflix_df["release_year"] == 1990
duration = int(np.median(netflix_df[release_year_1990]["duration"]))
print(f"\n=== The 1990s ===")
print(f"Movies from the 1990s in the catalog: {len(movies_90s)}")
print(f"Median duration of 1990 movies: {duration} min")

# Short (<90 min) action movies of the decade
short_movie_1990 = (
    (netflix_df["release_year"] >= 1990)
    & (netflix_df["release_year"] < 2000)
    & (netflix_df["type"] == "Movie")
    & (netflix_df["duration"] < 90)
    & (netflix_df["genre"] == "Action")
)
short_movie_count = len(netflix_df[short_movie_1990])
print(f"Short (<90 min) action movies from the 1990s: {short_movie_count}")

# Duration distribution of 1990s movies, with the 1990 median as reference
plt.figure(figsize=(10, 6))
sns.histplot(movies_90s["duration"], bins=30, color="#B81D24")
plt.axvline(duration, color="black", linestyle="--", label=f"1990 median: {duration} min")
plt.title("Duration of 1990s movies on Netflix")
plt.xlabel("Duration (minutes)")
plt.ylabel("Number of movies")
plt.legend()
plt.tight_layout()
plt.savefig("images/nineties_durations.png", dpi=150)
plt.close()

# Top genres of the decade
genres_90s = movies_90s["genre"].value_counts().head(8)
print(f"\nTop genres of the 1990s:\n{genres_90s}")

plt.figure(figsize=(10, 5))
sns.barplot(x=genres_90s.values, y=genres_90s.index, palette="rocket", hue=genres_90s.index, legend=False)
plt.title("Top genres of 1990s movies on Netflix")
plt.xlabel("Number of movies")
plt.ylabel("")
plt.tight_layout()
plt.savefig("images/nineties_genres.png", dpi=150)
plt.close()

print("\nCharts saved to images/")
