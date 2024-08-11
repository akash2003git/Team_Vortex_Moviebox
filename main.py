import streamlit as st
import pickle

st.set_page_config(layout="wide")

# Load the data
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Initialize or load watchlist
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

st.header("MOVIEBOX")

# Dropdown menu for selecting a movie
selected_movie = st.selectbox("Select a movie: ", movies_list)


def recommend(film):
    index = movies[movies['title'] == film].index[0]
    poster_urls = movies['poster_path'].apply(lambda x: f"https://image.tmdb.org/t/p/w500{x}")
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])

    recommend_movie = []
    recommend_poster = []
    recommend_release_date = []
    recommend_rating = []
    recommend_overview = []

    for i in distance[1:16]:  # Get top 15 recommendations
        movie = movies.iloc[i[0]]
        recommend_movie.append(movie['title'])
        recommend_poster.append(poster_urls[i[0]])
        recommend_release_date.append(movie['release_date'])
        recommend_rating.append(movie['vote_average'])
        recommend_overview.append(movie['overview'])

    return recommend_movie, recommend_poster, recommend_release_date, recommend_rating, recommend_overview


if st.button("Show Recommend"):
    movie_names, movie_posters, release_dates, ratings, overviews = recommend(selected_movie)

    # Create columns for displaying the movie information
    num_cols = 5
    for i in range(0, len(movie_names), num_cols):
        cols = st.columns(num_cols)
        for j, col in enumerate(cols):
            index = i + j
            if index < len(movie_names):
                col.image(movie_posters[index], width=200)
                with col:
                    with st.popover("Overview"):
                        st.markdown(overviews[index])
                col.write(f"**{movie_names[index]}**")
                col.write(f"Release Date: {release_dates[index]}  \n Rating: {ratings[index]}")


