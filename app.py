import streamlit as st 
import pandas as pd
import pickle
import requests
st.title('Movie Recommender System')

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{movie_id}?api_key=d4eea7b287474a4b062a1f0574a168aa&language=en-US'.format(movie_id=movie_id))
    data=response.json()
    # st.text(data) 
    # st.text('https://api.themoviedb.org/3/movie/{movie_id}?api_key=d4eea7b287474a4b062a1f0574a168aa&language=en-US'.format(movie_id=movie_id))
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']

movies_dict= pickle.load(open('movies_dict.pkl','rb'))
similarity= pickle.load(open('similarity.pkl','rb'))
movies=pd.DataFrame(movies_dict)

selected_movie_name=st.selectbox('Title',movies['title'].values)

def recommend(movie):
    movie_index=movies[movies['title'] == movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommend_movies=[]
    recommend_movie_posters=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].movie_id
        #fetch poster from API
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movie_posters.append(fetch_poster(movie_id))
    return recommend_movies,recommend_movie_posters

if st.button('Recommend'):
   names,posters = recommend(selected_movie_name)
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