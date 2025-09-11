```python
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
```
```python
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
```

```python
import pandas as pd

# Carregar o dataset de partidas
partidas = pd.read_csv('../data/raw/campeonato-brasileiro-full.csv')

# Converter a coluna 'Data' para o formato datetime e extrair o ano
partidas['data'] = pd.to_datetime(partidas['data'], dayfirst=True)
partidas['ano'] = partidas['data'].dt.year

# Inicializar um dicionário para armazenar os dados agregados
estadios_ano_dict = {}

# Iterar sobre cada partida para agregar os dados por estádio e ano
for _, partida in partidas.iterrows():
    estadio = partida['arena']
    ano = partida['ano']
    
    if (estadio, ano) not in estadios_ano_dict:
        estadios_ano_dict[(estadio, ano)] = {
            'estadio': estadio,
            'ano': ano,
            'partidas': 0,
            'vitorias_casa': 0,
            'vitorias_fora': 0,
            'empates': 0,
        }
    
    # Atualizar as estatísticas
    estadios_ano_dict[(estadio, ano)]['partidas'] += 1
    if partida['vencedor'] == partida['mandante']:
        estadios_ano_dict[(estadio, ano)]['vitorias_casa'] += 1
    elif partida['vencedor'] == partida['visitante']:
        estadios_ano_dict[(estadio, ano)]['vitorias_fora'] += 1
    else:
        estadios_ano_dict[(estadio, ano)]['empates'] += 1

# Converter o dicionário em um DataFrame
estadios_ano_df = pd.DataFrame(estadios_ano_dict.values())

# Salvar o novo dataset
estadios_ano_df.to_csv('../data/processed/estadios_por_ano.csv', index=False)
```