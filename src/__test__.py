import secrets
from src.__init__ import SpotifyAPI
import json


clientID = secrets.clientID
clientSecret = secrets.clientSecret

spotify = SpotifyAPI(clientID, clientSecret, response_format='json')
theslowrush = spotify.get_album('31qVWUdRrlb8thMvts0yYL?si=D1zRNNpgQhm2u4ghc4lE1g')
print(spotify.get_artist_top_tracks("7vtSUU3zpHeYJfX6BPNrJd?si=btSPCo7OSdesUYSX03ZQVw"))



"""
with open('album.json', 'w') as f:
    json.dump(theslowrush, f)"""
    
