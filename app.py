import pickle
import streamlit as st

movies = pickle.load(open('movie_data.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("MOVIE RECOMMENDER SYSTEM")
selected_movie=st.selectbox('Select a movie',movies['title'].values)
myButton=st.button('Recommend')

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

if myButton:
    recommended_movies = recommend(selected_movie)
    st.write('Recommended movies:')
    for movie in recommended_movies:
        st.write(movie)
