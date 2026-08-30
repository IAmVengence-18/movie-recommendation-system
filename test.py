import os
import httpx

url = "https://3.175.86.103/3/discover/movie"

params = {
    "api_key": os.getenv("TMDB_API_KEY"),
    "page": 1,
    "vote_count.gte": 1000
}

headers = {
    "Host": "api.themoviedb.org"
}

response = httpx.get(
    url,
    params=params,
    headers=headers,
    timeout=20,
    verify=True
)

print(response.status_code)
print(response.text[:500])