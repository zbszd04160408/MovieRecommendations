import streamlit as st
import pandas as pd
import numpy as np
from scipy.spatial import distance
from PIL import Image
import os.path
from pathlib import Path

def get_5recommendation_yesKmeans(df, movie_id):
    """
    Get the dataframe having distance between input movies and others, and 5 recommendation movie ID
    (This function only treats a dataframe created by K-mode AND K-means clustering)
    
    Parameters
    ----------
    df : dataframe
        a dataframe among 4 I mentioned above
    movie_id : str
        input movie's id
        
    Returns
    -------
    subgroup_df
        a dataframe having only movies within the same group as input movie + distance between input movie to others
    recommendation
        a list containig 5 movie's id (The 5 closest distance movie's id)
    """
    # Find the group number of input movie.
    group_num = df[df["id"] == movie_id]['group'].values[0]
    # Find the subgroup number of input movie.
    subgroup_num = df[df["id"] == movie_id]['subgroup'].values[0]
    # Get dataframe of which the group number is same as the input movie's group
    subgroup_df = df[(df["group"] == group_num)&(df["subgroup"] == subgroup_num)].reset_index(drop = True)
    # Convert input movie's features into list
    standard_point = subgroup_df[subgroup_df["id"] == movie_id].loc[:, "review_1st":"popularity"].values.tolist()
    
    # Calculate the euclidean distance between input movie and other movies within the same cluster
    for i in range(subgroup_df.shape[0]):
        point = subgroup_df.iloc[i]["review_1st":"popularity"].values.tolist()
        
        subgroup_df.loc[i, "distance"] = distance.euclidean(standard_point, point)
    
    subgroup_df_temp = subgroup_df[subgroup_df.id != movie_id]
    recommendation = subgroup_df_temp.sort_values(by = ['distance'])[:5]['id'].values.tolist()
    
    return subgroup_df, recommendation


functions = ['Please Select', 'Ratings Recommendation', 'Content Recommendations']

option = st.sidebar.selectbox('Please select the function you would like to use:', functions)

main_df_filepath = Path(__file__).parents[0] / 'Data/IMDb_movies.csv'
noVotes_kmodesKmeans_path = Path(__file__).parents[0] / 'Data/noVotes_kmode_kmeans_final_df.csv'
withVotes_kmodesKmeans_path = Path(__file__).parents[0] / 'Data/yesVotes_kmode_kmeans_final_df.csv'
main_df = pd.read_csv(main_df_filepath)
noVotes_kmodesKmeans_data = pd.read_csv(noVotes_kmodesKmeans_path)
withVotes_kmodesKmeans_data = pd.read_csv(withVotes_kmodesKmeans_path)

ids = noVotes_kmodesKmeans_data[['id']]
merged_df = pd.merge(ids, main_df, left_on="id", right_on="imdb_title_id")
movies = np.array(merged_df[['title']].values.tolist()).squeeze()

if option == 'Please Select':
    st.title("Welcome to our Movie Recommendation System!")
    st.header("Please Select Any Function You Would Like On the Sidebar! ")
elif option == 'Ratings Recommendation':
    st.title("Recommendations Based on Ratings")
    st.write("Ranked by the distance from the selected movie. ")
    movie = st.sidebar.selectbox('Please select a movie:', movies)
    id = main_df[main_df['title'] == movie]['imdb_title_id'].values[0]
    st.header("Movie Recommendation for %s" % movie)
    poster_name = '%s.jpg' % id
    path = Path(__file__).parents[0] /'Data/movie_poster/total'/poster_name
    if os.path.exists(path):
        image = Image.open(path)
        st.image(image, caption=movie)
    subdf, rec = get_5recommendation_yesKmeans(noVotes_kmodesKmeans_data, id)
    for i in rec:
        movie_title = main_df[main_df['imdb_title_id'] == i]['title'].values[0]
        year = main_df[main_df['imdb_title_id'] == i]['year'].values[0]
        genre = main_df[main_df['imdb_title_id'] == i]['genre'].values[0]
        country = main_df[main_df['imdb_title_id'] == i]['country'].values[0]
        language = main_df[main_df['imdb_title_id'] == i]['language'].values[0]
        director = main_df[main_df['imdb_title_id'] == i]['director'].values[0]
        avg_votes = main_df[main_df['imdb_title_id'] == i]['avg_vote'].values[0]
        st.subheader(movie_title)
        st.write("Year: %s"%year)
        st.write("Genre: %s" % genre)
        st.write("Country: %s" % country)
        st.write("Language: %s" % language)
        st.write("Director: %s" % director)
        st.write("Average Ratings: %.2f" % avg_votes)
        pn = '%s.jpg' % i
        p = Path(__file__).parents[0] /'Data/movie_poster/total'/pn
        if os.path.exists(p):
            image = Image.open(p)
            st.image(image, caption=movie_title)


elif option == 'Content Recommendations':
    st.title("Recommendations Based on Content")
    st.write("Ranked by the distance from the selected movie. ")
    movie = st.sidebar.selectbox('Please select a movie:', movies)
    id = main_df[main_df['title'] == movie]['imdb_title_id'].values[0]
    st.header("Movie Recommendation for %s" % movie)
    poster_name = '%s.jpg' % id
    path = Path(__file__).parents[0] /'Data/movie_poster/total'/poster_name
    if os.path.exists(path):
        image = Image.open(path)
        st.image(image, caption=movie)
    subdf, rec = get_5recommendation_yesKmeans(withVotes_kmodesKmeans_data, id)
    for i in rec:
        movie_title = main_df[main_df['imdb_title_id'] == i]['title'].values[0]
        year = main_df[main_df['imdb_title_id'] == i]['year'].values[0]
        genre = main_df[main_df['imdb_title_id'] == i]['genre'].values[0]
        country = main_df[main_df['imdb_title_id'] == i]['country'].values[0]
        language = main_df[main_df['imdb_title_id'] == i]['language'].values[0]
        director = main_df[main_df['imdb_title_id'] == i]['director'].values[0]
        avg_votes = main_df[main_df['imdb_title_id'] == i]['avg_vote'].values[0]
        st.subheader(movie_title)
        st.write("Year: %s"%year)
        st.write("Genre: %s" % genre)
        st.write("Country: %s" % country)
        st.write("Language: %s" % language)
        st.write("Director: %s" % director)
        st.write("Average Ratings: %.2f" % avg_votes)
        pn = '%s.jpg' % i
        p = Path(__file__).parents[0] /'Data/movie_poster/total'/pn
        if os.path.exists(p):
            image = Image.open(p)
            st.image(image, caption=movie_title)