import streamlit as st
import pandas as pd

import streamlit as st

st.title("曲分析アプリへようこそ")


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = "65ea74f9e1b14363948853e8f98e79d3"
client_secret = "e6128fa21fc9456f978abeabfb4ca054"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

track_name = st.text_input("検索したい楽曲を入力してください:")
result = sp.search(track_name, limit=1, type="track")

if result["tracks"]["items"]:
    track = result["tracks"]["items"][0]
    st.write(f"Track Name: {track['name']}")
    st.write(f"Artists: {', '.join([artist['name'] for artist in track['artists']])}")
    st.image(track['album']['images'][0]['url'], caption='Album Cover', use_column_width=True)
else:
    st.warning("申し訳ありません。見つかりませんでした.")

if st.button("分析する"):
    audio_features = sp.audio_features(track['id'])[0]
    st.write("### 楽曲分析:")
    st.write(f" - ダンサブル: {audio_features['danceability']}")
    st.write(f" - キー: {audio_features['key']}")
    st.write(f" - 生活: {audio_features['liveness']}")
    st.write(f" - ラウドネス: {audio_features['loudness']}")
    st.write(f" - エネルギー: {audio_features['energy']}")
    st.write(f" - 言葉の量: {audio_features['speechiness']}")
    st.write(f" - モード: {audio_features['mode']}")
    st.write(f" - アコースティック: {audio_features['acousticness']}")
    st.write(f" - テンポ: {audio_features['tempo']}")
    st.write(f" - バランス: {audio_features['valence']}")
    st.write(f" - 拍子: {audio_features['time_signature']}")

    # 他の分析データも同様に表示できます

#再生させる
# if result["tracks"]["items"]:
#     track = result["tracks"]["items"][0]
#     st.write(f"Track Name: {track['name']}")
#     st.write(f"Artists: {', '.join([artist['name'] for artist in track['artists']])}")
#     st.image(track['album']['images'][0]['url'], caption='Album Cover', use_column_width=True)

#     # Embed Playerを追加
#     st.write("### Preview:")
#     st.write(f" [Listen on Spotify](https://open.spotify.com/embed/track/{track['id']})")

if result["tracks"]["items"]:
    # Embed Playerを追加
    st.write("### Preview:")
    st.markdown(f'<iframe src="https://open.spotify.com/embed/track/{track["id"]}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)


# 類似楽曲の提案
recommendations = sp.recommendations(seed_tracks=[track['id']], limit=5)
st.write("### おススメ！")
for rec_track in recommendations['tracks']:
        st.write(f"- [{rec_track['name']}]({rec_track['external_urls']['spotify']}) by {', '.join([artist['name'] for artist in rec_track['artists']])}")
else:
    st.warning("No results found.")