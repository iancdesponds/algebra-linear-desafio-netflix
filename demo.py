import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.linalg import svd, diagsvd
import random as rd

# Carrega os dados

df = pd.read_csv('data/ratings_small.csv')
df.drop(['timestamp'], axis=1, inplace=True)
df.head()

# Cria a matriz de ratings

A = df.pivot_table(index='userId', columns='movieId', values='rating').fillna(2.8)
# Preenche os valores NaN com 2.8 (Média, arredondada para uma casa decimal, entre 0.5 e 5, valores possíveis para rating)
A = A.to_numpy()

# Encontra o valor de k

u, s, v = svd(A) # Decomposição SVD da matriz A
# s é um array com os valores singulares de A

plt.figure(figsize=(10, 4))
plt.plot(s[15:]) # Ignora o primeiro valor singular, pois ele é muito maior que os outros
plt.xticks(range(0, len(s)-1, 25))
plt.xlabel('Número do valor singular')
plt.ylabel('Valor singular')
plt.text(120, 20, 'k = 100', fontsize=12, color='r')
plt.axvline(x=100, color='r', linestyle='--')
plt.title('Valores singulares')
plt.show()

k = 100

# Define as listas que armazenarão as posições selecionadas, os valores selecionados, os valores gerados e os valores simulados
posicoes_selecionadas = []
valores_selecionados = []
valores_gerados = []
valores_simulados = []

# Processo de seleção de posições aleatórias e geração de valores de rating
for i in range(0, 100):
    A_temp = A.copy()
    while True:
        # Seleciona uma posição aleatória na qual o valor não seja 2.8
        i = rd.randint(0, len(A) - 1)
        j = rd.randint(0, len(A[0]) - 1)
        if A_temp[i][j] != 2.8: # Se o valor for diferente de 2.8, a posição é válida, pois é uma avaliação real
            break
    
    posicoes_selecionadas.append((i, j)) # Armazena a posição selecionada
    valores_selecionados.append(A_temp[i][j]) # Armazena o valor selecionado
    valor_gerado = max((rd.random() * rd.randint(1, 5)), 0.5) # Gera um valor de rating entre 0.5 e 5
    A_temp[i][j] = valor_gerado # Substitui o valor original pelo valor gerado
    valores_gerados.append(valor_gerado) # Armazena o valor gerado

    # Processo de remoção de ruído
    U, S, V = svd(A_temp)
    k = 100 # Valor encontrado com o método do cotovelo, analisando o gráfico dos valores singulares
    S[k:] = (len(S)-k)*[0] # Apaga os k últimos valores singulares
    A_simulado = U @ diagsvd(S, len(A), len(A[0])) @ V
    valores_simulados.append(A_simulado[i][j]) # Armazena o valor simulado


erros = [valores_simulados[i] - valores_selecionados[i] for i in range(0, 100)] # Calcula os erros
erros_absolutos = [abs(valores_selecionados[i] - valores_simulados[i]) for i in range(0, 100)] # Calcula os erros absolutos

media_erros = sum(erros) / len(erros) # Calcula a média dos erros
media_erros_absolutos = sum(erros_absolutos) / len(erros_absolutos) # Calcula a média dos erros absolutos

# Salvando a informação em um arquivo csv
df = pd.DataFrame({'Posições selecionadas': posicoes_selecionadas, 'Valores selecionados': valores_selecionados, 'Valores gerados': valores_gerados, 'Valores simulados': valores_simulados, 'Erros': erros, 'Erros absolutos': erros_absolutos})
df.to_csv('data/erros_a_partir_k_100.csv', index=False) # Salvando o DataFrame em um arquivo CSV

# Exibindo os resultados

print('Média dos erros:', media_erros)
print('Média dos erros absolutos:', media_erros_absolutos)

# Histograma dos erros

df = pd.read_csv('data/erros_a_partir_k_100.csv')
df.head()

plt.figure(figsize=(10, 5))
plt.hist(df['Erros absolutos'], bins=15, edgecolor='black')
plt.xticks(range(0, 6))
plt.xlabel('Erro absoluto')
plt.ylabel('Frequência')
plt.title('Histograma dos erros absolutos')
plt.savefig('data/img/histograma_erros_absolutos.png') # Salva o gráfico em um arquivo

plt.figure(figsize=(10, 5))
plt.hist(df['Erros'], bins=15, edgecolor='black')
plt.xticks(range(-5, 6))
plt.xlabel('Erro')
plt.yticks(range(0, 20, 2))
plt.ylabel('Frequência')
plt.title('Histograma dos erros') 
plt.savefig('data/img/histograma_erros.png') # Salva o gráfico em um arquivo

