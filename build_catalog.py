import os
import time
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY") 
BASE_URL = "https://api.themoviedb.org/3"

def make_request(client, url, params, retries=3):
    """Executes requests reusing the connection session."""
    for attempt in range(retries):
        try:
            response = client.get(url, params=params)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            print(f"HTTP Status Error {e.response.status_code} on attempt {attempt + 1}")
            if e.response.status_code == 401:
                print("Validation Failed: Ensure your env variable holds the long Access Token.")
            if attempt == retries - 1:
                raise

        except httpx.RequestError as e:
            print(f"Network glitch caught (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(2)
            else:
                raise

def discover_movies(client, page):
    url = f"{BASE_URL}/discover/movie"
    
    params = {
        "page": page,
        "vote_count.gte": 1000
    }
    return make_request(client, url, params)

def get_movie_details(client, movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"

    params = {}

    return make_request(client, url, params)

def get_movie_credits(client, movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/credits"

    params = {}

    return make_request(client, url, params)

def get_movie_keywords(client, movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/keywords"

    params = {}

    return make_request(client, url, params)

def get_movie_data(client, movie_id):
    details = get_movie_details(client, movie_id)
    credits = get_movie_credits(client, movie_id)
    keywords_data = get_movie_keywords(client, movie_id)

    director = None
    cast=[]
    keywords=[]
    genres=[]

    for crew in credits.get('crew', []):
        if crew.get('job')=='Director':
            director=crew.get('name')
            break
    
    cast=[actor.get('name') for actor in credits.get('cast', [])[:5]]

    keywords=[keyword.get('name') for keyword in keywords_data.get('keywords', [])]

    genres=[genre.get('name') for genre in details.get('genres', [])]

    return {
        "Title": details.get("title"),
        "Overview": details.get("overview"),
        "Release Date": details.get("release_date"),
        "Runtime": details.get("runtime"),
        "Budget": details.get("budget"),
        "Revenue": details.get("revenue"),
        "Vote Average": details.get("vote_average"),
        "Vote Count": details.get("vote_count"),
        "Movie ID": details.get("id"),
        "Popularity": details.get("popularity"),
        "Poster Path": details.get("poster_path"),
        "Director":director,
        "Cast": cast,
        "Keywords": keywords,
        "Genres": genres
    }


def collect_catalog(client,total_pages=20,first_page_data=None):
    movies=[]
    for page in range(1,total_pages+1):
        if page==1 and first_page_data:
            data=first_page_data
        else:
            data=discover_movies(client,page)
        page_movies=data.get("results",[])
        movies.extend(page_movies)

        time.sleep(0.5) 
    return movies

def save_catalog(movies):

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/discovered_movies.json","w",encoding="utf-8") as file:
        json.dump(movies,file,ensure_ascii=False,indent=4)
    print(f"Saved {len(movies)} to data/raw/discovered_movies.json")

def save_enriched_movies(enriched_movies):
    os.makedirs("data/enriched", exist_ok=True)
    with open("data/enriched/enriched_movies.json","w",encoding="utf-8") as file:
        json.dump(enriched_movies,file,ensure_ascii=False,indent=4)
    print(f"Saved {len(enriched_movies)} to data/enriched/enriched_movies.json")

def load_enriched_movies():
    file_path = "data/processed/enriched_movies.json"

    if not os.path.exists(file_path):
        return []

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "User-Agent": "MovieDataAnalysis/1.0"
}

def load_catalog():
    with open("data/raw/discovered_movies.json","r",encoding="utf-8") as file:
        return json.load(file)


with httpx.Client(headers=headers, timeout=20.0) as client:
    try:
        movies=load_catalog()
        print(f"Loaded {len(movies)} movies from data/raw/discovered_movies.json")
        enriched_movies=[]
        for index,movie in enumerate(movies):
            movie_id=movie.get("id")
            movie_data=get_movie_data(client,movie_id)
            enriched_movies.append(movie_data)
            if index%100==0:
                save_enriched_movies(enriched_movies)
                print(f"Progress: {index}/{len(movies)}")
            time.sleep(0.5)
        save_enriched_movies(enriched_movies)
        print(f"Enriched {len(enriched_movies)} movies.")

    except Exception as e:
        print(f"Error: {e}")



# def search_movie(query):
#     url = f"{BASE_URL}/search/movie"

#     params = {
#         "api_key": API_KEY,
#         "query": query
#     }

#     response = httpx.get(url, params=params)
#     response.raise_for_status()

#     return response.json()["results"]



# results = search_movie("Oppenheimer")
# movie_details=get_movie_details(results[0]["id"])
# movie_credits=get_movie_credits(results[0]["id"])
# movie_keywords=get_movie_keywords(results[0]["id"])
# movie_data = get_movie_data(results[0]["id"])
# print(movie_data)

# for key, value in movie_details.items():
#     print(f"{key}: {value}")

# for actor in movie_credits["cast"][:10]:
#     print(actor['name'],":",actor['character'])

# for crew in movie_credits['crew']:
#     if crew['job']=='Director':
#         print(f"Director: {crew['name']}")

# for keyword in movie_keywords['keywords']:
#     print(f"{keyword['name']}"+" ")

