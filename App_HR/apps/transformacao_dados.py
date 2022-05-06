import pandas         as pd
import streamlit      as st
import geopandas

import datetime as dt
import os

@st.cache( allow_output_mutation=True)
def get_data(path):
    return pd.read_csv(path)

@st.cache( allow_output_mutation=True)
def get_path():
    path = 'data_set/kc_house_data.csv'
    return path

@st.cache( allow_output_mutation=True)
def get_path_to_export():
    path = 'data_set/house_data_transformado.csv'
    return path

@st.cache( allow_output_mutation=True)
def get_geo_path():
    url = "https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson"
    geo_data = geopandas.read_file(url)
    return geo_data

def transformacao (data_set):
    
    data_set['date'] = pd.to_datetime(data_set['date']).dt.date

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

def features(data_set):
    # Filtro Ano de Construção <> 1955
    # Se construção >= 1955 == 0 senão < 1955
    data_set['construcao_1955'] = data_set['ano_construido'].apply(lambda construcao : 0 if construcao >= 1955 else 1)

    # Filtro por Porão
    # Se Sem Porão == 0 se não 1
    data_set['sem_porao'] = data_set['m2_porao'].apply(lambda x : 0 if x == 0 else 1)

    # Filtro de Temporariedade
    #Filtro Ano
    data_set['ano_venda'] = pd.to_datetime(data_set['data_venda']).dt.year
    # Filtro Mês
    data_set['mes'] = pd.to_datetime(data_set['data_venda']).dt.month
    # Filtro Sazonalidade
    # Primavera -> Março 03 a Maio 05
    # Verão -> Junho 06 a Agosto 08
    # Outono -> Setembro 09 a Novembro 11
    # Inverno -> Dezembro 12 a Fevereiro 02
    data_set['estacoes'] = data_set['mes'].apply(lambda mes: 'primavera' if (mes >= 3) & (mes <= 5) else
                                            'verao' if (mes >= 6) & (mes <= 8) else
                                            'outono' if (mes >= 9) & (mes <= 11) else
                                            'inverno')

    # Filtro de Condição do Imóvel
    # boa condição == 1
    # má condição == 0
    data_set['boa_condicao'] = data_set['condicao'].apply(lambda condicao: 1 if condicao >= 4 else 0)

    # Filtro Nível de Construção
    # bom nível de construcao == 1
    # má nível de construcao == 0
    data_set['bom_nivel_construcao'] = data_set['nivel_construcao'].apply(lambda nivel: 1 if nivel >= 10 else 0)
    return data_set

def exportar (data_set):
    path_to_export = get_path_to_export()
    data_set.to_csv(path_to_export, index=False)

def teste_exportar ():
    path_exportado = get_path_to_export()
    
    if os.path.exists(path_exportado) == False:
        data_set_exportado = 0
        return data_set_exportado, 0
    
    else:
        data_set_exportado = 1
        return data_set_exportado, path_exportado
    

def pull_data():
    
    exportado, path_exportado = teste_exportar()
    
    if exportado == 1:
        return get_data(path_exportado)
    
    else:
        data_set = transformacao(get_data(get_path()))
        data_set = features(data_set)
        exportar(data_set)
        return data_set