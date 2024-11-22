import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Configurar autenticação com a API
CLIENT_ID = "b81a16193da84fb8913306533ac9dcd0"
CLIENT_SECRET = "bb63c11708dc4473a109755e037f5b09"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Função para obter todos os gêneros disponíveis no Spotify
def get_spotify_genres():
    genres = sp.recommendation_genre_seeds()
    return genres['genres']

# Obter todos os gêneros
spotify_genres = get_spotify_genres()

# Imprimir todos os gêneros
print("Available Spotify Genres:")
for genre in spotify_genres:
    print(genre)
