import httpx

api_key = "b35242cb2e4677d8a1416b5b68f9bac0"

movie_id = 68721   # Iron Man 3

url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"

response = httpx.get(url)

print(response.status_code)

data = response.json()

print(data["original_title"])
print(data["poster_path"])