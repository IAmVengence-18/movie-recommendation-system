import os
import httpx

API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"

def discover_movies(page):
    url=f"{BASE_URL}/discover/movie"
    params={
        "api_key": API_KEY,
        "page": page,
        'vote_count.gte': 1000,
    }
    try:
        response=httpx.get(url,params=params,timeout=20)
    except httpx.HTTPError as e:
        print(f"Error fetching movie data: {e}")
        return {"results": []}

    response.raise_for_status()

    return response.json()

data=discover_movies(1)
movies=data['results']
print(len(movies))



# def search_movie(query):
#     url = f"{BASE_URL}/search/movie"

#     params = {
#         "api_key": API_KEY,
#         "query": query
#     }

#     response = httpx.get(url, params=params)
#     response.raise_for_status()

#     return response.json()["results"]


# def get_movie_details(movie_id):
#     url = f"{BASE_URL}/movie/{movie_id}"

#     params = {
#         "api_key": API_KEY
#     }

#     response = httpx.get(url, params=params)
#     response.raise_for_status()

#     return response.json()

# def get_movie_credits(movie_id):
#     url = f"{BASE_URL}/movie/{movie_id}/credits"

#     params = {
#         "api_key": API_KEY
#     }

#     response = httpx.get(url, params=params)
#     response.raise_for_status()

#     return response.json()

# def get_movie_keywords(movie_id):
#     url = f"{BASE_URL}/movie/{movie_id}/keywords"

#     params = {
#         "api_key": API_KEY
#     }

#     response = httpx.get(url, params=params)
#     response.raise_for_status()

#     return response.json()


# def get_movie_data(movie_id):
#     details = get_movie_details(movie_id)
#     credits = get_movie_credits(movie_id)
#     keywords_data = get_movie_keywords(movie_id)
    
#     director = None
#     cast=[]
#     keywords=[]
#     genres=[]

#     for crew in credits.get('crew', []):
#         if crew.get('job')=='Director':
#             director=crew.get('name')
#             break
    
#     cast=[actor.get('name') for actor in credits.get('cast', [])[:5]]

#     keywords=[keyword.get('name') for keyword in keywords_data.get('keywords', [])]

#     genres=[genre.get('name') for genre in details.get('genres', [])]

#     return {
#         "Title": details.get("title"),
#         "Overview": details.get("overview"),
#         "Release Date": details.get("release_date"),
#         "Runtime": details.get("runtime"),
#         "Budget": details.get("budget"),
#         "Revenue": details.get("revenue"),
#         "Vote Average": details.get("vote_average"),
#         "Vote Count": details.get("vote_count"),
#         "Movie ID": details.get("id"),
#         "Popularity": details.get("popularity"),
#         "Poster Path": details.get("poster_path"),
#         "Director":director,
#         "Cast": cast,
#         "Keywords": keywords,
#         "Genres": genres
#     }


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

