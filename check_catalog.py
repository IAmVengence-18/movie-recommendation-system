import json
from collections import Counter
import os

FILE_PATH = "data/raw/discovered_movies.json"

with open(FILE_PATH, "r", encoding="utf-8") as file:
    movies = json.load(file)

print(f"Total records: {len(movies)}")

# Movie IDs
movie_ids = [movie.get("id") for movie in movies]

unique_ids = set(movie_ids)

def remove_duplicates(movies):
    unique_movies = {}
    
    for movie in movies:
        movie_id = movie.get("id")

        if movie_id not in unique_movies:
            unique_movies[movie_id] = movie

    return list(unique_movies.values())

clean_movies = remove_duplicates(movies)
print(f"\nAfter removing duplicates: {len(clean_movies)} movies")

def save_clean_catalog(movies):
    os.makedirs("data/processed", exist_ok=True)

    with open(
        "data/processed/movies_catalog.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            movies,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(
        f"Clean catalog saved: "
        f"{len(movies)} unique movies"
    )

save_clean_catalog(clean_movies)