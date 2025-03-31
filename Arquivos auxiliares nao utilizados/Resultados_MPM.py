# %% [markdown]
# # Importar

# %%
import pandas as pd
import numpy as np

from datetime import timedelta, date
pd.options.display.max_rows = 500

# %%
mes_atual = date.today().month
ano_atual = date.today().year
data_atual = str(ano_atual) + str.zfill(str(mes_atual), 2)

# %%
caminho_arquivo = r"C:\Users\lfmelo\Documents\Demanda MPM\Tabelas\PLANILHA DADOS COMPARATIVOS JN X MPM - LAÍS.ods"

# Lê todas as planilhas do arquivo
planilhas = pd.read_excel(caminho_arquivo, sheet_name=None, engine="odf", dtype=str)

dfs_planilha = {}

for nome_planilha, df in planilhas.items():
    dfs_planilha[nome_planilha] = df.copy()

# %%
dfs_planilha.keys()

# %%
df_servidores = dfs_planilha['Dados SERVIDORES Ativos TJGO']
df_magistrados = dfs_planilha['Dados MAGISTRADOS ativos TJGO']
df_serventias = dfs_planilha['Dados SERVENTIAS TJGO']

# %%
caminho_arquivo = r"C:\Users\lfmelo\Documents\Demanda MPM\Tabelas\Perguntas - MPM X JUSTIÇA.ods"

# Lê todas as planilhas do arquivo
planilhas = pd.read_excel(caminho_arquivo, sheet_name=None, engine="odf", dtype=str)

dfs_planilha_variaveis = {}

for nome_planilha, df in planilhas.items():
    dfs_planilha_variaveis[nome_planilha] = df.copy()

# %%
dfs_planilha_variaveis.keys()

# %%
df_variaveis_servidores = dfs_planilha_variaveis["Questionário - Servidores"]
df_variaveis_magistrados = dfs_planilha_variaveis["Questionário - Magistrados"]
df_variaveis_auxiliares = dfs_planilha_variaveis["Questionário - Auxiliares"]

# %%
import os

caminho_pasta = f"C:\\Users\\lfmelo\\Documents\\Demanda MPM\\Dados\\MPM_{data_atual}"

# Criar a pasta (não gera erro se já existir)
os.makedirs(caminho_pasta, exist_ok=True)

# %%
df_servidores.to_csv(f"C:\\Users\\lfmelo\\Documents\\Demanda MPM\\Dados\\MPM_{data_atual}\\dados_servidores_{data_atual}.csv", index=False)
df_magistrados.to_csv(f"C:\\Users\\lfmelo\\Documents\\Demanda MPM\\Dados\\MPM_{data_atual}\\dados_magistrados_{data_atual}.csv", index=False)
df_serventias.to_csv(f"C:\\Users\\lfmelo\\Documents\\Demanda MPM\\Dados\\MPM_{data_atual}\\dados_serventias_{data_atual}.csv", index=False)

# %%
df_situ_prof = {'Situação profissional atual' : [1,2,3,6,7,8,9,10,11,12,13],
                'Descrição Situação profissional atual' : ['Cargo de chefia',
                                                           'Outros cargos em comissão ou funções comissionadas',
                                                           'Não exerce cargo em comissão ou função comissionada',
                                                           'Afastado(a)', 'Aposentado(a)','Falecido(a)',
                                                           'Exoneração/Vacância', 'Demitido(a)', 'Saída por Remoção',
                                                           'Saída por cessão/requisição',
                                                           'Vigência de Contrato/Vínculo (opção destinada a todas as forças auxiliares, inclusive terceirizados(as))']}

df_ident_genero = {'Identidade de gênero' : [1,2,3,4,5,6,7,8,9],
                   'Descrição Identidade de gênero' : ['Cisgênero (pessoas que se identificam com o sexo biológico com o qual nasceram)',
                                                      'Transgênero (pessoas cuja identidade de gênero difere, em diferentes graus, do sexo biológico atribuído ao nascer)',
                                                      'Transexual (pessoas que se identificam com um gênero diferente do sexo biológico com o qual nasceram e que procuram se adequar à sua identidade de gênero, podendo se submeter a tratamentos hormonais ou cirúrgicos)',
                                                      'Travesti (pessoas que buscam se expressar através de elementos associados ao sexo oposto - ex: nomes, corte de cabelo, roupas, acessórios, expressões corporais e etc)',
                                                      'Gênero fluido (pessoas que não se identificam com um único papel ou identidade de gênero)',
                                                      'Agênero (ausência de identidade de gênero)',
                                                      'Outra',
                                                      'Não Informado',
                                                      'Não Declarado pelo Respondente']}

# %% [markdown]
# # Análises independentes

# %%
# Análise dos dados duplicados
df_duplicadas_servidores = df_servidores.duplicated(subset='CPF', keep='first')
df_duplicadas_servidores = df_servidores[df_duplicadas_servidores]

# %% [markdown]
# # Tratamento dos dados

# %%
df_variaveis_servidores = df_variaveis_servidores.rename(columns=df_variaveis_servidores.iloc[0]).drop(df_variaveis_servidores.index[0])
df_variaveis_magistrados = df_variaveis_magistrados.rename(columns=df_variaveis_magistrados.iloc[0]).drop(df_variaveis_magistrados.index[0])
df_variaveis_auxiliares = df_variaveis_auxiliares.rename(columns=df_variaveis_auxiliares.iloc[0]).drop(df_variaveis_auxiliares.index[0])

# %%
df_variaveis_servidores = df_variaveis_servidores[['Nº','DESCRIÇÃO DA PERGUNTA','RESPOSTA NUMÉRICA']]
df_variaveis_magistrados = df_variaveis_magistrados[['Nº', 'DESCRIÇÃO DA PERGUNTA', 'RESPOSTA NUMÉRICA']]
df_variaveis_auxiliares = df_variaveis_auxiliares[['Nº', 'DESCRIÇÃO DA PERGUNTA', 'RESPOSTA NUMÉRICA']]

# %%
df_servidores.loc[:, 'Data de início da situação'] = pd.to_datetime(df_servidores['Data de início da situação'], format='%d/%m/%Y')
df_servidores.loc[:, 'Data posse'] = pd.to_datetime(df_servidores['Data posse'], format='%d/%m/%Y')
df_servidores.loc[:, 'Data de saída da situação'] = pd.to_datetime(df_servidores['Data de saída da situação'], format='%d/%m/%Y')

df_servidores['Data de início da situação'] = df_servidores['Data de início da situação'].apply(lambda x: x.date())
df_servidores['Data posse'] = df_servidores['Data posse'].apply(lambda x: x.date())
df_servidores['Data de saída da situação'] = df_servidores['Data de saída da situação'].apply(lambda x: x.date())

# %%
# Criada uma nova coluna chamada 'Data de início da situação - TRATADA' para corrigir datas que são anteriores a 2024
df_servidores['Data de início da situação - TRATADA'] = df_servidores['Data de início da situação'].apply(lambda x: date(2024,1,1) if x < date(2024,1,1) else x)

# Substituimos datas nulas por 31/12/2024
df_servidores['Data de saída da situação'] = df_servidores['Data de saída da situação'].fillna(date(2024,12,31))

# Criada uma nova coluna chamada 'Data de saída da situação - TRATADA' para corrigir datas que são posteriores a 2024
df_servidores['Data de saída da situação - TRATADA'] = df_servidores['Data de saída da situação'].apply(lambda x: date(2024,12,31) if x > date(2024,12,31) else x)

# %%
df_servidores = df_servidores[df_servidores['Data de início da situação'] < date(2025,1,1)]

# %%
df_servidores['Tempo de afastamento'] = df_servidores['Data de saída da situação - TRATADA'] - df_servidores['Data de início da situação - TRATADA']

# %%
df_serventia_para_merge = df_serventias[['Código Serventia','Classificação da Unidade Judiciária']].drop_duplicates()

df_servidor_Serventia = pd.merge(df_servidores,df_serventia_para_merge,how='left',left_on='Órgão de lotação do(a) Servidor(a) ou AuxiliarCódigo CNJ',right_on='Código Serventia')

# %%
# Dado pedido pela Carina

#df_servidor_Serventia[df_servidor_Serventia['Classificação da Unidade Judiciária'] == 103]
#len(df_servidor_Serventia[df_servidor_Serventia['Classificação da Unidade Judiciária'] == 103]['CPF'].unique())

# %%
df_servidor_Serventia['Classificação da Unidade Judiciária'] = df_servidor_Serventia['Classificação da Unidade Judiciária'].astype(str)
df_grouped_serventia = df_servidor_Serventia.groupby(['CPF'])['Classificação da Unidade Judiciária'].apply(lambda x: ' - '.join(x)).reset_index()

# %%
#Lista de órgãos que não estão na tabela de serventias
df_servidor_Serventia[df_servidor_Serventia['Código Serventia'].isna()]['Órgão de lotação do(a) Servidor(a) ou AuxiliarCódigo CNJ'].unique()

# %%
df_serventia_UJ2 = df_serventias[df_serventias['Tipo de Unidade Judiciária'] == 'UJ2']['Código Serventia'].unique()

# %% [markdown]
# # Servidores

# %% [markdown]
# ## Número 1

# %%
N_1_df = df_servidores[(df_servidores['Cargo'] == '1')]
N_1 = len(N_1_df['Cargo'])
N_1 ######################## ?

# %% [markdown]
# ## Número 2

# %%
N_2_df = df_servidores[(df_servidores['Cargo'] == '1') & 
              (df_servidores['Área de atuação'] == '5') & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]
N_2 = len(N_2_df[~(N_2_df['Situação profissional atual'].isin(['11','12']))]['CPF'].unique())
N_2

# %%
df_servidores['Situação profissional atual'].unique()

# %% [markdown]
# ## Número 3

# %%
df_Juizado_Especial_Adjunto = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='102']
cpf_Juizado_Especial_Adjunto = df_Juizado_Especial_Adjunto['CPF'].unique()

# %%
N_3_df = df_servidores[(df_servidores['Cargo'] == '1') & 
              (df_servidores['Área de atuação'] == '4') & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31)) &
              ~(df_servidores['CPF'].isin(cpf_Juizado_Especial_Adjunto))]
N_3 = len(N_3_df[(~(N_3_df['Situação profissional atual'].isin(['11','12'])))]['CPF'].unique())
N_3

# %% [markdown]
# ## Número 4

# %%
df_serventia_Turmas_Recusais = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='104']
cpf_Turmas_Recursais = df_serventia_Turmas_Recusais['CPF'].unique()

# %%
N_4_df = df_servidores[(df_servidores['Cargo'] == '1') & 
              (df_servidores['Área de atuação'].isin(['4','5'])) & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31)) &
              (df_servidores['CPF'].isin(cpf_Turmas_Recursais))]
N_4 = len(N_4_df[(~(N_4_df['Situação profissional atual'].isin(['11','12'])))]['CPF'].unique())
N_4

# %% [markdown]
# ## Número 5

# %%
df_Juizado_Especial_Exclusivo = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='103']
cpf_Juizado_Especial_Exclusivo = df_Juizado_Especial_Exclusivo['CPF'].unique()

# %%
df_Juizado_Especial_Adjunto = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='102']
cpf_Juizado_Especial_Adjunto = df_Juizado_Especial_Adjunto['CPF'].unique()

# %%
N_5_df = df_servidores[(df_servidores['Cargo'] == '1') & 
              (df_servidores['Área de atuação'].isin(['4','5'])) & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31)) &
              (df_servidores['CPF'].isin(cpf_Juizado_Especial_Exclusivo))]
N_5 = len(N_5_df[(~(N_5_df['Situação profissional atual'].isin(['11','12']))) & ~(N_5_df['CPF'].isin(cpf_Juizado_Especial_Adjunto))]['CPF'].unique())
N_5

# %% [markdown]
# ## Número 6

# %%
df_serventia_Juizado_Especial = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária'].str.contains(r'101&102|101&103|101&104|102')]

cpf_Juizado_Especial = df_serventia_Juizado_Especial['CPF'].unique()

# %%
N_6_df = df_servidores[(df_servidores['Cargo'] == '1') & 
              (df_servidores['Área de atuação'] == '4') & 
              (~(df_servidores['Situação profissional atual'].isin(['11','12']))) & # perguntar se é acumuladamente ou não
               (df_servidores['CPF'].isin(cpf_Juizado_Especial))]
#N_6_df
N_6 = len(N_6_df['CPF'].unique())
N_6

# %% [markdown]
# ## Número 7

# %%
N_7_df = df_servidores[(df_servidores['Cargo'] == '1') & 
              (df_servidores['Área de atuação'].isin(['1','2','3'])) & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]
N_7 = len(N_7_df[~(N_7_df['Situação profissional atual'].isin(['11','12']))]['CPF'].unique())
N_7

# %% [markdown]
# ## Número 8

# %%
N_8_df = df_servidores[(df_servidores['Cargo'].isin(['2','3'])) & 
              (df_servidores['Área de atuação'].isin(['5'])) & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]
N_8 = len(N_8_df['CPF'].unique())
N_8

# %% [markdown]
# ## Número 9

# %%
df_Juizado_Especial_Adjunto = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='102']
cpf_Juizado_Especial_Adjunto = df_Juizado_Especial_Adjunto['CPF'].unique()

# %%
N_9_df = df_servidores[(df_servidores['Cargo'].isin(['2','3'])) & 
              (df_servidores['Área de atuação'].isin(['4'])) & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]
N_9 = len(N_9_df[~N_9_df['CPF'].isin(cpf_Juizado_Especial_Adjunto)]['CPF'].unique())
N_9

# %% [markdown]
# ## Número 10

# %%
df_serventia_Turmas_Recusais = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='104']
cpf_Turmas_Recursais = df_serventia_Turmas_Recusais['CPF'].unique()

# %%
N_10_df = df_servidores[(df_servidores['Cargo'].isin(['2','3'])) & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]
N_10 = len(N_10_df[N_10_df['CPF'].isin(cpf_Turmas_Recursais)]['CPF'].unique())
N_10

# %% [markdown]
# ## Número 11

# %%
df_Juizado_Especial_Exclusivo = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='103']
cpf_Juizado_Especial_Exclusivo = df_Juizado_Especial_Exclusivo['CPF'].unique()

# %%
df_Juizado_Especial_Adjunto = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='102']
cpf_Juizado_Especial_Adjunto = df_Juizado_Especial_Adjunto['CPF'].unique()

# %%
N_11_df = df_servidores[(df_servidores['Cargo'].isin(['2','3'])) & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31)) &
              (df_servidores['CPF'].isin(cpf_Juizado_Especial_Exclusivo))]
N_11 = len(N_11_df[~N_11_df['CPF'].isin(cpf_Juizado_Especial_Adjunto)]['CPF'].unique())
N_11

# %% [markdown]
# ## Número 12

# %%
df_Juizado_Especial_Exclusivo = df_grouped_serventia[(df_grouped_serventia['Classificação da Unidade Judiciária'].str.contains(r'103')) | 
                                                     (df_grouped_serventia['Classificação da Unidade Judiciária']=='102')]
cpf_Juizado_Especial_Exclusivo = df_Juizado_Especial_Exclusivo['CPF'].unique()

# %%
df_Juizado_Especial_Exclusivo['Classificação da Unidade Judiciária'].unique()

# %%
N_12_df = df_servidores[(df_servidores['Cargo'].isin(['2','3'])) & 
                (df_servidores['Área de atuação'].isin(['4'])) &
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31)) &
              (df_servidores['CPF'].isin(cpf_Juizado_Especial_Exclusivo))]
N_12 = len(N_12_df['CPF'].unique())
N_12

# %% [markdown]
# ## Número 13

# %%
N_13_df = df_servidores[(df_servidores['Cargo'].isin(['2','3'])) & 
                (df_servidores['Área de atuação'].isin(['1','2','3'])) &
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]
N_13 = len(N_13_df['CPF'].unique())
N_13

# %% [markdown]
# ## Número 14

# %%
N_14_df = df_servidores[(df_servidores['Cargo'].isin(['4'])) & 
                (df_servidores['Área de atuação'].isin(['5'])) &
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]
N_14 = len(N_14_df['CPF'].unique())
N_14

# %% [markdown]
# ## Número 15

# %%
df_Juizado_Especial_Adjunto = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='102']
cpf_Juizado_Especial_Adjunto = df_Juizado_Especial_Adjunto['CPF'].unique()

# %%
N_15_df = df_servidores[(df_servidores['Cargo'].isin(['4'])) & 
                (df_servidores['Área de atuação'].isin(['4'])) &
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]
N_15 = len(N_15_df[~N_15_df['CPF'].isin(cpf_Juizado_Especial_Adjunto)]['CPF'].unique())
N_15

# %% [markdown]
# ## Número 16

# %%
df_serventia_Turmas_Recusais = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='104']
cpf_Turmas_Recursais = df_serventia_Turmas_Recusais['CPF'].unique()

# %%
N_16_df = df_servidores[(df_servidores['Cargo'].isin(['4'])) & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]
N_16 = len(N_16_df[N_16_df['CPF'].isin(cpf_Turmas_Recursais)]['CPF'].unique())
N_16

# %% [markdown]
# ## Número 17

# %%
df_Juizado_Especial_Exclusivo = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='103']
cpf_Juizado_Especial_Exclusivo = df_Juizado_Especial_Exclusivo['CPF'].unique()

# %%
df_Juizado_Especial_Adjunto = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária']=='102']
cpf_Juizado_Especial_Adjunto = df_Juizado_Especial_Adjunto['CPF'].unique()

# %%
N_17_df = df_servidores[(df_servidores['Cargo'].isin(['4'])) & 
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31)) &
              (df_servidores['CPF'].isin(cpf_Juizado_Especial_Exclusivo))]
N_17 = len(N_17_df[~N_17_df['CPF'].isin(cpf_Juizado_Especial_Adjunto)]['CPF'].unique())
N_17

# %% [markdown]
# ## Número 18

# %%
df_serventia_Juizado_Especial = df_grouped_serventia[(df_grouped_serventia['Classificação da Unidade Judiciária'].str.contains(r'101&102|101&103|101&104')) |
                                                     (df_grouped_serventia['Classificação da Unidade Judiciária'] == '102')]

cpf_Juizado_Especial = df_serventia_Juizado_Especial['CPF'].unique()

# %%
N_18_df = df_servidores[(df_servidores['Cargo'] == '4') & 
              (df_servidores['Área de atuação'] == '4') & 
               (df_servidores['CPF'].isin(cpf_Juizado_Especial))]
# N_18_df
N_18 = len(N_18_df['CPF'].unique())
N_18

# %% [markdown]
# ## Número 19

# %%
N_19_df = df_servidores[(df_servidores['Cargo'].isin(['4'])) & 
                (df_servidores['Área de atuação'].isin(['1','2','3'])) &
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]
N_19 = len(N_19_df['CPF'].unique())
N_19

# %% [markdown]
# ## Número 20

# %%
df_servidores['Situação profissional atual'] = df_servidores['Situação profissional atual'].astype(str)
df_grouped_situ_serv = df_servidores.groupby(['CPF'])['Situação profissional atual'].apply(lambda x: ' - '.join(x)).reset_index()

df_servidores_situacao_11_12 = df_grouped_situ_serv[df_grouped_situ_serv['Situação profissional atual'].str.contains(r'11|12')]

cpf_servidores_situacao_11_12 = df_servidores_situacao_11_12['CPF'].unique()

# %%
df_servidores_situacao_11_12

# %%
N_20_df = df_servidores[(df_servidores['Cargo'].isin(['1','2','3','4'])) & 
              (df_servidores['Área de atuação'] == '5') & 
              (df_servidores['Situação profissional atual'].isin(['6'])) & 
               (~(df_servidores['Situação profissional atual'].isin([cpf_servidores_situacao_11_12])))]

# %%
N_20 = N_20_df['Tempo de afastamento'].sum()

if N_20 == 0:
    N_20 = 0
else:   
    N_20 = int(N_20.days)
N_20

# %% [markdown]
# ## Número 21

# %%
N_21_df = df_servidores[(df_servidores['Cargo'].isin(['1','2','3','4'])) & 
              (df_servidores['Área de atuação'] == '4') & 
              (df_servidores['Situação profissional atual'].isin(['6'])) & 
               (~(df_servidores['Situação profissional atual'].isin(cpf_servidores_situacao_11_12)))]


len(N_21_df['CPF'].unique())
N_21 = N_21_df['Tempo de afastamento'].sum()

if N_21 == 0:
    N_21 = 0
else:   
    N_21 = int(N_21.days)
N_21

# %% [markdown]
# ## Número 22

# %%
df_serventia_Turmas_Recusais = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária'].str.contains(r'104')]
cpf_Turmas_Recursais = df_serventia_Turmas_Recusais['CPF'].unique()

# %%
N_22_df = df_servidores[(df_servidores['Cargo'].isin(['1','2','3','4']))]

len(N_22_df['CPF'].unique())

# %%
N_22_df = df_servidores[(df_servidores['Cargo'].isin(['1','2','3','4'])) & 
              (df_servidores['CPF'].isin(cpf_Turmas_Recursais))]

len(N_22_df['CPF'].unique())

# %%
N_22_df['Situação profissional atual'].unique()

# %%
N_22_df = df_servidores[(df_servidores['Cargo'].isin(['1','2','3','4'])) & 
              (df_servidores['CPF'].isin(cpf_Turmas_Recursais)) & 
              (df_servidores['Situação profissional atual'].isin(['6']))]

len(N_22_df['CPF'].unique())

# %%
N_22_df = df_servidores[(df_servidores['Cargo'].isin(['1','2','3','4'])) & 
              (df_servidores['CPF'].isin(cpf_Turmas_Recursais)) & 
              (df_servidores['Situação profissional atual'].isin(['6'])) &
               (~(df_servidores['Situação profissional atual'].isin(cpf_servidores_situacao_11_12)))]

len(N_22_df['CPF'].unique())

# %%
N_22_df = df_servidores[(df_servidores['Cargo'].isin(['1','2','3','4'])) & 
              (df_servidores['CPF'].isin(cpf_Turmas_Recursais)) & 
              (df_servidores['Situação profissional atual'].isin(['6'])) &
               (~(df_servidores['Situação profissional atual'].isin(cpf_servidores_situacao_11_12)))]


len(N_22_df['CPF'].unique())
N_22 = N_22_df['Tempo de afastamento'].sum()

if N_22 == 0:
    N_22 = 0
else:   
    N_22 = int(N_22.days)
N_22

# %% [markdown]
# ## Número 23

# %%
df_Juizado_Especial_Exclusivo = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária'].str.contains(r'103')]
cpf_Juizado_Especial_Exclusivo = df_Juizado_Especial_Exclusivo['CPF'].unique()

# %%
N_23_df = df_servidores[(df_servidores['Cargo'].isin(['1','2','3','4'])) & 
              (df_servidores['CPF'].isin(cpf_Juizado_Especial_Exclusivo)) & 
              (df_servidores['Situação profissional atual'].isin(['6'])) & 
               (~(df_servidores['Situação profissional atual'].isin(cpf_servidores_situacao_11_12)))]


len(N_23_df['CPF'].unique())
N_23 = N_23_df['Tempo de afastamento'].sum()

if N_23 == 0:
    N_23 = 0
else:   
    N_23 = int(N_23.days)

# %% [markdown]
# ## Número 24

# %%
df_Juizado_Especial_Adjunto = df_grouped_serventia[df_grouped_serventia['Classificação da Unidade Judiciária'].str.contains(r'102')]
cpf_Juizado_Especial_Adjunto = df_Juizado_Especial_Adjunto['CPF'].unique()

# %%
N_24_df = df_servidores[(df_servidores['Cargo'].isin(['1','2','3','4'])) & 
            (df_servidores['CPF'].isin(cpf_Juizado_Especial_Adjunto)) &
              (df_servidores['Área de atuação'] == '4') & 
              (df_servidores['Situação profissional atual'].isin(['6'])) & 
               (~(df_servidores['Situação profissional atual'].isin(cpf_servidores_situacao_11_12)))]


len(N_24_df['CPF'].unique())
N_24 = N_24_df['Tempo de afastamento'].sum()

if N_24 == 0:
    N_24 = 0
else:   
    N_24 = int(N_24.days)
N_24

# %% [markdown]
# ## Número 25

# %%
N_25_df = df_servidores[(df_servidores['Cargo'].isin(['1','2','3','4'])) & 
              (df_servidores['Área de atuação'].isin(['1','2','3'])) & 
              (df_servidores['Situação profissional atual'].isin(['6'])) & 
               (~(df_servidores['Situação profissional atual'].isin(cpf_servidores_situacao_11_12)))]


len(N_25_df['CPF'].unique())
N_25 = N_25_df['Tempo de afastamento'].sum()

if N_25 == 0:
    N_25 = 0
else:   
    N_25 = int(N_25.days)
N_25

# %% [markdown]
# ## Número 26

# %%
N_26_df = df_servidores[(df_servidores['Cargo'].isin(['1'])) & 
               ((df_servidores['Situação profissional atual'].isin(cpf_servidores_situacao_11_12)))&
              (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]


N_26 = len(N_26_df['CPF'].unique())
N_26

# %% [markdown]
# ## Número 27

# %%
serv_aux_inativos = pd.read_excel(r"C:\Users\lfmelo\Documents\Demanda MPM\Tabelas\quadro_pessoal_e_auxiliar - com Inativos.xlsx",engine='openpyxl',dtype=str)

# %%
N_27_df = serv_aux_inativos[(serv_aux_inativos['Status'] == 'Inativo') &
               ((serv_aux_inativos['Situação profissional atual'].isin(['7','8','9','10']))) &
               (serv_aux_inativos['Data de saída da situação'].isna())]


N_27 = len(N_27_df['CPF'].unique())
N_27

# %% [markdown]
# ## Número 28

# %%
N_28_df = df_servidores[(df_servidores['Área de atuação'] == '3') &
                (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]


N_28 = len(N_28_df[~N_28_df['Situação profissional atual'].isin(['7','8','9','10','11','12'])]['CPF'].unique())
N_28

# %% [markdown]
# ## Número 29

# %%
N_29_df = df_servidores[(df_servidores['Área de atuação'] == '2') &
                (df_servidores['Data de saída da situação - TRATADA']==date(2024,12,31))]


N_29 = len(N_29_df[~N_29_df['Situação profissional atual'].isin(['7','8','9','10','11','12'])]['CPF'].unique())
N_29

# %% [markdown]
# ## Junção tabela Servidores

# %%
df_variaveis_servidores['RESPOSTA NUMÉRICA'] = df_variaveis_servidores['RESPOSTA NUMÉRICA'].replace({
    "547A DGP está retirando TI e Ejug?": "547",
    "92(A DGP está considerando TI e Ejug?)": "92",
    "350(A DGP está considerando TI e Ejug?)": "350"
})

df_variaveis_servidores['RESPOSTA NUMÉRICA'] = df_variaveis_servidores['RESPOSTA NUMÉRICA'].astype(int)

# %%
df_variaveis_servidores['TIPO'] = 'Servidores'
df_variaveis_servidores['MPM'] = [N_1,N_2,N_3,N_4,N_5,N_6,N_7,N_8,N_9,N_10,N_11,N_12,N_13,N_14,N_15,N_16,
                                  N_17,N_18,N_19,N_20,N_21,N_22,N_23,N_24,N_25,N_26,N_27,N_28,N_29]
df_variaveis_servidores['REFERÊNCIA'] = data_atual
df_variaveis_servidores['DIFERENÇA EM PERCENTUAL'] = round(((df_variaveis_servidores['MPM'] - df_variaveis_servidores['RESPOSTA NUMÉRICA']) / df_variaveis_servidores['RESPOSTA NUMÉRICA'])*100,2)

# Substituindo NaN e inf por 0
df_variaveis_servidores['DIFERENÇA EM PERCENTUAL'].replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# Opcional: Se você sabe que certos valores são anômalos, pode optar por removê-los
df_variaveis_servidores = df_variaveis_servidores[df_variaveis_servidores['DIFERENÇA EM PERCENTUAL'].between(-100, 100)]
df_variaveis_servidores['DIFERENÇA EM PERCENTUAL'] = round(df_variaveis_servidores['DIFERENÇA EM PERCENTUAL'],2)


df_variaveis_servidores.to_excel(f"C:\\Users\\lfmelo\\Documents\\Demanda MPM\\Dados\\MPM\\MPM_Servidores_{data_atual}.xlsx",engine='openpyxl',index=False) # Usar excel devido a quantidade de caracteres na coluna 'DESCRIÇÃO DA PERGUNTA'

# %% [markdown]
# # Magistrados

# %% [markdown]
# ## Tratamento tabela magistrados

# %%
df_magistrados_Serventia = pd.merge(df_magistrados,df_serventia_para_merge,how='left',left_on='Órgão de lotação do magistrado(a)',right_on='Código Serventia')
df_magistrados_Serventia['Classificação da Unidade Judiciária'] = df_magistrados_Serventia['Classificação da Unidade Judiciária'].astype(str)
df_magistrados_Serventia['Classificação da Unidade Judiciária'] = df_magistrados_Serventia['Classificação da Unidade Judiciária'].str.replace('.0','')

# %%
df_magistrados.loc[:, 'Data de início da situação'] = pd.to_datetime(df_magistrados['Data de início da situação'], format='%d/%m/%Y')
df_magistrados.loc[:, 'Data posse'] = pd.to_datetime(df_magistrados['Data posse'], format='%d/%m/%Y')
df_magistrados.loc[:, 'Data de saída da situação'] = pd.to_datetime(df_magistrados['Data de saída da situação'], format='%d/%m/%Y')

df_magistrados['Data de início da situação'] = df_magistrados['Data de início da situação'].apply(lambda x: x.date())
df_magistrados['Data posse'] = df_magistrados['Data posse'].apply(lambda x: x.date())
df_magistrados['Data de saída da situação'] = df_magistrados['Data de saída da situação'].apply(lambda x: x.date())

# %%
df_magistrados = df_magistrados[df_magistrados['Data de início da situação'] < date(2025,1,1)]
#df_magistrados = df_magistrados[df_magistrados['Data de saída da situação'] >= date(2024,1,1)]

# %%
# Criada uma nova coluna chamada 'Data de início da situação - TRATADA' para corrigir datas que são anteriores a 2024
df_magistrados['Data de início da situação - TRATADA'] = df_magistrados['Data de início da situação'].apply(lambda x: date(2024,1,1) if x < date(2024,1,1) else x)

# Substituimos datas nulas por 31/12/2024
df_magistrados['Data de saída da situação'] = df_magistrados['Data de saída da situação'].fillna(date(2024,12,31))

# Criada uma nova coluna chamada 'Data de saída da situação - TRATADA' para corrigir datas que são posteriores a 2024
df_magistrados['Data de saída da situação - TRATADA'] = df_magistrados['Data de saída da situação'].apply(lambda x: date(2024,12,31) if x > date(2024,12,31) else x)

# %%
df_magistrados_Serventia['Classificação da Unidade Judiciária'] = df_magistrados_Serventia['Classificação da Unidade Judiciária'].astype(str)
df_grouped_magis_serventia = df_magistrados_Serventia.groupby(['CPF'])['Classificação da Unidade Judiciária'].apply(lambda x: ' - '.join(x)).reset_index()

# %%
df_magistrados['Situação profissional atual'] = df_magistrados['Situação profissional atual'].apply(lambda x: str(x))
df_grouped_situ_magis = df_magistrados.groupby(['CPF'])['Situação profissional atual'].apply(lambda x: ' - '.join(x)).reset_index()

df_magistados_situacao_11_12 = df_grouped_situ_magis[df_grouped_situ_magis['Situação profissional atual'].str.contains(r'11|12')]

cpf_magistrados_situacao_11_12 = df_magistados_situacao_11_12['CPF'].unique()

# %% [markdown]
# ## Número 1

# %%
NM_1_df = df_magistrados[(df_magistrados['Cargo'].isin(['4','5','7','8','9','10'])) & 
                         (df_magistrados['Data de saída da situação - TRATADA']== date(2024,12,31))]
NM_1 = len(NM_1_df['CPF'].unique())
NM_1

# %% [markdown]
# ## Número 2

# %%
NM_2_df = df_magistrados[(df_magistrados['Cargo'].isin(['3'])) & 
                         (df_magistrados['Data de saída da situação - TRATADA']== date(2024,12,31))]
NM_2 = len(NM_2_df['CPF'].unique())
NM_2

# %% [markdown]
# ## Número 3

# %%
NM_3_df = df_magistrados[(df_magistrados['Cargo'].isin(['1','2'])) & 
                         (df_magistrados['Data de saída da situação - TRATADA']== date(2024,12,31))]
NM_3 = len(NM_3_df['CPF'].unique())
NM_3

# %% [markdown]
# ## Número 4

# %%
df_Juizado_especial = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'] == '103']
cpf_Juizado_especial = df_Juizado_especial['CPF'].unique()

# %%
NM_4_df = df_magistrados[(df_magistrados['Cargo'].isin(['1','2'])) & 
                         (df_magistrados['Data de saída da situação - TRATADA']== date(2024,12,31)) &
                        (df_magistrados['CPF'].isin(cpf_Juizado_especial))]
NM_4 = len(NM_4_df['CPF'].unique())
NM_4

# %% [markdown]
# ## Número 5

# %%
df_turmas_recursais = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'] == '104']
cpf_turmas_recursais = df_turmas_recursais['CPF'].unique()

# %%
NM_5_df = df_magistrados[(df_magistrados['Cargo'].isin(['1','2'])) & 
                         (df_magistrados['Data de saída da situação - TRATADA']== date(2024,12,31)) &
                        (df_magistrados['CPF'].isin(cpf_turmas_recursais))]
NM_5 = len(NM_5_df['CPF'].unique())
NM_5

# %% [markdown]
# ## Número 6

# %% [markdown]
# ### Tratamento magistrados inativos

# %%
df_magistrados_inativos = pd.read_excel(r"C:\Users\lfmelo\Documents\Demanda MPM\Tabelas\magistrados - com Inativos.xlsx",engine='openpyxl',dtype=str)
df_magistrados_inativos = df_magistrados_inativos.drop_duplicates()

# %%
df_magistrados_inativos.loc[:, 'Data de início da situação'] = pd.to_datetime(df_magistrados_inativos['Data de início da situação'], format='%d/%m/%Y')
df_magistrados_inativos.loc[:, 'Data de saída da situação'] = pd.to_datetime(df_magistrados_inativos['Data de saída da situação'], format='%d/%m/%Y')

df_magistrados_inativos['Data de início da situação'] = df_magistrados_inativos['Data de início da situação'].apply(lambda x: x.date())
df_magistrados_inativos['Data de saída da situação'] = df_magistrados_inativos['Data de saída da situação'].apply(lambda x: x.date())

# %%
df_magistrados_inativos = df_magistrados_inativos[df_magistrados_inativos['Data de início da situação'] < date(2025,1,1)]

# %% [markdown]
# ### Código

# %%
NM_6_df = df_magistrados_inativos[
    (df_magistrados_inativos['Status'] == 'Inativo') &
    (df_magistrados_inativos['Data de início da situação'] >= date(2024,1,1)) &
    (pd.isna(df_magistrados_inativos['Data de saída da situação'])) & 
    (df_magistrados_inativos['Situação profissional atual'].isin(['12','13','14','15']))
]

NM_6 = len(NM_6_df['CPF'].unique())
NM_6

# %% [markdown]
# ## Número 7

# %%
NM_7_df = df_magistrados[(df_magistrados['Cargo'].isin(['4','5','7','8','9','10'])) & (df_magistrados['Data de saída da situação - TRATADA']== date(2024,12,31))]
NM_7 = len(NM_7_df[~NM_7_df['Situação profissional atual'].isin(['12','13','14','15','17','19'])]['CPF'].unique())
NM_7

# %% [markdown]
# ## Número 8

# %%
NM_8_df = df_magistrados[(df_magistrados['Cargo'].isin(['3'])) & (df_magistrados['Data de saída da situação - TRATADA']== date(2024,12,31))]
NM_8 = len(NM_8_df[~NM_8_df['Situação profissional atual'].isin(['12','13','14','15','17','19'])]['CPF'].unique())
NM_8

# %% [markdown]
# ## Número 9

# %%
NM_9_df = df_magistrados[(df_magistrados['Cargo'].isin(['4','5','7','8','9','10'])) & (df_magistrados['Data de saída da situação - TRATADA']== date(2024,12,31))]
NM_9 = len(NM_9_df[NM_9_df['Situação profissional atual'].isin(['7','9','10','19'])]['CPF'].unique())
NM_9

# %% [markdown]
# ## Número 10

# %%
df_Juizado_especial_Turma_recursal = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'].str.contains(r'102|104')]

cpf_Juizado_especial_Turma_recursal = df_Juizado_especial_Turma_recursal['CPF'].unique()

# %%
NM_10_df = df_magistrados[(df_magistrados['Cargo'].isin(['1','2','6','11'])) & 
              (df_magistrados['Situação profissional atual'].isin(['7','8','9','10','19'])) & 
               (~(df_magistrados['CPF'].isin(cpf_Juizado_especial_Turma_recursal))) &
               (df_magistrados['Data de saída da situação - TRATADA'] == date(2024,12,31))]


NM_10 = len(NM_10_df['CPF'].unique())
NM_10

# %%
NM_10_df.tail()

# %%
teste = NM_10_df.groupby('CPF')['Órgão de lotação do magistrado(a)'].count().reset_index()
teste[teste['Órgão de lotação do magistrado(a)'] > 1]

# %% [markdown]
# ## Número 11

# %%
df_Juizado_especial_adjunto = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'].str.contains(r'102')]
cpf_Juizado_especial_adjunto = df_Juizado_especial_adjunto['CPF'].unique()

df_Turma_recursal = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'].str.contains(r'104')]
cpf_Turma_recursal = df_Turma_recursal['CPF'].unique()

# %%
NM_11_df = df_magistrados[(df_magistrados['CPF'].isin(cpf_Turma_recursal)) & 
              (df_magistrados['Situação profissional atual'].isin(['7','8','9','10','19'])) & 
               (~(df_magistrados['CPF'].isin(cpf_Juizado_especial_adjunto)))&
               (df_magistrados['Data de saída da situação - TRATADA'] == date(2024,12,31))]


NM_11 = len(NM_11_df['CPF'].unique())
NM_11

# %%
teste = NM_11_df.groupby('CPF')['Órgão de lotação do magistrado(a)'].count().reset_index()
teste[teste['Órgão de lotação do magistrado(a)'] > 1]

# %% [markdown]
# ## Número 12

# %%
df_Juizado_especial = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'].str.contains(r'103')]
cpf_Juizado_especial = df_Juizado_especial['CPF'].unique()

# %%
NM_12_df = df_magistrados[(df_magistrados['CPF'].isin(cpf_Juizado_especial)) & 
              (df_magistrados['Situação profissional atual'].isin(['7','8','9','10','19'])) & 
               (~(df_magistrados['CPF'].isin(cpf_Juizado_especial_Turma_recursal)))&
               (df_magistrados['Data de saída da situação - TRATADA'] == date(2024,12,31))]


NM_12 = len(NM_12_df['CPF'].unique())
NM_12

# %%
teste = NM_12_df.groupby('CPF')['Órgão de lotação do magistrado(a)'].count().reset_index()
teste[teste['Órgão de lotação do magistrado(a)'] > 1]

# %% [markdown]
# ## Número 13

# %%
df_acum_turmas_recursais = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'].str.contains(r'101&104|102&104|103&104')]
cpf_acum_turmas_recursais = df_acum_turmas_recursais['CPF'].unique()

# %%
NM_13_df = df_magistrados[(df_magistrados['Cargo'].isin(['1','2','6','11'])) & 
              (df_magistrados['Situação profissional atual'].isin(['7','8','9','10','19'])) & 
               ((df_magistrados['CPF'].isin(cpf_acum_turmas_recursais)))&
               (df_magistrados['Data de saída da situação - TRATADA'] == date(2024,12,31))]


NM_13 = len(NM_13_df['CPF'].unique())
len(NM_13_df['CPF'].unique())

# %%
teste = NM_13_df.groupby('CPF')['Órgão de lotação do magistrado(a)'].count().reset_index()
teste[teste['Órgão de lotação do magistrado(a)'] > 1]

# %% [markdown]
# ## Número 14

# %%
df_acum_turmas_recursais = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'].str.contains(r'102&104|103&104')]
cpf_acum_turmas_recursais = df_acum_turmas_recursais['CPF'].unique()

# %%
NM_14_df = df_magistrados[(df_magistrados['Cargo'].isin(['1','2','6','11'])) & 
              (df_magistrados['Situação profissional atual'].isin(['7','8','9','10','19'])) & 
               ((df_magistrados['CPF'].isin(cpf_acum_turmas_recursais)))&
               (df_magistrados['Data de saída da situação - TRATADA'] == date(2024,12,31))]


NM_14 = len(NM_14_df['CPF'].unique())
len(NM_14_df['CPF'].unique())

# %%
teste = NM_14_df.groupby('CPF')['Órgão de lotação do magistrado(a)'].count().reset_index()
teste[teste['Órgão de lotação do magistrado(a)'] > 1]

# %% [markdown]
# ## Número 15

# %%
df_acum_turmas_recursais = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'].str.contains(r'104 -|- 104')]
cpf_acum_turmas_recursais = df_acum_turmas_recursais['CPF'].unique()

# %%
NM_15_df = df_magistrados[(df_magistrados['Cargo'].isin(['1','2','6','11'])) & 
                ((df_magistrados['CPF'].isin(cpf_Turma_recursal))) &
              (df_magistrados['Situação profissional atual'].isin(['7','8','9','10','19'])) & 
               (~(df_magistrados['CPF'].isin(cpf_Juizado_especial_adjunto)))&
               (df_magistrados['Data de saída da situação - TRATADA'] == date(2024,12,31))]


NM_15 = len(NM_15_df['CPF'].unique())
NM_15

# %%
teste = NM_15_df.groupby('CPF')['Órgão de lotação do magistrado(a)'].count().reset_index()
teste[teste['Órgão de lotação do magistrado(a)'] > 1]

# %% [markdown]
# ## Número 16

# %%
NM_16_df_aux = df_magistrados[(df_magistrados['Cargo'].isin(['1','2','11']))& 
              (df_magistrados['Situação profissional atual'].isin(['6','7','10','19']))]

cpf_NM_16 = NM_16_df_aux['CPF'].unique()

NM_16_df = df_magistrados[(df_magistrados['CPF'].isin(cpf_NM_16)) &
                          (df_magistrados['Órgão de lotação do magistrado(a)'].isin(['16']))]

# %%
# Converter as colunas para datetime
NM_16_df['Data de início da situação - TRATADA'] = pd.to_datetime(NM_16_df['Data de início da situação - TRATADA'])
NM_16_df['Data de saída da situação - TRATADA'] = pd.to_datetime(NM_16_df['Data de saída da situação - TRATADA'])

NM_16_df = NM_16_df.drop_duplicates()

# Calcular a diferença em dias e garantir valores não negativos
NM_16_df.loc[:, 'Quantidade de dias'] = (
    (NM_16_df['Data de saída da situação - TRATADA'] - NM_16_df['Data de início da situação - TRATADA'])
    .dt.days
    .clip(lower=0)
)

# %%
NM_16 = NM_16_df['Quantidade de dias'].sum()
NM_16

# %% [markdown]
# ## Número 17

# %%
df_turmas_recursais = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'].str.contains(r'104')]
cpf_turmas_recursais = df_turmas_recursais['CPF'].unique()

# %%
NM_17_df_aux = df_magistrados[(df_magistrados['CPF'].isin(cpf_turmas_recursais))& 
              (df_magistrados['Situação profissional atual'].isin(['6','7','10','19']))]

cpf_NM_17 = NM_17_df_aux['CPF'].unique()

NM_17_df = df_magistrados[(df_magistrados['CPF'].isin(cpf_NM_17)) &
                          (df_magistrados['Órgão de lotação do magistrado(a)'].isin(['16']))]

# %%
# Converter as colunas para datetime
NM_17_df['Data de início da situação - TRATADA'] = pd.to_datetime(NM_17_df['Data de início da situação - TRATADA'])
NM_17_df['Data de saída da situação - TRATADA'] = pd.to_datetime(NM_17_df['Data de saída da situação - TRATADA'])

# Calcular a diferença em dias e garantir valores não negativos
NM_17_df.loc[:, 'Quantidade de dias'] = (
    (NM_17_df['Data de saída da situação - TRATADA'] - NM_17_df['Data de início da situação - TRATADA'])
    .dt.days
    .clip(lower=0)
)

NM_17 = NM_17_df['Quantidade de dias'].sum()

# %%
NM_17

# %% [markdown]
# ## Número 18

# %%
df_juizados_esp = df_grouped_magis_serventia[df_grouped_magis_serventia['Classificação da Unidade Judiciária'].str.contains(r'103')]
cpf_juizados_esp = df_juizados_esp['CPF'].unique()

NM_18_df_aux = df_magistrados[(df_magistrados['CPF'].isin(cpf_juizados_esp))& 
              (df_magistrados['Situação profissional atual'].isin(['6','7','10','19']))]

cpf_NM_18 = NM_18_df_aux['CPF'].unique()

NM_18_df = df_magistrados[(df_magistrados['CPF'].isin(cpf_NM_18)) &
                          (df_magistrados['Órgão de lotação do magistrado(a)'].isin(['16']))]

# Converter as colunas para datetime
NM_18_df['Data de início da situação - TRATADA'] = pd.to_datetime(NM_18_df['Data de início da situação - TRATADA'])
NM_18_df['Data de saída da situação - TRATADA'] = pd.to_datetime(NM_18_df['Data de saída da situação - TRATADA'])

# Calcular a diferença em dias e garantir valores não negativos
NM_18_df.loc[:, 'Quantidade de dias'] = (
    (NM_18_df['Data de saída da situação - TRATADA'] - NM_18_df['Data de início da situação - TRATADA'])
    .dt.days
    .clip(lower=0)
)

NM_18 = NM_18_df['Quantidade de dias'].sum()
NM_18

# %% [markdown]
# ## Junção tabela Magistrados

# %%
df_variaveis_magistrados['RESPOSTA NUMÉRICA'] = df_variaveis_magistrados['RESPOSTA NUMÉRICA'].replace("297Inativos","297")
df_variaveis_magistrados['RESPOSTA NUMÉRICA'] = df_variaveis_magistrados['RESPOSTA NUMÉRICA'].astype(int)

# %%
df_variaveis_magistrados['TIPO'] = 'Magistrados'
df_variaveis_magistrados['DESCRIÇÃO DA PERGUNTA'] = df_variaveis_magistrados['DESCRIÇÃO DA PERGUNTA'].astype(str)
df_variaveis_magistrados['MPM'] = [NM_1, NM_2, NM_3, NM_4, NM_5, NM_6, NM_7, NM_8, NM_9, NM_10,NM_11,NM_12,NM_13,NM_14,NM_15,NM_16,NM_17,NM_18]
df_variaveis_magistrados['REFERÊNCIA'] = data_atual
df_variaveis_magistrados['DIFERENÇA EM PERCENTUAL'] = round(((df_variaveis_magistrados['MPM'] - df_variaveis_magistrados['RESPOSTA NUMÉRICA']) / df_variaveis_magistrados['RESPOSTA NUMÉRICA'])*100, 2)

# Substituindo NaN e inf por 0
df_variaveis_magistrados['DIFERENÇA EM PERCENTUAL'].replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# Opcional: Se você sabe que certos valores são anômalos, pode optar por removê-los
df_variaveis_magistrados = df_variaveis_magistrados[df_variaveis_magistrados['DIFERENÇA EM PERCENTUAL'].between(-100, 100)]

df_variaveis_magistrados.to_excel(f"C:\\Users\\lfmelo\\Documents\\Demanda MPM\\Dados\\MPM\\MPM_Magistrados_{data_atual}.xlsx",engine='openpyxl',index=False) # Usar excel devido a quantidade de caracteres na coluna 'DESCRIÇÃO DA PERGUNTA'

# %% [markdown]
# # Auxiliares

# %% [markdown]
# ## Número 1

# %%
df_NA_1 = df_servidores[(df_servidores['Cargo'] == '6') &
                              (df_servidores['Data de saída da situação - TRATADA'] == date(2024,12,31)) &
                              (df_servidores['Situação profissional atual'].isin(['1','2','3','13']))]
NA_1 = len(df_NA_1['CPF'].unique())
NA_1

# %% [markdown]
# ## Número 2

# %%
df_NA_2 = df_servidores[(df_servidores['Cargo'] == '5') &
                              (df_servidores['Data de saída da situação - TRATADA'] == date(2024,12,31)) &
                              (df_servidores['Situação profissional atual'].isin(['1','2','3','13']))]
NA_2 = len(df_NA_2['CPF'].unique())
NA_2

# %% [markdown]
# ## Número 3

# %%
df_NA_3 = df_servidores[(df_servidores['Cargo'] == '8') &
                              (df_servidores['Data de saída da situação - TRATADA'] == date(2024,12,31)) &
                              (df_servidores['Situação profissional atual'].isin(['1','2','3','13']))]
NA_3 = len(df_NA_3['CPF'].unique())
NA_3

# %% [markdown]
# ## Número 4

# %%
df_NA_4 = df_servidores[(df_servidores['Cargo'] == '9') &
                              (df_servidores['Data de saída da situação - TRATADA'] == date(2024,12,31)) &
                              (df_servidores['Situação profissional atual'].isin(['1','2','3','13']))]
NA_4 = len(df_NA_4['CPF'].unique())
NA_4

# %% [markdown]
# ## Número 5

# %%
df_NA_5 = df_servidores[(df_servidores['Cargo'] == '11') &
                              (df_servidores['Data de saída da situação - TRATADA'] == date(2024,12,31)) &
                              (df_servidores['Situação profissional atual'].isin(['1','2','3','13']))]
NA_5 = len(df_NA_5['CPF'].unique())
NA_5

# %% [markdown]
# ## Número 6

# %%
# Tá errado pois aqui foi utilizado a planilha de servidores mas nas instruções diz para usar a planilha de Dado da Diretoria de Gestão de Pessoas
df_NA_6 = df_servidores[(df_servidores['Cargo'].isin(['5','6','7','8','9','10','11','12','13'])) &
                              (df_servidores['Data de saída da situação - TRATADA'] == date(2024,12,31))]
NA_6 = len(df_NA_6['CPF'].unique())
NA_6

# %% [markdown]
# ## Junção das tabelas Auxiliares

# %%
df_variaveis_auxiliares['RESPOSTA NUMÉRICA'] = df_variaveis_auxiliares['RESPOSTA NUMÉRICA'].astype(int)

# %%
df_variaveis_auxiliares['TIPO'] = 'Auxiliares'
df_variaveis_auxiliares['MPM'] = [NA_1,NA_2,NA_3,NA_4,NA_5,NA_6]
df_variaveis_auxiliares['REFERÊNCIA'] = data_atual
df_variaveis_auxiliares['DIFERENÇA EM PERCENTUAL'] = round(((df_variaveis_auxiliares['MPM'] - df_variaveis_auxiliares['RESPOSTA NUMÉRICA']) / df_variaveis_auxiliares['RESPOSTA NUMÉRICA'])*100,2)

# Substituindo NaN e inf por 0
df_variaveis_auxiliares['DIFERENÇA EM PERCENTUAL'].replace([np.inf, -np.inf, np.nan], 0, inplace=True)

# Opcional: Se você sabe que certos valores são anômalos, pode optar por removê-los
df_variaveis_auxiliares = df_variaveis_auxiliares[df_variaveis_auxiliares['DIFERENÇA EM PERCENTUAL'].between(-100, 100)]
df_variaveis_auxiliares['DIFERENÇA EM PERCENTUAL'] = round(df_variaveis_auxiliares['DIFERENÇA EM PERCENTUAL'],2)


df_variaveis_auxiliares.to_excel(f"C:\\Users\\lfmelo\\Documents\\Demanda MPM\\Dados\\MPM\\MPM_Auxiliares_{data_atual}.xlsx",engine='openpyxl',index=False) # Usar excel devido a quantidade de caracteres na coluna 'DESCRIÇÃO DA PERGUNTA'


