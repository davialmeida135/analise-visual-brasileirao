from typing import defaultdict
import pandas as pd

# Carrega csv com dados dos times e anos
partidas = pd.read_csv("../data/raw/campeonato-brasileiro-full.csv")

# Seleciona colunas relevantes
partidas = partidas[["data", "mandante", "visitante", "vencedor"]]

partidas['data'] = pd.to_datetime(partidas['data'], dayfirst=True)
partidas['ano'] = partidas['data'].dt.year

mandante_ano_dict = defaultdict()

# Iterar sobre cada partida para agregar os dados por estádio e ano
for _, partida in partidas.iterrows():
    ano = partida['ano']
    mandante = partida['mandante']

    if (ano, mandante) not in mandante_ano_dict:
        mandante_ano_dict[(ano, mandante)] = {
            'ano': ano,
            'mandante': mandante,
            'partidas': 0,
            'vitorias_casa': 0,
            'derrotas_casa': 0,
            'empates': 0,
        }
    
    # Atualizar as estatísticas
    mandante_ano_dict[(ano, mandante)]['partidas'] += 1
    if partida['vencedor'] == partida['mandante']:
        mandante_ano_dict[(ano, mandante)]['vitorias_casa'] += 1
    elif partida['vencedor'] == partida['visitante']:
        mandante_ano_dict[(ano, mandante)]['derrotas_casa'] += 1
    else:
        mandante_ano_dict[(ano, mandante)]['empates'] += 1

# Converter o dicionário em um DataFrame
mandante_ano_df = pd.DataFrame(mandante_ano_dict.values())

# Salvar o novo dataset
mandante_ano_df.to_csv('../data/processed/mandante_ano.csv', index=False)