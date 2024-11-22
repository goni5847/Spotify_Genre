import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configurar autenticação com a API
CLIENT_ID = "b81a16193da84fb8913306533ac9dcd0"
CLIENT_SECRET = "bb63c11708dc4473a109755e037f5b09"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Função para obter características acústicas
def get_audio_features(track_id):
    features = sp.audio_features(track_id)
    if features and features[0]:
        return features[0]
    return None

# Função para obter o gênero do artista
def get_artist_genre(artist_id):
    artist_info = sp.artist(artist_id)
    return artist_info.get('genres', [])

# Track ID from URL
track_id = '4nV8PITIDTuj7bZKN7ysZB'

# Obter detalhes da música
track_info = sp.track(track_id)
audio_features = get_audio_features(track_id)

# Obter o gênero do artista
artist_id = track_info['artists'][0]['id']
artist_genres = get_artist_genre(artist_id)

if audio_features:
    track_details = {
        'track_id': track_id,
        'track_name': track_info['name'],
        'artist_name': track_info['artists'][0]['name'],
        'album_name': track_info['album']['name'],
        'danceability': audio_features['danceability'],
        'energy': audio_features['energy'],
        'tempo': audio_features['tempo'],
        'valence': audio_features['valence'],
        'acousticness': audio_features['acousticness'],
        'genres': artist_genres  # Adding genres of the artist
    }
    print(track_details)
else:
    print("Audio features not available.")
