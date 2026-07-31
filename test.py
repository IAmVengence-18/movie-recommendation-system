import pickle
import streamlit as st
import httpx
import time
import re
api_key = st.secrets["TMDB_API_KEY"]

movie = pickle.load(open('movie_data.pkl', 'rb'))
similarity = pickle.load(open('similarity_float16.pkl', 'rb'))

print(type(movie["production_companies"]))
print(movie["production_companies"])

print(type(movie["production_companies"][0]))
print(movie["production_companies"][0]) 