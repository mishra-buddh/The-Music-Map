import pickle
import streamlit as st
import pandas as pd
import requests as re

def url_getter(song_id):  # Extract the url for the image from json returned by Spotify api
    api_id= 'https://v1.nocodeapi.com/ritik0009/spotify/UUQTqhAymGFOhQfE/tracks?ids='+song_id
    api_result= re.get(api_id)
    if api_result.status_code != 200: 
        st.warning(f"Bad response for {song_id}: {api_result.status_code}")
        return "https://via.placeholder.com/250" # display placeholder image
    try:
        result= api_result.json()
        return result['tracks'][0]['album']['images'][0]['url'] # extract image url for display
    except Exception as e:
        st.warning(f"Failed to parse {song_id}: {e}")
        return "https://via.placeholder.com/250" # display placeholder image


music_list= pickle.load(open("musics.pkl","rb"))
vect_similarity= pickle.load(open("similarities.pkl","rb"))

music_list= pd.DataFrame(music_list)
def recommendation_engine(song): # Returns the recommended music and poster url
    song= str(song)  # redundant statement for preventing any type mismatch


    indexing= music_list[music_list['track_name'] == song].index[0]

    distances= vect_similarity[indexing]

    song_list= sorted(list(enumerate(distances)), reverse= True, key= lambda x:x[1])[1:6]
    
    recommendations= []
    track_poster_id= []
    for i in song_list:
        recommendations.append(music_list.iloc[i[0]].track_name)
        track_poster_id.append(url_getter(music_list.iloc[i[0]]['track_id']))
    
    return recommendations, track_poster_id


st.title("Music System")

select_music= st.selectbox("What to play today?", music_list['track_name'].values)

if st.button('Play song ▶️'):
    recom, poster= recommendation_engine(select_music)
    
    post1, post2, post3, post4, post5 = st.columns(5) # 5 colums for 5 music posters
    with post1: 
        st.write(recom[0])
        st.image(poster[0], width= 250)
    with post2:
        st.write(recom[1])
        st.image(poster[1], width= 250)
    with post3:
        st.write(recom[2])
        st.image(poster[2], width= 250)
    with post4:
        st.write(recom[3])
        st.image(poster[3], width= 250)
    with post5:
        st.write(recom[4])
        st.image(poster[4], width= 250)