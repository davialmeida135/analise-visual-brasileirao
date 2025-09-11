import pandas as pd
from geopy.geocoders import Nominatim
import time

# Carrega os dados das partidas
partidas = pd.read_csv("../data/raw/campeonato-brasileiro-full.csv")

# Cria um dicionário para armazenar as estatísticas dos estádios
estadios_dict = {}
for partida in partidas.iterrows():
    partida = partida[1]
    estadio = partida["arena"]
    if estadio not in estadios_dict:
        estadios_dict[estadio] = {
            "partidas": 1,
            "vitorias_casa": 0,
            "vitorias_fora": 0,
            "empates": 0,
            "data_primeira_partida": partida["data"],
            "data_ultima_partida": partida["data"],
            "times_casa": {},
        }
    else:
        estadios_dict[estadio]["partidas"] += 1

    if partida["vencedor"] == partida["mandante"]:
        estadios_dict[estadio]["vitorias_casa"] += 1
    elif partida["vencedor"] == partida["visitante"]:
        estadios_dict[estadio]["vitorias_fora"] += 1
    else:
        estadios_dict[estadio]["empates"] += 1

    estadios_dict[estadio]["data_ultima_partida"] = partida["data"]
    estadios_dict[estadio]["times_casa"][partida["mandante"]] = (
        estadios_dict[estadio]["times_casa"].get(partida["mandante"], 0) + 1
    )

# Converte o dicionário em um DataFrame
estadios_pd = pd.DataFrame(estadios_dict).transpose()

geolocator = Nominatim(user_agent="analise-visual-brasileirao")
lat = []
lon = []

# Pipeline de busca de coordenadas geográficas de cada estádio
for index, estadio in estadios_pd.iterrows():
    print(f"Procurando {estadio.name}...")
    location = None
    for attempt in range(3):
        try:
            location = geolocator.geocode(estadio.name)
            if location:
                break
        except Exception as e:
            print(f"Erro na tentativa {attempt + 1}: {e}")
            time.sleep(1)
    if location:
        lat.append(location.latitude)
        lon.append(location.longitude)
        print(f"achou {location.latitude}, {location.longitude}")
    else:
        print("não achou")
        lat.append("Unk")
        lon.append("Unk")

estadios_pd["latitude"] = lat
estadios_pd["longitude"] = lon

# Salva o DataFrame em um arquivo CSV
estadios_pd.to_csv("../data/analise_estadios/estadios.csv", index_label="estadio")
