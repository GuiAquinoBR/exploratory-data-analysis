# Para o dataframe
import pandas as pd

# Para remover letras do dataframe
import numpy as np

# Para os gráficos
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import folium

# Extraindo os dados
dados = pd.read_csv('/content/suicide_total_deaths.csv')
pd.set_option('display.max_columns', None) # Para visualizar todas as linhas do Dataframe
dados.head()

dadosT = dados.transpose().reset_index() # Realizando a transposta dos dados e redefinindo os índices
dadosT.columns = dadosT.iloc[0] # Redefinido os nomes das colunas
dadosT.drop(0, inplace=True) # Excluindo a linha de índice 0
dadosT = dadosT.reset_index() # Redefinindo os índices
dadosT.drop(columns='index', inplace=True) # Excluindo a coluna index
novos_dados = dadosT.rename({'country':'year'}, axis=1) # Renomeando a coluna

display(novos_dados.isna().sum()) # Se possui valores NaN
print('\n')
display(novos_dados.isnull().sum()) # Se possui valores Nulos
print('\n')
display(novos_dados.dtypes) # Tipo dos dados em cada coluna
print('\n')
display(novos_dados.shape) # Tamando do dataset

# Função para remover o k
def removerK(coluna):
  if 'k' in coluna:
      if len(coluna) > 1:
          return float(coluna.replace('k', '')) * 1000
  elif 'K' in coluna:
      if len(coluna) > 1:
          return float(coluna.replace('K', '')) * 1000
  else:
    return coluna
  
# Removendo k
for i in novos_dados.columns:
  novos_dados[i] = novos_dados[i].apply(removerK)

# Alterando o tipo das colunas
for i in novos_dados.columns:
  if i != 'year':
    novos_dados[i] = novos_dados[i].astype('float64')

# Qual a quantidades de suicídios por ano?
df = novos_dados.iloc[:,1::]
listaAno = list(novos_dados.year)

totalAno = {}
somaAno = []

# Destacando os valores das linhas
for i in range(len(listaAno)):
  somaAno.append(df.iloc[i].values.sum())

# Adicionando as listas em um dicionário
for i in range(len(listaAno)):
  totalAno[listaAno[i]] = somaAno[i]

dicionario = {}
dicionario['Ano'] = list(totalAno.keys())
dicionario['Qntd'] = list(totalAno.values())
df = pd.DataFrame(dicionario, columns=['Ano','Qntd'])

# Gráfico de linha
plt.style.use('fivethirtyeight')
plt.figure(figsize=(17,7))
plt.grid(linestyle=':')
sns.lineplot(x=df.Ano, y=df.Qntd, alpha=1)
plt.autoscale(enable=True)
plt.title('Quantidade de Suicídio por Ano', fontsize=14, weight='bold')
plt.ylabel('Número de Mortes')
plt.xticks(rotation=45)
plt.show()
#---------------------------------------------------------------------------

# Quais os índices de suicídio dos países mais populosos do mundo? (China, Índia, EUA, Indonésia e Paquistão)
fig, ax = plt.subplots(figsize=(17,7))
plt.style.use('bmh')
plt.grid(linestyle=':')

ax.plot(novos_dados.year, novos_dados.China, label='China', alpha=1, color='r')
ax.plot(novos_dados.year, novos_dados.India, label='India', alpha=1, color='tab:orange')
ax.plot(novos_dados.year, novos_dados['United States'], label='EUA', alpha=1, color='b')
ax.plot(novos_dados.year, novos_dados.Indonesia, label='Indonésia', alpha=1, color='tab:olive')
ax.plot(novos_dados.year, novos_dados.Pakistan, label='Paquistão', alpha=1, color='g')

ax.set_title('Índice de suicídios nos 5 países mais populosos do mundo', fontsize=14, weight='bold')
ax.set_xlabel('Ano')
ax.set_ylabel('Número de mortes')
ax.legend()

plt.xticks(rotation=45)
plt.show()
#---------------------------------------------------------------------------

# Qual é o continente com o maior volume de suicídios? E o continente com o menor volume?
# Separando os países por continentes
america_central = novos_dados[['Bermuda','Belize','Costa Rica','El Salvador','Guatemala','Honduras','Nicaragua','Panama','Antigua and Barbuda','Bahamas','Barbados','Cuba','Dominica','Dominican Republic','Grenada','Haiti','Jamaica','St. Lucia','St. Kitts and Nevis','St. Vincent and the Grenadines','Trinidad and Tobago','Puerto Rico','Virgin Islands (U.S.)']]
america_sul = novos_dados[['Argentina','Bolivia','Brazil','Chile','Colombia','Ecuador','Guyana','Paraguay','Peru','Suriname','Uruguay', 'Venezuela']]
america_norte = novos_dados[['Canada','United States','Mexico']]
africa = novos_dados[["Cote d'Ivoire",'South Africa','Angola','Algeria','Benin','Botswana','Burkina Faso','Burundi','Cameroon','Chad','Djibouti','Egypt','Eritrea','Ethiopia','Gabon','Gambia','Ghana','Guinea','Guinea-Bissau','Equatorial Guinea','Madagascar','Cape Verde','Comoros','Sao Tome and Principe','Seychelles','Lesotho','Liberia','Libya','Malawi','Mali','Morocco','Mauritania','Mozambique','Namibia','Niger','Nigeria','Kenya','Central African Republic','Congo, Dem. Rep.','Congo, Rep.','Mauritius','Rwanda','Senegal','Sierra Leone','Somalia','Eswatini','Sudan','South Sudan','Tanzania','Togo','Tunisia','Uganda','Zambia','Zimbabwe']]
asia = novos_dados[['Lao','Kyrgyz Republic','Afghanistan','Saudi Arabia','Armenia','Azerbaijan','Bahrain','Bangladesh','Brunei','Bhutan','Cambodia','Qatar','China','Singapore','North Korea','South Korea','United Arab Emirates','Philippines','Georgia','Yemen','India','Indonesia','Iran','Iraq','Israel','Japan','Jordan','Kuwait','Lebanon','Malaysia','Maldives','Myanmar','Mongolia','Nepal','Oman','Pakistan','Russia','Syria','Sri Lanka','Tajikistan','Thailand','Turkmenistan','Turkey','Uzbekistan','Vietnam','Palestine','Timor-Leste','Taiwan']]
europa = novos_dados[['Albania','Germany','Andorra','Austria','Belgium','Belarus','Bosnia and Herzegovina','Bulgaria','Kazakhstan','Cyprus','Croatia','Denmark','Slovak Republic','Slovenia','Spain','Estonia','Finland','France','Greece','Hungary','Ireland','Iceland','Italy','Latvia','Lithuania','Luxembourg','Malta','Moldova','Monaco','Montenegro','Norway','Netherlands','Poland','Portugal','Czech Republic','North Macedonia','United Kingdom','Romania','San Marino','Serbia','Sweden','Switzerland','Ukraine']]
oceania = novos_dados[['Guam','Cook Is','American Samoa','Australia','Micronesia, Fed. Sts.','Fiji','Marshall Islands','Solomon Islands','Kiribati','Nauru','New Zealand','Palau','Papua New Guinea','Samoa','Tonga','Tuvalu', 'Vanuatu','Northern Mariana Islands','Tokelau']]
groenlandia = novos_dados[['Greenland']]

# Somando as mortes dos países do continente por ano
ano = list(novos_dados.year.values)
ameCen = []
ameNor = []
ameSul = []
asialist = []
euro = []
afri = []
ocean = []
groen = []

for i in range(0,len(america_central)):
   ameCen.append(america_central.iloc[i].sum())
   ameNor.append(america_norte.iloc[i].sum())
   ameSul.append(america_sul.iloc[i].sum())
   asialist.append(asia.iloc[i].sum())
   euro.append(europa.iloc[i].sum())
   afri.append(africa.iloc[i].sum())
   ocean.append(oceania.iloc[i].sum())
   groen.append(groenlandia.iloc[i].sum())

continentes = pd.DataFrame({'Ano':ano, 'America Central':ameCen,'America Norte':ameNor,
                            'America Sul':ameSul,'Asia':asialist, 'Europa':euro,
                            'Africa':afri,'Oceania':ocean, 'Groenlândia':groen})

ameCenTot = continentes[['America Central']].sum()
ameNorTot = continentes[['America Norte']].sum()
ameSulTot = continentes[['America Sul']].sum()
asiaTot = continentes[['Asia']].sum()
euroTot = continentes[['Europa']].sum()
afriTot = continentes[['Africa']].sum()
oceanTot = continentes[['Oceania']].sum()
groelTot = continentes[['Groenlândia']].sum()

# Criando o gráfico de mapa
mapa = folium.Map(location=[0.0, 0.0],
                  zoom_start=2,
                  tiles='OpenStreetMap')

folium.Circle(
    radius=700000,
    location=[-17.32083702890929, -57.247544896160214],
    popup="<i>América do Sul com 780.544 Mil</i>",
    color="green",
    fill=True,
    tooltip='Clique para ver os detalhes').add_to(mapa)

folium.Circle(
    radius=300000,
    location=[12.198741434268346, -85.37254473952882],
    popup="<i>América Central com 184.694 Mil</i>",
    color="yellow",
    fill=True,
    tooltip='Clique para ver os detalhes').add_to(mapa)

folium.Circle(
    radius=800000,
    location=[48, -102],
    popup="<i>América do Norte com 1.460.830 Milhão</i>",
    color="blue",
    fill=True,
    tooltip='Clique para ver os detalhes').add_to(mapa)

folium.Circle(
    radius=50000,
    location=[66.03881366440447, -44.87904384484402],
    popup="<i>Groenlândia com 1363 Mil</i>",
    color="pink",
    fill=True,
    tooltip='Clique para ver os detalhes').add_to(mapa)

folium.Circle(
    radius=1200000,
    location=[52.78661560749805, 23.824737016960196],
    popup="<i>Europa com 3.054.549 Milhões</i>",
    color="purple",
    fill=True,
    tooltip='Clique para ver os detalhes').add_to(mapa)

folium.Circle(
    radius=3200000,
    location=[47.13826131791401, 99.60211457413058],
    popup="<i>Asia com 16.223.494 Milhões</i>",
    color="red",
    fill=True,
    tooltip='Clique para ver os detalhes').add_to(mapa)

folium.Circle(
    radius=1300000,
    location=[-1.4328019860802115, 22.066924516960196],
    popup="<i>Africa com 1.893.772 Milhão</i>",
    color="brown",
    fill=True,
    tooltip='Clique para ver os detalhes').add_to(mapa)

folium.Circle(
    radius=200000,
    location=[-7.040168749692714, 130.17239285971866],
    popup="<i>Oceania com 111.041 Mil</i>",
    color="orange",
    fill=True,
    tooltip='Clique para ver os detalhes').add_to(mapa)

mapa
