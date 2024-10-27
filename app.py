import pickle
import streamlit as st
import re

#Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movies['original_title'].values

def clean_string(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def recommend(movie_name, n=5, sort_order=None):
    cleanedMovieName = clean_string(movie_name)
    if cleanedMovieName not in movies['title_clean'].values:
        st.error("Movie not found in the dataset.")
        return []

    idx = movies[movies['title_clean'] == cleanedMovieName].index[0]
    movieidx_smlr = [(i, similarity[idx][i]) for i in range(len(similarity[idx]))]
    sortSmlr = sorted(movieidx_smlr, reverse=True, key=lambda x: x[1])

    if n > len(sortSmlr) - 1:
        n = len(sortSmlr) - 2
        
    recommended_movies = []
    for i in sortSmlr[1:n + 1]:
        movie_data = {
            "title": movies.iloc[i[0]].original_title,
            "release_year": movies.iloc[i[0]].release_year,
            "rating": movies.iloc[i[0]].rating,
            "popularity": movies.iloc[i[0]].popularity
        }
        recommended_movies.append(movie_data)
    
    # Apply sorting based on user-selected order
    if sort_order == "Most Similar Content":
        # Default to similarity (already sorted)
        pass
    elif sort_order == "Newest First":
        recommended_movies.sort(key=lambda x: x['release_year'], reverse=True)
    elif sort_order == "Oldest First":
        recommended_movies.sort(key=lambda x: x['release_year'])
    elif sort_order == "Highest Rating":
        recommended_movies.sort(key=lambda x: x['rating'], reverse=True)
    elif sort_order == "Lowest Rating":
        recommended_movies.sort(key=lambda x: x['rating'])
    elif sort_order == "Most Popular":
        recommended_movies.sort(key=lambda x: x['popularity'], reverse=True)
    elif sort_order == "Least Popular":
        recommended_movies.sort(key=lambda x: x['popularity'])
    
    return [movie['title'] for movie in recommended_movies]

#Frontend code starts here
c1, c2, c3 = st.columns([1, 2, 1]) 
image_path = "title.jpg"
with c2:
    st.image(image_path)

selected_movie = st.selectbox("Type here or select a movie from dropdown list", movie_list)
number = st.slider("How many movies do you want?", min_value=0, max_value=50, value=5)

col1, col2 = st.columns([2, 1])

with col2: 
    sort_order = st.selectbox("Sort by", options=[
        "Most Similar Content", 
        "Newest First", 
        "Oldest First", 
        "Highest Rating", 
        "Lowest Rating", 
        "Most Popular", 
        "Least Popular"], 
        index=0)  # Set the default selection to "Most Similar Content"

with col1:
    if st.button('Show Recommendation'):
        # If no sort order is selected, it defaults to "Most Similar Content"
        recommended_movie_names = recommend(selected_movie, number, sort_order)
        for movie in recommended_movie_names:
            st.subheader(movie, divider=True)
