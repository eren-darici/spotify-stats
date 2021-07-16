import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
from urllib.request import urlretrieve
import json

class Spotify:
    def __init__(self):
        os.environ['SPOTIPY_CLIENT_ID'] = ''
        os.environ['SPOTIPY_CLIENT_SECRET'] = ''
        os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'
        
        self.scope = "user-library-read user-top-read user-read-currently-playing user-follow-read"

    def login(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))
        print("Connected as", self.sp.current_user()['display_name'])

    def current_info(self):
        if type(self.sp.currently_playing()) is not None:
            songName = self.sp.currently_playing()['item']['name']
            artistName = self.sp.currently_playing()['item']['artists'][0]['name']
            result = self.sp.currently_playing()['item']['id']
            features = self.sp.audio_analysis(result)
            # result = self.sp.currently_playing()
            # return json.dumps(features, indent=4)
            track = features['track']
            informations = {'tempo': track['tempo'],
                            'name': songName,
                            'artist': artistName,
                            'key': track['key'],
                            'mode': track['mode'],
                            'cover_url': self.sp.currently_playing()['item']['album']['images'][0]['url']}

            return informations
        else:
            return "ERROR: App could not find any songs playing right now. Please open a song and try again."


    def _load_json(self, json_file):
        with open(json_file) as file:
            tonal_information = json.load(file)

        return tonal_information

    def currentSong(self, json_file):
        tonal_information = self._load_json(json_file)
        song_information = self.current_info()

        informations = {'song': song_information['name'],
                        'artist': song_information['artist'],
                        'tempo': song_information['tempo'],
                        'key': tonal_information['pitchClass'][str(song_information['key'])],
                        'mode': tonal_information['mode'][str(song_information['mode'])],
                        'cover_url': song_information['cover_url']}

        return informations

    def download_cover(self, url):
        urlretrieve(url, "static/cover.png")

    def stats(self):
        genres = []
        for song in self.sp.current_user_top_tracks(time_range='short_term')['items']:
            # print(json.dumps(song['album']['id'], indent=4))
            # print("--")
            try:
                data = self.sp.artist(song['artists'][0]['external_urls']['spotify'])['genres'][0]
                # print(data)
                genres.append(data)
            except:
                data = "NO GENRE DATA AVAILABLE"
                # print(data)
                genres.append(data)
        occurence = {}
        for genre in genres:
            occurence[genre] = (genres.count(genre) / len(genres)) * 100

        occurence = dict(sorted(occurence.items(), key=lambda item: item[1]))
        for key in occurence:
            occurence[key] = str(occurence[key])

        return occurence
