import streamlit      as st
import pandas         as pd
import plotly.express as px
import folium

from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster

from apps import transformacao_dados

def transformacao_negocio_a (data_set):
    
    qn1 = data_set[['id','preco','boa_condicao','cep','estacoes']].copy()
    
    # Calculando a mediana do preço de compra
    qn1_median = qn1[[ 'preco','cep']].groupby('cep').median().reset_index()
    qn1_median.rename(columns = { 'preco':'mediana_preco' }, inplace=True)
    
    qn1 = pd.merge( qn1, qn1_median, on='cep', how='inner')
    
    # Pode comprar = 1
    # Não pode comprar = 0
    qn1['comprar'] = 0
    qn1.loc[ (qn1['boa_condicao'] == 1) & (qn1['preco'] < qn1['mediana_preco']), 'comprar' ] = 1
    
    return qn1

def questao_negocio_a (data_set):
    
    aptos_compra = data_set.loc[data_set['comprar'] == 1].copy()
    
    aptos_compra['economia'] = 0
    aptos_compra['economia'] = aptos_compra.apply(lambda x : x['mediana_preco'] - x['preco'], axis=1)
    
    return aptos_compra

def filtros_dash_qna (data_set,qna):
    data_dash = pd.merge( data_set, qna[['id','comprar','economia','mediana_preco']], on='id')
    
    # Os filtros possuem 2 linhas
    # Linha 1 dos filtros
    c1, c3, c5, c7 = st.columns((4))
    
    with c1:
        area_cons_min = int(data_dash['m2_construido_total'].min() - 1 )
        area_cons_max = int(data_dash['m2_construido_total'].max() + 1 )
        
        f_area_construida = st.slider('Área Construída', min_value= area_cons_min,
                                    max_value= area_cons_max, value= (area_cons_min, area_cons_max))
    
    with c3:
        area_tot_min = int(data_dash['m2_terreno_total'].min() - 1 )
        area_tot_max = int(data_dash['m2_terreno_total'].max() + 1 )    
        
        f_area_total = st.slider('Área Total', min_value= area_tot_min,
                                max_value= area_tot_max, value= (area_tot_min, area_tot_max))
    
    with c5:
        preco_imovel_min = int(data_dash['preco'].min() - 1 )
        preco_imovel_max = int(data_dash['preco'].max() + 1 )
        
        f_preco_imovel = st.slider('Valor do Imóvel', min_value= preco_imovel_min,
                                max_value= preco_imovel_max, value= (preco_imovel_min, preco_imovel_max))
    
    with c7:
        f_vista_agua = st.multiselect('Vista água', sorted(set(data_dash['vista_agua'].unique())))
        if f_vista_agua != []:
            data_dash = data_dash.loc[data_dash['vista_agua'].isin(f_vista_agua)]
        else:
            data_dash = data_dash.copy()
    
    # Linha 2 dos filtros
    col1, col3, col5, col7 = st.columns((4))   
    
    with col1:
        f_andares = st.multiselect('Andares', sorted( set( data_dash['andares'].unique())))
        if f_andares != []:
            data_dash = data_dash.loc[data_dash['andares'].isin(f_andares)]
        else:
            data_dash = data_dash.copy()
    
    with col3:
        f_quartos = st.multiselect('Quartos', sorted( set( data_dash['quartos'].unique())))
        if f_quartos != []:
            data_dash = data_dash.loc[data_dash['quartos'].isin(f_quartos)]
        else:
            data_dash = data_dash.copy()
    
    with col5:
        f_banheiros = st.multiselect('Banheiros', sorted( set( data_dash['banheiros'].unique())))
        if f_banheiros != []:
            data_dash = data_dash.loc[data_dash['banheiros'].isin(f_banheiros)]
        else:
            data_dash = data_dash.copy()
    
    with col7:
        f_cep = st.multiselect('Cep', sorted(set(data_dash['cep'].unique())))
        if f_cep != []:
            data_dash = data_dash.loc[data_dash['cep'].isin(f_cep)]
        else:
            data_dash = data_dash.copy()
    
    data_dash = data_dash[((data_dash['m2_construido_total'] > f_area_construida[0]) & (data_dash['m2_construido_total'] < f_area_construida[1])) &
                          ((data_dash['m2_terreno_total'] > f_area_total[0]) & (data_dash['m2_terreno_total'] < f_area_total[1])) &
                          ((data_dash['preco'] > f_preco_imovel[0]) & (data_dash['preco'] < f_preco_imovel[1]))]
    return data_dash

def dashboard_qna(data_set):
    data_dash = data_set.copy()
    
    fig = px.scatter_mapbox(data_dash,
                            lat='latitude',
                            lon='longitude',
                            color='preco',
                            color_continuous_scale=px.colors.cyclical.IceFire, 
                            size_max=15, 
                            zoom=10)
    
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(height=450, margin={"r":0,"t":0,"l":0,"b":0})
    
    c1, c2 = st.columns((5,2))
    
    with c1:
        st.plotly_chart(fig, use_container_width= True)
    
    with c2:
        st.write(f'O total de imóveis aptos a comprar são: {data_dash.shape[0]:,.2f}')
        
        valor_compra = data_dash['preco'].sum()
        st.write(f'O valor total do aporte para adiquirir os imóveis é: {valor_compra:,.2f}')
        
        valor_economizado = data_dash['economia'].sum()
        st.write(f'O valor total de economia ao adiquirir todos os imóveis é: {valor_economizado:,.2f}')
        
    
    return None

def transformação_negocio_b(data_set):
    qn2 = data_set[['id','preco','cep','estacoes']].copy()
    
    qn2_median = qn2[['preco','cep','estacoes']].groupby(['cep','estacoes']).median().reset_index()
    qn2_median.rename(columns = { 'preco':'mediana_preco' }, inplace=True)
    
    qn2 = pd.merge( qn2, qn2_median, on=['cep','estacoes'], how='inner')
    
    qn2['preco_venda'] = qn2[['mediana_preco','preco']].apply(lambda x: (x['preco']*1.1) if x['preco'] >= x['mediana_preco']
                                                                        else (x['preco']*1.3), axis=1)
    
    qn2['lucro_venda'] = qn2['preco_venda'] - qn2['preco']
    return qn2

def questao_negocio_b(data_set, qn1):
    
    aptos_venda = data_set.copy()
    aptos_venda = pd.merge(aptos_venda,qn1[['id','mediana_preco','economia','preco']], on='id',how='right')
    aptos_venda.rename(columns={'mediana_preco_x':'mediana_preco_venda','mediana_preco_y':'mediana_preco_compra',
                                'preco_y':'preco_compra'},inplace=True)
    
    lucro_venda = aptos_venda['lucro_venda'].sum()
    lucro_sazonalidade = aptos_venda[['lucro_venda','estacoes']].groupby('estacoes').sum().reset_index()
    return aptos_venda

def filtros_dash_qnb (data_set, qnb):
    data_dash = pd.merge( data_set, qnb[['id','preco_venda','lucro_venda','preco_compra']], on='id')
    
    # Os filtros possuem somente 1 linha
    c1, c3, c5, c7 = st.columns((4))
    
    with c1:
        preco_compra_min = int(data_dash['preco_compra'].min() - 1 )
        preco_compra_max = int(data_dash['preco_compra'].max() + 1 )
        
        f_preco_compra = st.slider('Preço de Compra do Imóvel', min_value= preco_compra_min,
                                    max_value= preco_compra_max, value= (preco_compra_min, preco_compra_max))
    
    with c3:
        preco_venda_min = int(data_dash['preco_venda'].min() - 1 )
        preco_venda_max = int(data_dash['preco_venda'].max() + 1 )
        
        f_preco_venda = st.slider('Valor de venda do Imóvel', min_value= preco_venda_min,
                                max_value= preco_venda_max, value= (preco_venda_min, preco_venda_max))
    
    with c5:
        lucro_venda_min = int(data_dash['lucro_venda'].min() - 1 )
        lucro_venda_max = int(data_dash['lucro_venda'].max() + 1 )    
        
        f_lucro_venda = st.slider('Lucro da Venda do Imóvel', min_value= lucro_venda_min,
                                max_value= lucro_venda_max, value= (lucro_venda_min, lucro_venda_max))
    
    with c7:
        f_estacoes = st.multiselect('Estações', sorted( set( data_dash['estacoes'].unique())))
        if f_estacoes != []:
            data_dash = data_dash.loc[data_dash['estacoes'].isin(f_estacoes)]
        else:
            data_dash = data_dash.copy()
    
    data_dash = data_dash[((data_dash['preco_compra'] > f_preco_compra[0]) & (data_dash['preco_compra'] < f_preco_compra[1])) &
                          ((data_dash['preco_venda'] > f_preco_venda[0]) & (data_dash['preco_venda'] < f_preco_venda[1])) &
                          ((data_dash['lucro_venda'] > f_lucro_venda[0]) & (data_dash['lucro_venda'] < f_lucro_venda[1]))]
    return data_dash

def dashboard_qnb(data_set):
    
    data_dash = data_set.copy()
    
    # Base Map - Folium 
    density_map = folium.Map( location=[data_dash['latitude'].mean(), data_dash['longitude'].mean() ],
                              default_zoom_start=15 ) 

    marker_cluster = MarkerCluster().add_to( density_map )
    for name, row in data_dash.iterrows():
        folium.Marker( [row['latitude'], row['longitude'] ], 
            popup='Comprado por R${0}. Vendido por R${1}. Lucro {2} '.format( row['preco_compra'], 
                           row['preco_venda'], 
                           row['lucro_venda']) ).add_to( marker_cluster )
    
    c1, c2 = st.columns((5,3))
    
    with c1:
        folium_static( density_map )
    
    with c2:
        st.write(f'O total de imóveis aptos a venda são: {data_dash.shape[0]:,.2f}')
        lucro_venda = data_dash['lucro_venda'].sum()
        st.write(f'A lucratividade total estimada é de: {lucro_venda:,.2f}')
        lucro_sazonalidade = data_dash[['lucro_venda','estacoes']].groupby('estacoes').sum().reset_index()
        st.write(f'A lucratividade por sazonalidade estimada é de:')
        st.dataframe(lucro_sazonalidade)
    
    return None

def app():
    st.title("Questões de Negócio")
    data_set = transformacao_dados.pull_data()
    #   geofile = transformacao_dados.get_geo_path()
    
    st.markdown('### Questão de negócio 1: Quais são os melhores imóveis e por quanto comprar?')
    qn1 = transformacao_negocio_a(data_set)
    qn1 = questao_negocio_a(qn1)
    dash_qn1 = filtros_dash_qna(data_set, qn1) # filtros
    st.header('Dashboard')
    dashboard_qna(dash_qn1) # Dashboard
    
    st.markdown('### Questão de negócio 2: Qual o melhor período de venda dos imóveis e por quanto vender?')
    qn2 = transformação_negocio_b(data_set)
    qn2 = questao_negocio_b(qn2, qn1)
    dash_qn2 = filtros_dash_qnb(data_set, qn2)
    st.header('Dashboard')
    dashboard_qnb(dash_qn2)