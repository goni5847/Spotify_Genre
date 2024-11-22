import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Configurar autenticação com a API
CLIENT_ID = "b81a16193da84fb8913306533ac9dcd0"
CLIENT_SECRET = "bb63c11708dc4473a109755e037f5b09"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Função para obter todas as características acústicas de uma faixa
def get_audio_features(track_id):
    features = sp.audio_features(track_id)
    if features and features[0]:
        return features[0]
    return None

# Função para coletar dados de músicas com todas as características acústicas
def get_track_data(query, limit=20):
    global id
    total_tracks = 0
    data = []

    # Use a while loop to collect tracks until we reach the desired limit
    while total_tracks < limit:
        results = sp.search(q=query, type='track', limit=50, offset=total_tracks)
        tracks = results['tracks']['items']
        
        # If no more tracks are found, break the loop
        if not tracks:
            break

        for track in tracks:
            track_id = track['id']
            track_name = track['name']
            artist_name = track['artists'][0]['name']

            # Verificar se o track_id já foi adicionado
            if track_id not in seen_ids:
                # Tentar obter características acústicas
                audio_features = get_audio_features(track_id)
                if audio_features:
                    # Adicionar o gênero como a última coluna
                    data.append({
                        'id': id,
                        'danceability': audio_features['danceability'],
                        'energy': audio_features['energy'],
                        'key': audio_features['key'],
                        'loudness': audio_features['loudness'],
                        'mode': audio_features['mode'],
                        'speechiness': audio_features['speechiness'],
                        'acousticness': audio_features['acousticness'],
                        'instrumentalness': audio_features['instrumentalness'],
                        'liveness': audio_features['liveness'],
                        'valence': audio_features['valence'],
                        'tempo': audio_features['tempo'],
                        'time_signature': audio_features['time_signature'],
                        'genre': query.split(':')[1],  # Extrair o gênero da query
                        'track_name': track_name,
                        'artist_name': artist_name,
                    })
                    seen_ids.add(track_id)  # Adicionar o track_id ao conjunto de ids únicos
                    id += 1
                    total_tracks += 1  # Increment the total track count

    return data


# Exemplo: coletar dados para diferentes gêneros
genres = ['pop', 'rock', 'indie', 'metal', 'acoustic', 'alternative', 'ambient', 'blues', 'edm', 'reggae', 'classical']
all_tracks = []

# Inicializar a variável global 'id' e o conjunto de ids 'seen_ids'
id = 0
seen_ids = set()

for genre in genres:
    print(f"Coletando músicas do gênero: {genre}")
    all_tracks.extend(get_track_data(f'genre:{genre}', limit=10))  # Request 10 tracks per genre

# Criar um DataFrame com todas as características acústicas
df = pd.DataFrame(all_tracks)

# Salvar a tabela como CSV
df.to_csv('spotify_tracks_all_audio_features.csv', index=False)

print("Tabela criada com sucesso!")
