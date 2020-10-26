"""################### Importando os Pacotes ######################"""
import pandas as pd
import numpy as np
import requests
import json
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime as dt
import math
from scipy.optimize import curve_fit
sns.set_style()



"""###################  Fonte dos dados ################### """

url = "https://api.covid19api.com/total/country/brazil"
#<Response [200]> : Everything went okay, and the result has been returned (if any).
payload = {}
headers= {} #provide information such as authentication keys.
response = requests.request("GET", url, headers=headers, data = payload)
print(response.json())

#Criando Dataset
df = pd.json_normalize(response.json())
df.head()

"""################### Feature Engineering ###################"""

# converter a coluna Datetime em tipo datetime;
df.Date = pd.to_datetime(df.Date, format="%Y-%m-%d").dt.tz_localize(None)

# Criando features para cada período
df['year'] = df.Date.dt.year
df['month'] = df.Date.dt.month.map({1:'Janeiro', 1:'Fevereiro', 3:'Março', 4:'Abril', 5:'Maio', 6:'Junho', 7:'Julho', 8:'Agosto',9:'Setembro', 10:'Outubro', 11:'Novembro', 12:'Dezembro'})
df['day'] = df.Date.dt.day
df['day_of_week'] = df.Date.dt.dayofweek.map({0:'Segunda', 1:'Terça', 2:'Quarta', 3:'Quinta', 4:'Sexta', 5:'Sábado', 6:'Domingo'})

#Criando variáveis para os eventos diários  ao invés de acumulados
df['Mortes_por_Dia'] = df.Deaths.diff().fillna(0)
df['Casos_Confirmados_por_Dia'] = df.Confirmed.diff().fillna(0).astype('int64')
df['Recuperados_por_Dia'] = df.Recovered.diff().fillna(0).astype('int64')
df['Active'] = df.Recovered.diff().fillna(0).astype('int64')
df['Dias'] = (df.index + 1 ).astype('float64')

df.head()

"""################### Visualizações segundo dias da semana ###################"""

ordem = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']

df_weekday = df.copy().groupby(df['day_of_week']).sum().reindex(ordem)
df_weekday

""" Casos Confirmados """

fig, ax = plt.subplots(figsize=(12,6))

df_weekday['Confirmed'].loc[ordem].plot(legend=True).yaxis.get_major_formatter().set_scientific(False)
ax.set_xlabel("Dia da Semana")
ax.legend(['Número de casos Confirmados'])
plt.title("Casos Confirmados por dia da semana");

""" Mortes """

fig, ax = plt.subplots(figsize=(12,6))

df_weekday['Deaths'].loc[ordem].plot(legend=True).yaxis.get_major_formatter().set_scientific(False)
ax.set_xlabel("Dia da Semana")
ax.legend(['Número de óbitos'])
plt.title("Número de óbitos por dia da semana");

""" Recuperados """

fig, ax = plt.subplots(figsize=(12,6))

df_weekday['Recovered'].loc[ordem].plot(legend=True).yaxis.get_major_formatter().set_scientific(False)
ax.set_xlabel("Dia da Semana")
ax.legend(['Número de recuperados'])
plt.title("Número de recuperados por dia da semana");

""" Casos Ativos """

fig, ax = plt.subplots(figsize=(12,6))

df_weekday['Active'].loc[ordem].plot(legend=True).yaxis.get_major_formatter().set_scientific(False)
ax.set_xlabel("Dia da Semana")
ax.legend(['Número de casos ativos'])
plt.title("Número de casos ativos por dia da semana");

"""################### Visualizações segundo meses ###################"""

ordem = ['Fevereiro','Março','Abril','Maio','Junho','Julho','Agosto','Setembro','Outubro']

df_month = df.copy().groupby(df['month']).sum().reindex(ordem)

df_month

"""## Casos Confirmados"""

fig, ax = plt.subplots(figsize=(12,6))

df_month['Confirmed'].loc[ordem].plot(legend=True).yaxis.get_major_formatter().set_scientific(False)
ax.set_xlabel("Mês")
ax.legend(['Número de casos Confirmados'])
plt.title("Casos Confirmados por mês");

"""## Mortes"""

fig, ax = plt.subplots(figsize=(12,6))

df_month['Deaths'].loc[ordem].plot(legend=True).yaxis.get_major_formatter().set_scientific(False)
ax.set_xlabel("Mês")
ax.legend(['Número de óbitos'])
plt.title("Número de óbitos por mês");

"""## Recuperados"""

fig, ax = plt.subplots(figsize=(12,6))

df_month['Recovered'].loc[ordem].plot(legend=True).yaxis.get_major_formatter().set_scientific(False)
ax.set_xlabel("Mês")
ax.legend(['Número de recuperados'])
plt.title("Número de recuperados por mês");

"""## Casos Ativos"""

fig, ax = plt.subplots(figsize=(12,6))

df_month['Active'].loc[ordem].plot(legend=True).yaxis.get_major_formatter().set_scientific(False)
ax.set_xlabel("Mês")
ax.legend(['Número de casos ativos'])
plt.title("Número de casos ativos por mês");

"""################### Ajustando Modelo epidemiológico ###################"""

def mlTanh(x, a1, a2, a3, b1, b2, b3, c1, c2, c3, d):
  x1=b1*x + c1
  x2=b2*x + c2
  x3=b3*x + c3
  return a1*np.tanh(x1) + a2*np.tanh(x2)  + a3*np.tanh(x3)  - d**2

y  = np.array(df["Mortes_por_Dia"], dtype="float")
x1 = np.array(df['Dias'], dtype="float")
xi = np.linspace(0, len(y), 100)

cof_u, cov  = curve_fit(mlTanh, x1, y)

yi = list(map(lambda x: mlTanh(x, *cof_u), xi))

plt.plot(x1, y, 'rD')
plt.plot(xi, yi, '--b')
plt.plot(xi, mlTanh(xi, cof_u[0], cof_u[1], cof_u[2], cof_u[3], cof_u[4], cof_u[5], cof_u[6], cof_u[7], cof_u[8], cof_u[9]), 'b-')

"""## Extrapolação/ previsão"""

print("Tive que fazer alteração para testar")

print("Tive que fazer alteração para testar 2")
