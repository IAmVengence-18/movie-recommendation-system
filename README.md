# 🎬 Movie Recommendation System

A content-based Movie Recommendation System built using NLP techniques, TF-IDF vectorization, and Cosine Similarity. The application recommends similar movies based on their metadata and displays posters, ratings, genres, directors, and movie overviews through an interactive Streamlit interface.

## 🚀 Live Demo

Deployed on Streamlit Cloud.

## ✨ Features

* Content-based movie recommendations
* Movie posters fetched using the TMDb API
* Movie ratings and release year
* Director and genre information
* Expandable movie overview section
* Interactive Streamlit web interface

## 🛠️ Tech Stack

* Python
* Pandas
* Scikit-Learn
* Streamlit
* TMDb API
* Git & GitHub

## 📊 Recommendation Method

1. Movie metadata preprocessing
2. Feature engineering using movie overview, genres, keywords, cast, and crew
3. TF-IDF Vectorization
4. Cosine Similarity computation
5. Top-N movie recommendation retrieval

## 📁 Project Structure

```text
app.py
movie_data_deploy.pkl
similarity_float16.pkl
requirements.txt
README.md
```

## 🔧 Challenges Solved

* API integration using TMDb
* Streamlit deployment
* Secret management using Streamlit Secrets
* Similarity matrix optimization from 184 MB to 46 MB using float16 conversion
* Deployment-friendly data reduction from 41 MB to 1.9 MB

## 🚀 Future Improvements

* Larger movie dataset
* Search autocomplete
* User authentication
* Hybrid recommendation system
* Transformer/embedding-based recommendations
* Improved UI and responsiveness

## 👨‍💻 Author

Lavya Gaba

B.Tech Computer Science, VIT Vellore
