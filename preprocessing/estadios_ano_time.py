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
    mandante = partida['mandante']

    if (estadio, ano, mandante) not in estadios_ano_dict:
        estadios_ano_dict[(estadio, ano, mandante)] = {
            'estadio': estadio,
            'ano': ano,
            'mandante': mandante,
            'partidas': 0,
            'vitorias_casa': 0,
            'vitorias_fora': 0,
            'empates': 0,
        }
    
    # Atualizar as estatísticas
    estadios_ano_dict[(estadio, ano, mandante)]['partidas'] += 1
    if partida['vencedor'] == partida['mandante']:
        estadios_ano_dict[(estadio, ano, mandante)]['vitorias_casa'] += 1
    elif partida['vencedor'] == partida['visitante']:
        estadios_ano_dict[(estadio, ano, mandante)]['vitorias_fora'] += 1
    else:
        estadios_ano_dict[(estadio, ano, mandante)]['empates'] += 1

# Converter o dicionário em um DataFrame
estadios_ano_df = pd.DataFrame(estadios_ano_dict.values())

# Salvar o novo dataset
estadios_ano_df.to_csv('../data/processed/estadios_ano_mandante.csv', index=False)