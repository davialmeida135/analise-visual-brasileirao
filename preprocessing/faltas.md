```python
import pandas as pd

# Carrega csv com dados das partidas
partidas = pd.read_csv("../data/raw/campeonato-brasileiro-full.csv")

# Carrega csv com dados dos cartões
cartoes = pd.read_csv("../data/raw/campeonato-brasileiro-cartoes.csv")

# Renomeia coluna ID para partida_id para facilitar join de dataframes
partidas["partida_id"] = partidas["ID"]

# Junta os dois dataframes com base na coluna partida_id
cartoes_partidas = pd.merge(partidas, cartoes, on="partida_id", how="inner")

# Seleciona apenas colunas relevantes
final_df = cartoes_partidas[
    [
        "partida_id",
        "data",
        "vencedor",
        "mandante",
        "visitante",
        "clube",
        "cartao",
        "atleta",
        "posicao",
        "minuto",
    ]
]

# Adiciona uma coluna "resultado" para indicar se o clube do jogador ganhou, perdeu ou empatou a partida
for idx, row in final_df.iterrows():
    if row["vencedor"] == row["mandante"]:
        if row["clube"] == row["mandante"]:
            final_df.at[idx, "resultado"] = "Vitória"
        else:
            final_df.at[idx, "resultado"] = "Derrota"
    elif row["vencedor"] == row["visitante"]:
        if row["clube"] == row["visitante"]:
            final_df.at[idx, "resultado"] = "Vitória"
        else:
            final_df.at[idx, "resultado"] = "Derrota"
    else:
        final_df.at[idx, "resultado"] = "Empate"

# Exporta o dataframe final para um novo arquivo CSV
final_df.to_csv("../data/processed/analise_faltas.csv", index=False)

```