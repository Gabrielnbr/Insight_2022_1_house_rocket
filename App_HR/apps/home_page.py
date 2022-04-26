# 1. Home Page
# Explicação do Projeto
    # 1. Introdução e Premissas
    # 2. Data set + Filtros Zipcode, Preço (Min Max), Sazonalidade, Quais colunas quer ver.

# ===================
# 0.1 Imports
# ===================

import streamlit as st
# Como faz a classe multiapp??? o vídeo não mostra, buscar outas alternativas.


import pandas         as pd
import numpy          as np
import seaborn        as sns
import streamlit      as st
import folium
import geopandas

from matplotlib import pyplot as plt
from matplotlib import gridspec

from apps import transformacao_dados

# 0.1 CONFIG LAYOUT
st.set_page_config( layout='wide' )
np.set_printoptions(suppress=True)
pd.set_option('display.float_format', '{:.4f}'.format)

# Functions
@st.cache( allow_output_mutation=True)
def getdata(path):
    return pd.read_csv(path)

@st.cache(allow_output_mutation=True)
def get_geofile(url):
    return geopandas.read_file(url)

@st.cache(allow_output_mutation=True)
def features (data_set):

    data_set.rename(columns = {'id': 'id', 'date': 'data_venda', 'price':'preco', 'bedrooms':'quartos', 'bathrooms':'banheiros',
                            'sqft_living': 'm2_construido_total','sqft_lot':'m2_terreno_total', 'floors':'andares', 'waterfront':'vista_agua',
                            'view':'vista_geral', 'condition':'condicao', 'grade':'nivel_construcao','sqft_above':'m2_construidos_chao',
                            'sqft_basement':'m2_porao', 'yr_built':'ano_construido', 'yr_renovated':'ano_reformado', 'zipcode':'cep',
                            'lat':'latitude', 'long':'longitude'}, inplace=True)

    data_set['data_venda'] = pd.to_datetime(data_set['data_venda'], format="%Y-%m-%d")

    data_set.drop(columns=['sqft_living15','sqft_lot15'], inplace=True)
    data_set.drop_duplicates(['id'],inplace=True)

    data_set.loc[data_set['quartos'] == 33, 'quartos'] = 3

    # Mudando de pés2 para m2
    data_set['m2_construido_total'] = data_set['m2_construido_total'].apply(lambda x: x*0.09290304)
    data_set['m2_terreno_total'] = data_set['m2_terreno_total'].apply(lambda x: x*0.09290304)
    data_set['m2_construidos_chao'] = data_set['m2_construidos_chao'].apply(lambda x: x*0.09290304)
    data_set['m2_porao'] = data_set['m2_porao'].apply(lambda x: x*0.09290304)

    return data_set

def show(data):
    st.subheader("Testando aqui")
    st.dataframe(data)

def app():
    
    path = "../A_House_Rocket/data_set/kc_house_data.csv"
    # url = "https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson"
    
    data_set = getdata(path)
    
    data_set = features(data_set)
    
    #data = transformacao_dados.pull_data()
    #url = "https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson"
    
    show(data_set)