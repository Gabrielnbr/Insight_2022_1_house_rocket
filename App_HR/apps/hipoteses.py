# 3. Hipóteses
# Serão textos/gráficos sem necessidade de filtros.

import streamlit      as st
import plotly.express as px
import pandas         as pd
import numpy          as np
from apps import transformacao_dados

def h1(data_set):
    st.markdown('### H1. Imóveis que possuem vista para água são, pelo menos, 30% mais caros, na média.')
    
    h1 = data_set[['preco','vista_agua']].groupby('vista_agua').mean().reset_index()

    h1['percent'] = h1['preco'].pct_change()
    st.write(f'H1 é falsa, pois os imóveis com vista para a água, em média, são {h1.iloc[1,2]:.2%} mais caros.')
    
    fig = px.bar(h1, x='vista_agua', y='preco', color = 'preco')
    st.plotly_chart(fig, use_container_width=True)
    
    return None

def h2(data_set):
    st.markdown('### H2: Imóveis com data de construção menor do que 1955, são 50% mais baratos na média.')
    
    h2 = data_set[['preco','construcao_1955']].groupby('construcao_1955').mean().reset_index().sort_values(by='construcao_1955',ascending=False)
    
    h2['percent'] = h2['preco'].pct_change()
    st.write(f'H2 é falsa, pois os imóveis anteriores a 1955, são em média {h2.iloc[1,2]:.2%} mais caros.')
    
    fig = px.bar(h2, x='construcao_1955', y='preco', color = 'preco')
    st.plotly_chart(fig, use_container_width=True)
    
    return None

def h3(data_set):
    st.markdown('### H3: Imóveis sem porão possuem m2_construcao_total 50% maiores do que com porão, na média.')
    
    h3 = data_set[['m2_terreno_total','sem_porao']].groupby('sem_porao').mean().reset_index()

    h3['percent'] = h3['m2_terreno_total'].pct_change()
    st.write(f'H3 é falsa, pois os imóveis sem porão são, em média, {h3.iloc[1,2]:.2%} maiores do que imóveis com porão.')

    fig = px.bar( h3, x='sem_porao', y='m2_terreno_total', color='m2_terreno_total')
    st.plotly_chart(fig, use_container_width=True)
    
    return None

def h4(data_set):
    st.markdown('### H4: O Crescimento do preço dos imóveis YoY (Year over Year) é de 10%, em média.')
    h4 = data_set[['preco','ano_venda']].groupby('ano_venda').mean().reset_index()
    
    h4['percent'] = h4['ano_venda'].pct_change()
    st.write(f'H4 é falsa, pois o crescimento dos preços dos imóveis YoY, em média, é de {h4.iloc[1,2]:.2%}')
    
    fig = px.bar( h4, x = 'ano_venda', y = 'preco', color='preco')
    st.plotly_chart(fig, use_container_width=True)
    
    return None

def h5(data_set):
    
    st.markdown('### H5: Imóveis com 3 banheiros tem um crescimento médio no Preço MoM (Month of Month) de 15%.')
    h5 = data_set[['preco','mes']].loc[data_set['banheiros']==3].groupby('mes').mean().reset_index()
    
    h5['porcentagem'] = round(h5['preco'].pct_change(),2)
    
    media_h5 = h5['porcentagem'].mean()
    st.write(f'H5 é falsa, os imóveis não possuem um crescimento MoM de 15%, pois ele prossui uma variação média no período de {media_h5:.2%}')
    
    fig1 = px.bar( h5, x='mes', y='preco',
                   color='preco', title= 'Variação medio do Preço por mês')
    fig2 = px.bar( h5, x='mes', y='porcentagem',
                   color='porcentagem', title= 'Porcentagem de crescimento medio em relação ao mês anterior')
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    
    return None

def h6(data_set):
    st.markdown('### H6: Imóveis no inverno são, em média, são 20% mais baratos do que o resto do ano.')
    h6 = data_set[['preco', 'estacoes']].copy()
    
    h6.loc[h6['estacoes'] == 'inverno', 'sep_inverno'] = 1
    h6.loc[h6['estacoes'] != 'inverno', 'sep_inverno'] = 0
    
    h6_1 = h6[['preco', 'estacoes']].groupby('estacoes').mean().reset_index()
    h6_2 = h6[['preco', 'sep_inverno']].groupby('sep_inverno').mean().reset_index()
    
    h6_2['percent'] = h6_2['preco'].pct_change()
    st.write(f'H6 é falsa, pois em média o valor dos imóveis no inverno é {h6_2.iloc[1,2]:.2%} em comparação ao resto do ano.')
    
    fig1 = px.bar(h6_1, x='estacoes', y='preco', color='preco')
    fig2 = px.bar(h6_2, x='sep_inverno', y='preco', color='preco')
    
    c1, c2 = st.columns((1,1))
    with c1:
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        st.plotly_chart(fig2, use_container_width=True)
    
    return None

def h7(data_set):
    st.markdown('### H7: Pelo menos 80% dos imóveis com condição 4 e 5 tem níveis de construção 7 ou mais.')
    # Condição 4 e 5 = boa_condicao = 1
    h7 = data_set[['boa_condicao','nivel_construcao']].loc[data_set['boa_condicao'] == 1].groupby('nivel_construcao').sum().reset_index()
    
    h7_boa_condicao = h7['boa_condicao'].loc[h7['nivel_construcao'] >= 7].sum()
    h7_todas_condicoes = h7['boa_condicao'].sum()
    h7_paretto = h7_boa_condicao/h7_todas_condicoes
    
    st.write(f'H7 é verdadeira, pois os imóveis com boa condição representão {h7_paretto:.2%}.')
    st.write(f'Sendo o total de imóveis em boa condção: {h7_todas_condicoes} e os imóveis com nível de construção 7 ou mais: {h7_boa_condicao}.')
    
    fig = px.bar( h7, x='nivel_construcao', y='boa_condicao', color='boa_condicao')
    st.plotly_chart(fig, use_container_width=True)
    
    return None

def h8(data_set):
    st.markdown('### H8: Pelo menos 80% dos imóveis com vista para água possuem nível de construção 10 ou mais.')
    h8 = data_set[['vista_agua','nivel_construcao']].loc[data_set['vista_agua'] == 1].groupby('nivel_construcao').sum().reset_index()
    
    h8_vista_agua = h8['vista_agua'].loc[h8['nivel_construcao'] >= 10].sum()
    h8_todas_condicoes = h8['vista_agua'].sum()
    h8_paretto = h8_vista_agua/h8_todas_condicoes
    
    st.write(f'H8 é falsa, pois os imóveis com boa condição representão {h8_paretto:.2%}.')
    st.write(f'Sendo o total de imóveis em boa condção: {h8_todas_condicoes} e os imóveis com nível de construção 10 ou mais: {h8_vista_agua}.')
    
    fig = px.bar( h8, x='nivel_construcao', y='vista_agua', color='vista_agua')
    st.plotly_chart(fig, use_container_width=True)
    
    return None

def layout_pagina(data_set):
    
    c1, c2 = st.columns((1,1))
    with c1:
        h1(data_set)
    with c2:
        h2(data_set)
    
    c3, c4 = st.columns((1,1))
    with c3: 
        h3(data_set)
    with c4:
        h4(data_set)
    
    h5(data_set)
    
    h6(data_set)
    
    c7, c8 = st.columns((1,1))
    with c7:
        h7(data_set)
    with c8:
        h8(data_set)
    
    return

def app ():
    
    # Supressão da notação científica. Não consegui fazer essa supressão
    
    data_set = transformacao_dados.pull_data()
    st.subheader("Hipóteses")
    
    layout_pagina(data_set)