import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

import requests
from bs4 import BeautifulSoup
from pprint import pprint

URL = "https://www.billboard.com/charts/hot-100/"
SPOTIFY_ID = "563c270011f0489a8ca7acf10a4a357a"
SPOTIFY_SECRETE = "27a4a29cd1b84e2fa003aeda3791952a"

#bs4------------------------------------------------------------------

user_input = input("Type in format YYYY-MM-DD: ")
user_url = URL+user_input

year = user_input.split('-')[0]

response = requests.get(user_url)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

titles_tag = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
titles = [title.getText() for title in titles_tag]

#spotipy--------------------------------------------------------------

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_ID, client_secret=SPOTIFY_SECRETE)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

song_uris = []
for i in titles:
    result = sp.search(q=f"track:{i} year:{year}", limit=1, type="track")
    # pprint(result['tracks']['href'])
    try:
        song_uris.append(result['tracks']['items'][0]['uri'])
    except IndexError:
        print(f"{i} does not exist in Spotify. Skip")

playlist = sp.user_playlist_create(sp.current_user()["id"], "20210318", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

# result = sp.search(q="coldplay", limit=1, type="track")
# pprint(result)


# sp = spotipy.Spotify(
#     auth_manager=SpotifyOAuth(
#         scope="playlist-modify-private",
#         redirect_uri="https://example.com/",
#         client_id=SPOTIFY_ID,
#         client_secret=SPOTIFY_SECRETE,
#         show_dialog=True,
#         cache_path="token.txt"
#     )
# )
#
# user_id = sp.current_user()["id"]
#
# sp.user_playlist_create(user_id,'top100top',public=True,collaborative=False,description='')
