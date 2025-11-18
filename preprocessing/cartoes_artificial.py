import pandas as pd
import random

# Definir os valores possíveis para cada variável
clubes = [f"Clube {i}" for i in range(1, 21)]
posicoes = ['Goleiro', 'Defensor', 'Meio-Campo', 'Atacante']

# Gerar dados sintéticos
n = 1000  # Número de registros no dataset
data = {
    'Quantidade Cartões': [random.randint(0, 50) for _ in range(n)],
    'Minuto do jogo': [random.randint(1, 90) for _ in range(n)],
    'Clube': [random.choice(clubes) for _ in range(n)],
    'Posição do jogador': [random.choice(posicoes) for _ in range(n)],
    'Taxa de Vitórias': [round(random.uniform(0, 1), 2) for _ in range(n)]
}

# Criar o DataFrame
df = pd.DataFrame(data)
df.drop_duplicates(subset=['Minuto do jogo', 'Clube', 'Posição do jogador'], inplace=True)
# Exibir as primeiras linhas do dataset
print(df.head())

# Salvar o dataset em um arquivo CSV (opcional)
df.to_csv('dataset_sintetico.csv', index=False)