import pickle
import streamlit as st
import httpx
import time

api_key = 'xxx'

movies = pickle.load(open('movie_data.pkl', 'rb'))
similarity = pickle.load(open('similarity_cv.pkl', 'rb'))

st.title("MOVIE RECOMMENDER SYSTEM")
selected_movie=st.selectbox('Select a movie',movies['title'].values)
myButton=st.button('Recommend')

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    for i in movies_list:
        recommended_movies.append({'title': movies.iloc[i[0]].title,
                                   'movie_id': movies.iloc[i[0]].movie_id})
    return recommended_movies

def fetch_poster(movie_id):
    import time
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for attempt in range(3):
        try:
            response = httpx.get(
                url,
                headers=headers,
                timeout=10
            )
            data = response.json()
            print(movie_id)
            print(data.get('poster_path'))
            print(data.get('original_title'))
            poster_path = data['poster_path']
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

        except Exception as e:
            print(f"Attempt {attempt+1} failed for {movie_id}")
            print(e)
            time.sleep(1)
    return None


if myButton:
    recommended_movies = recommend(selected_movie)
    st.write('Recommended movies:')
    for movie in recommended_movies:
        poster = fetch_poster(movie["movie_id"])
        if poster:
            st.image(poster)

        st.write(movie["title"])
        time.sleep(1)

