import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie ID from TMDb API
def fetch_movie_id(movie_title):
    api_key = '13e49bcd81550c0a30390b7cced9f811'
    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}'
    response = requests.get(url)
    data = response.json()
    if data['results']:
        return data['results'][0]['id']
    else:
        return None

# Function to fetch poster image using movie ID
def fetch_poster(movie_id):
    api_key = '13e49bcd81550c0a30390b7cced9f811'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=13e49bcd81550c0a30390b7cced9f811&language=en-US'
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data:
        return f"http://image.tmdb.org/t/p/w500/{data['poster_path']}"
    else:
        return None

# Function to recommend movies
def recommend(movie):
    movie_id = fetch_movie_id(movie)
    if movie_id:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

        recommended_movies = []
        recommended_movies_posters = []

        for i in movies_list:
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_posters.append(fetch_poster(fetch_movie_id(movies.iloc[i[0]].title)))

        return recommended_movies, recommended_movies_posters
    else:
        return [], []

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox('What movie have you watched?', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    for name, poster in zip(names, posters):
        st.header(name)
        st.image(poster)
