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

import datetime as dt
from apps import transformacao_dados

# 0.1 CONFIG LAYOUT
st.set_page_config( layout='wide' )
np.set_printoptions(suppress=True)
pd.set_option('display.float_format', '{:.4f}'.format)

# Functions
@st.cache( allow_output_mutation=True)
def getdata(path):
    return pd.read_csv(path)

@st.cache( allow_output_mutation=True)
def get_geofile(url):
    return geopandas.read_file(url)

def show(data):
    st.subheader("Testando aqui")
    st.dataframe(data)

def atributos():
    
    text = """
    | Nome_Coluna | Tradução | Descrição |
    | ----------- | -------- | --------- |
    | id | id | ID exclusivo para cada casa vendida |
    | date | data_venda | Data da venda da casa |
    | price | preco | Preço de cada casa vendida |
    | bedrooms | quartos | Número de quartos |
    | bedrooms | banheiros | Número de banheiros, onde 0,5 representa um quarto com vaso sanitário, mas sem chuveiro |
    | sqft_living | m2_construido_total | Metragem quadrada do espaço interior dos apartamentos |
    | sqft_lot | m2_terreno_total | Metragem quadrada do espaço terrestre |
    | floors | andares | Número de andares |
    | waterfront | vista_agua | Variável fictícia para saber se o apartamento estava com vista para a orla ou não |
    | view | vista_geral | Índice de 0 a 4 de quão boa era a vista do imóvel. 0 é a pior vista e 4 é a melhor vista |
    | condition | condicao | Índice de 1 a 5 sobre a condição do apartamento. 1 é a pior condição e 5 é a melhor |
    | grade | nivel_construcao | Índice de 1 a 13, onde 1-3 fica aquém da construção e design de edifícios, 7 tem um nível médio de construção e design e 11-13 tem um alto nível de construção e design. |
    | sqft_above | m2_construidos_chao | Metragem quadrada do espaço interno da habitação que está acima do nível do solo |
    | sqft_basement | m2_porao | Metragem quadrada do espaço interno da habitação que está abaixo do nível do solo |
    | yr_built | ano_construído | Ano em que a casa foi construída |
    | yr_renovated | ano_reformado | Ano da última reforma da casa |
    | zipcode | cep | Em que área de código postal a casa está |
    | lat | latitude | latitude |
    | long | longitude | longitude |
    | sqft_living15 | nao_traduzido | Metragem quadrada do espaço habitacional interior para os 15 vizinhos mais próximos |
    | sqft_lot15 | nao_traduzido | A metragem quadrada dos lotes dos 15 vizinhos mais próximos |
    """
    
    st.markdown(text)
    
    #img = Image.open('img\Atributos.png')
    #st.image(img)
    
    return None

def app():
    data = transformacao_dados.pull_data()
    
    show(data)
    atributos()