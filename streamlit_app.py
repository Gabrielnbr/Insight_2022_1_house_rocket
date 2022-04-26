# ==================
# 0. IMPORTS
# ==================
from email.policy import default
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

import folium
import geopandas

from statistics import median
from xml.etree.ElementInclude import include
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from datetime import datetime

# 0.1 CONFIG LAYOUT
st.set_page_config( layout='wide' )

# Functions
@st.cache( allow_output_mutation=True)
def getdata(path):
    return pd.read_csv(path)

@st.cache(allow_output_mutation=True)
def get_geofile(url):
    return geopandas.read_file(url)

def set_feature(data):
    data['price_m2'] = data['price'] / data['sqft_lot']
    return data 

def overview_data(data):
    # ===================
    # 3. Data Overview
    # ===================
    st.title( 'Data Overview' )

    f_attributes = st.sidebar.multiselect('Enter columns', data.columns)
    f_zipcode = st.sidebar.multiselect('Enter zipcode', data['zipcode'].unique())

    st.write (f_zipcode)
    st.write (f_attributes)

    if ((f_zipcode != []) & (f_attributes != [])):
        data = data.loc[data['zipcode'].isin( f_zipcode ), f_attributes]

    elif ((f_zipcode != []) & (f_attributes == [])):
        data = data.loc[data['zipcode'].isin( f_zipcode ), :]

    elif ((f_zipcode == []) & (f_attributes != [])):
        data = data.loc[:, f_attributes]

    else:
        data = data.copy()

    st.dataframe(data)

    # Diagrama da página
    c1, c2 = st.columns((1,1))

    # 3.1. Averege Metrics
    df1 = data[['id', 'zipcode']].groupby('zipcode').count().reset_index()
    df2 = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df3 = data[['sqft_living', 'zipcode']].groupby('zipcode').mean().reset_index()
    df4 = data[['price_m2','zipcode']].groupby('zipcode').mean().reset_index()

    # 3.1.1 Merge DF
    m1 = pd.merge(df1, df2, on='zipcode', how='inner')
    m2 = pd.merge(m1, df3, on='zipcode', how='inner')
    df = pd.merge(m2, df4, on='zipcode', how='inner')

    df.columns = ['ZIPCODE', 'TOTAL HOUSES', 'PRICES', 'SQRT LIVING', 'PRICE/M2']

    c1.header('Averege Values')
    c1.dataframe(df, height = 600)

    # =============================
    # 4. Statistics Descriptive
    # =============================
    
    # Essa versão do Streamlit está dando problema para reconhecer e transformar o float64
    # Então estou pedindo para só selecionar o int64
    # Depois tentar transformar float64 em int64
    num_atributes = data.select_dtypes(include= ['int64'])
    media = pd.DataFrame(num_atributes.apply( np.mean ))
    mediana = pd.DataFrame(num_atributes.apply( np.median ))
    std = pd.DataFrame(num_atributes.apply( np.std ))

    max_ = pd.DataFrame(num_atributes.apply( np.max ))
    min_ = pd.DataFrame(num_atributes.apply( np.min ))

    df1 = pd.concat([max_, min_, media, mediana, std], axis=1).reset_index()
    df1.columns = ['Atributes', 'Max', 'Min', 'mean', 'median', 'std']

    c2.header('Statistics Descriptive')
    c2.dataframe(df1, height = 600)

    return None

def portofolio_density(data, geofile):
    # =============================
    # 5. Desnsidade de Pertifólio
    # =============================

    st.title( "Region Overview" )
    c1, c2 = st.columns((1,1))

    c1.header( "Portifólio Density" )

    df = data.sample(20)

    # 5.1. Base Mapa Folium
    density_mapa = folium.Map( location = [data['lat'].mean(), data['long'].mean()], default_zoom_star = 15)

    marker_cluster = MarkerCluster().add_to(density_mapa)
    for name, row in df.iterrows():
        folium.Marker ( [row['lat'], row['long']],
                        popup = 'Sold R$ {0} on: {1}. Features: {2} sqft, {3} bedrooms, {4} bathrooms, year built: {5}'.format( row['price'],
                                        row['date'],
                                        row['sqft_living'],
                                        row['bedrooms'],
                                        row['bathrooms'],
                                        row['yr_built'] ) ).add_to( marker_cluster )

    with c1:
        folium_static( density_mapa )

    # 5.2. Region Price
    c2.header("Price Density")

    df = data[['price', 'zipcode']].groupby('zipcode').mean().reset_index()
    df.columns = ['ZIP','PRICE']

    geofile = geofile[geofile['ZIP'].isin(df['ZIP'].to_list() )]

    region_price_map = folium.Map( location = [data['lat'].mean(), data['long'].mean()], default_zoom_star = 15)

    region_price_map.choropleth( data = df,
                                geo_data = geofile,
                                columns=['ZIP', 'PRICE'],
                                key_on='feature.properties.ZIP',
                                fill_color='YlOrRd',
                                fill_opacity = 0.7,
                                line_opacity = 0.2,
                                legend_name='AVG PRICE' )

    with c2:
        folium_static( region_price_map )
    
    return None

def comercial (data):
        # ========================================================
    # 6. Distribuição dos Imóveis por categoria comercial
    # ========================================================

    st.sidebar.title( "Comercial Options" )
    st.title( "Comecial Atributes" )

    # Formatação da Data
    data['date'] = pd.to_datetime( data['date'] ).dt.strftime( '%Y-%m-%d')

    # 6.1. Filters
    min_yr_build = int( data['yr_built'].min() )
    max_yr_build = int( data['yr_built'].max() )

    st.sidebar.subheader( 'Select Max Year Build' )
    filter_yr_built = st.sidebar.slider('Year Built',
                                                    min_yr_build,
                                                    max_yr_build,
                                                    min_yr_build)

    st.header("Averega Price per Year")
    st.sidebar.subheader('Select Max Year Built')
    st.write(filter_yr_built)

    # 6.2. Averega Price per Year

    df = data.loc[data['yr_built'] < filter_yr_built]
    df = df[['yr_built', 'price']].groupby('yr_built').mean().reset_index()

    fig = px.line(df, x='yr_built', y='price')

    st.plotly_chart( fig, use_container_width=True )


    # 6.3. Averega Price per Day
    st.header("Averega Price per Day")
    st.sidebar.subheader('Select Max Data')

    #filters
    min_date = datetime.strptime( data['date'].min(), "%Y-%m-%d") 
    max_date = datetime.strptime( data['date'].max(), "%Y-%m-%d")

    f_date = st.sidebar.slider( 'Date', min_date, max_date, min_date)

    #data filtering
    data['date'] = pd.to_datetime( data['date'] )
    df = data.loc[data['date'] < f_date]
    df = df[['date', 'price']].groupby('date').mean().reset_index()

    #plot
    fig = px.line(df, x='date', y='price')
    st.plotly_chart( fig, use_container_width=True )

    # ===================
    # Histograma
    # ===================

    st.header('Histograma')
    st.sidebar.subheader('Select Max Price')

    min_price = int( data['price'].min() )
    max_price = int( data['price'].max() )
    avg_price = int( data['price'].mean() )

    f_price = st.sidebar.slider( 'Price', min_price, max_price, avg_price)

    df = data.loc[data['price'] < f_price]

    fig = px.histogram(df, x='price', nbins = 50 )
    st.plotly_chart(fig, use_container_width=True )

    return None

def comercial_distribution(data):
    # ======================================================
    # Distribuição dos Imóveis por categorias Físicas
    # ======================================================

    st.sidebar.title( 'Atribute Optitons' )
    st.title( 'House Atributes' )

    # Filters

    f_bedrooms = st.sidebar.selectbox( "Max Bedrooms",
                                        sorted( set( data['bedrooms'].unique() ) ) )

    f_bathrooms = st.sidebar.selectbox( "Max Bathrooms",
                                        sorted( set( data['bathrooms'].unique() ) ) )

    c1, c2 = st.columns((1,1))

    # House bedrooms
    c1.header( 'Houses Bedrooms')
    df = data[data['bedrooms'] < f_bedrooms]
    fig = px.histogram( df, x='bedrooms', nbins=10 )
    c1.plotly_chart( fig, use_container_width=True )

    # House bethrooms
    c1.header( 'Houses Bathrooms')
    df = data[data['bathrooms'] < f_bathrooms]
    fig = px.histogram( df, x='bathrooms', nbins=10 )
    st.plotly_chart( fig, use_container_width=True )

    #Filter
    f_floors = st.sidebar.selectbox( "Max number of Floors",
                                    sorted( set( data['floors'].unique() ) ) )

    f_water_view = st.sidebar.checkbox( "Is Water View")

    c1, c2 = st.columns((1,1))

    # House floors
    c1.header("Floors")
    df = data[data['floors'] < f_floors]
    fig = px.histogram( df, x='floors', nbins=10 )
    c1.plotly_chart( fig, use_container_width=True )

    # House water view
    c2.header("Water view")
    if f_water_view:
        df = data[data['waterfront'] == 1]
    else:
        df =data.copy()

    fig = px.histogram( df, x='floors', nbins=10 )
    c2.plotly_chart( fig, use_container_width=True )

    return None

if __name__ == '__main__':
    # ETL
    # Data Extraction
    
    # 1.1 Get Data
    path = "../@2110.1 - Curso_Phyton_Zero_ao_DS - Youtube (CDS)/Data_set/kc_house_data.csv"
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'
    
    data = getdata(path)
    geofile = get_geofile(url)
    
    # Transformation
    data = set_feature( data )
    
    overview_data( data )
    
    portofolio_density( data, geofile )
    
    comercial( data )
    
    comercial_distribution( data )
    
    # Loading