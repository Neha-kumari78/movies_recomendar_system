import streamlit as st
import pickle
import pandas as pd
import requests


# Fetch Poster Function
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=eebd3594e326bb80c33a92f5e56d6b6d&language=en-US"

    response = requests.get(url)

    data = response.json()

    # If poster exists
    if 'poster_path' in data and data['poster_path']:

        poster_path = data['poster_path']

        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path

        return full_path

    # Fallback image
    else:
        return "https://via.placeholder.com/500x750?text=No+Poster"


# Recommendation Function
def recommend(movie):

    # movie index
    index = movies_list[movies_list['title'] == movie].index[0]

    # similarity scores
    distances = similarity[index]

    # top 5 movies
    movies_list1 = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list1:

        movie_id = movies_list.iloc[i[0]].movie_id

        # movie name
        recommended_movies.append(
            movies_list.iloc[i[0]].title
        )

        # movie poster
        recommended_movies_posters.append(
            fetch_poster(movie_id)
        )

    return recommended_movies, recommended_movies_posters


# Load Files
movies_list = pickle.load(open('movies.pkl', 'rb'))

similarity = pickle.load(open('similarity.pkl', 'rb'))


# Streamlit UI
st.title(" MOVIE RECOMMENDER SYSTEM")


selected_movie_name = st.selectbox(
    "Select Movie",
    movies_list['title'].values
)


# Recommend Button
if st.button('Recommend'):

    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])