import pickle
import streamlit as st
import httpx
import time
import re
st.markdown("""
<style>
div[data-testid="column"] {
    padding-left: 15px;
    padding-right: 15px;
}
.streamlit-expanderHeader {
    font-size: 16px;
}
img {
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

api_key = 'b35242cb2e4677d8a1416b5b68f9bac0'

movies = pickle.load(open('movie_data.pkl', 'rb'))
similarity = pickle.load(open('similarity_cv.pkl', 'rb'))

st.title("MOVIE RECOMMENDER SYSTEM")
selected_movie=st.selectbox('Select a movie',movies['title'].values)
myButton=st.button('Recommend')

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:4]
    recommended_movies=[]
    for i in movies_list:
        recommended_movies.append({'title': movies.iloc[i[0]].title,
                                   'movie_id': movies.iloc[i[0]].movie_id,
                                   'vote_average': movies.iloc[i[0]].vote_average,
                                   'year': movies.iloc[i[0]].year,
                                   'director': movies.iloc[i[0]].director,
                                   'overview': movies.iloc[i[0]].overview,
                                   'genre_names': movies.iloc[i[0]].genre_names
                                   })
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
    cols=st.columns(3, gap="large")
    for i,movie in enumerate(recommended_movies):
        with cols[i]:
            poster = fetch_poster(movie["movie_id"])
            if poster:
                st.image(poster, width=200)
            else:
                st.write("🎬 Poster unavailable")
            st.markdown(f"<h4>{movie['title']}</h4>",unsafe_allow_html=True)
            with st.expander("Details"):
                st.write(f" ⭐ {movie['vote_average']}")
                st.caption(f"📅 {int(movie['year'])}")
                st.caption(f"🎬 {re.sub(r'(?<!^)([A-Z])', r' \1', movie['director'])}")
                st.write(f"🎭 {', '.join(movie['genre_names'])}")
                with st.expander("Overview"):
                    st.write(movie["overview"]) 
            time.sleep(1)

# col1,col2 = st.columns(2)
# with col1:
#     st.write("This is column 1")
# with col2:
#     st.write("This is column 2")