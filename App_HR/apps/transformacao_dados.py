import pandas         as pd
import numpy          as np
import seaborn        as sns
import streamlit      as st
import folium
import geopandas

from matplotlib import pyplot as plt
from matplotlib import gridspec

@st.cache( allow_output_mutation=True)
def getdata(path):
    return pd.read_csv(path)

def transformacao (data_set):
    
    data_set['date'] = pd.to_datetime(data_set['date'])

    data_set.drop(columns=['sqft_living15','sqft_lot15'], inplace=True)
    data_set.drop_duplicates(['id'],inplace=True)

    data_set.loc[data_set['bedrooms'] == 33, 'bedrooms'] = 3

    # Mudando de pés2 para m2
    data_set['sqft_living'] = data_set['sqft_living'].apply(lambda x: x*0.09290304)
    data_set['sqft_lot'] = data_set['sqft_lot'].apply(lambda x: x*0.09290304)
    data_set['sqft_above'] = data_set['sqft_above'].apply(lambda x: x*0.09290304)
    data_set['sqft_basement'] = data_set['sqft_basement'].apply(lambda x: x*0.09290304)

    data_set.rename(columns = {'id': 'id', 'date': 'data_venda', 'price':'preco', 'bedrooms':'quartos', 'bathrooms':'banheiros',
                            'sqft_living': 'm2_construido_total','sqft_lot':'m2_terreno_total', 'floors':'andares', 'waterfront':'vista_agua',
                            'view':'vista_geral', 'condition':'condicao', 'grade':'nivel_construcao','sqft_above':'m2_construidos_chao',
                            'sqft_basement':'m2_porao', 'yr_built':'ano_construido', 'yr_renovated':'ano_reformado', 'zipcode':'cep',
                            'lat':'latitude', 'long':'longitude'}, inplace=True)

    return data_set

def pull_data():
    
    path = "../A_House_Rocket/data_set/kc_house_data.csv"
    # url = "https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson"
    
    data_set = getdata(path)
    
    data_set = transformacao(data_set)
    
    return 0