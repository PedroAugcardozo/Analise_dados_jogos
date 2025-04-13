import pandas as pd
import matplotlib.pyplot as plt

# ! chama todas as planilhas
interCalouros2024 = pd.read_excel("trabalho.proba(2).xlsx", sheet_name="InterCalouros2024")
interCalouros2023 = pd.read_excel("trabalho.proba(2).xlsx", sheet_name="InterCalouros2023")
interCursos2024 = pd.read_excel("trabalho.proba(2).xlsx", sheet_name="InterCursos2024")

# ! garante que todos nessa coluna seja uma string
interCalouros2024['Cursos'] = interCalouros2024['Cursos'].astype(str)
interCalouros2023['Cursos'] = interCalouros2023['Cursos'].astype(str)
interCursos2024['Cursos'] = interCursos2024['Cursos'].astype(str)


# ! concatena todas as colunas de saldo de gols e dos times
todos_campeonatos = pd.concat([interCalouros2024, interCalouros2023, interCursos2024], keys=["InterCalouros2024", "InterCalouros2023", "InterCursos2024"])
saldo_total_por_time = todos_campeonatos.groupby("Cursos")["Saldo de gols futsal"].sum().reset_index()

plt.figure(figsize=(10,6))

plt.bar(saldo_total_por_time["Cursos"], saldo_total_por_time["Saldo de gols futsal"], color='skyblue')

plt.xticks(rotation=90)  # Rotaciona os rótulos dos times
plt.title("Saldo Total de Gols por Time")
plt.xlabel("Time")
plt.ylabel("Saldo Total de Gols")

plt.tight_layout()  # Ajusta o layout para não cortar rótulos
plt.show()

# ! calcula a media do saldo de gols
media_gols_futsal = saldo_total_por_time["Saldo de gols futsal"].mean()
media_gols_futsal = round(media_gols_futsal, 2)
print(media_gols_futsal)

# ! aqui eu vou pegar o numero de vitorias totais de cada time
df_total = pd.concat([interCalouros2023, interCalouros2024, interCursos2024])

pontos_por_time = df_total.groupby('Cursos')['Pontuação Classificação Geral'].sum()

plt.figure(figsize=(10,10))
plt.barh(pontos_por_time.index, pontos_por_time, color='skyblue')
plt.xlabel('pontos totais')
plt.ylabel('time')
plt.title("distribuição totais por time")
plt.gca().invert_yaxis()
plt.show()

# ! ve quantos % cada time conseguiu de todos que poderia
pontos_possiveis = 273
porcentagem_pontos = (pontos_por_time/pontos_possiveis*100).round(2)

# ! saldo basquete 


# Converte a coluna 'saldo de pontos basquete' para numérico, substituindo valores não numéricos por NaN
df_total['saldo de pontos basquete'] = pd.to_numeric(df_total['saldo de pontos basquete'], errors='coerce')
# Substitui os NaN por 0
df_total['saldo de pontos basquete'].fillna(0, inplace=True)

# Realiza a soma dos pontos de basquete por curso
pontos_basquete = df_total.groupby('Cursos')['saldo de pontos basquete'].sum()

plt.figure(figsize=(10,10))
plt.barh(pontos_basquete.index, pontos_basquete, color='black')
plt.xlabel('pontos totais')
plt.ylabel('time')
plt.title("distribuição totais por time")
plt.gca().invert_yaxis()
plt.show()


#! compara dois times em todas as categorias

# Remove a coluna "Pontuação classificação" do DataFrame antes de gerar o gráfico
df_total_sem_pontuacao = df_total.drop(columns=["Pontuação classificação"])

# Agrupar por 'Cursos' (times) e somar as colunas de modalidades
df_total_agrupado = df_total.groupby("Cursos").sum(numeric_only=True)


times_para_comparar = ['Medicina', 'Educação fisica']

# Filtrar o DataFrame consolidado para incluir apenas os dois times
df_comparacao = df_total_agrupado.loc[times_para_comparar]

df_comparacao_transposto = df_comparacao.T

df_comparacao_transposto.plot(kind='bar', figsize=(14, 8))
plt.title("Comparação de Resultados por Modalidade entre FIPP e Medicina")
plt.xlabel("Modalidade")
plt.ylabel("Resultado")
plt.xticks(rotation=90)
plt.legend(title="Times")
plt.show()


#! grafico do numero de vitorias de cada time

# Selecionar todas as colunas que têm "vitórias" no nome
colunas_vitorias = [col for col in df_total.columns if "vitorias" in col.lower()]

# Somar as colunas de vitórias para cada time
df_total["Total_Vitorias"] = df_total[colunas_vitorias].sum(axis=1)

df_total.groupby("Cursos")["Total_Vitorias"].sum().plot(kind="bar", title="Total de Vitórias por Time")
plt.xlabel("Cursos")
plt.ylabel("Total de Vitórias")
plt.show()

#!soma do saldo de gols do futebol

# Selecionar todas as colunas que têm "Saldo de gols futebol" no nome
# Identificar todas as colunas que contêm "saldo de gols futebol" no nome, ignorando maiúsculas/minúsculas
colunas_saldo_gols = [col for col in df_total.columns if "saldo de gols futebol" in col.lower()]

# Verificar as colunas identificadas
print("Colunas de saldo de gols futebol identificadas:", colunas_saldo_gols)

# Certifique-se de que colunas foram encontradas
if colunas_saldo_gols:
    # Somar as colunas de saldo de gols para cada time e adicionar ao DataFrame
    df_total["Total_Saldo_Gols_Futebol"] = df_total[colunas_saldo_gols].sum(axis=1)

    # Gerar o gráfico de barras com a soma total para cada time
    df_total.groupby("Cursos")["Total_Saldo_Gols_Futebol"].sum().plot(kind="bar", title="Total de Saldo de Gols no Futebol por Time")
    plt.xlabel("Cursos")
    plt.ylabel("Total Saldo de Gols")
    plt.show()
else:
    print("Nenhuma coluna de 'Saldo de gols futebol' foi encontrada.")


#! quantos times deram W.O

# Criar uma nova coluna para armazenar o número de W.O. para cada time
df_total["Total_WO"] = df_total.apply(lambda row: row.astype(str).str.count("W.O").sum(), axis=1)


# Plotar o gráfico de W.O.
df_total.set_index("Cursos")["Total_WO"].plot(kind="bar", title="Total de W.O. por Time")
plt.xlabel("Cursos")
plt.ylabel("Total de W.O.")
plt.show()

#! quantas N.P cada time teve
# Criar uma nova coluna para armazenar o número de W.O. para cada time
df_total["Total_NP"] = df_total.apply(lambda row: row.astype(str).str.count("N.P").sum(), axis=1)


# Plotar o gráfico de W.O.
df_total.set_index("Cursos")["Total_NP"].plot(kind="bar", title="Total de N.P. por Time")
plt.xlabel("Cursos")
plt.ylabel("Total de W.O.")
plt.show()