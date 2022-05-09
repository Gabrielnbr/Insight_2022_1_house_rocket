# ===================
# 0.1 Imports
# ===================

import streamlit      as st
from apps import transformacao_dados

def intro ():
    
    text = """
    
    A empresa House Rocket tem como negócio principal a compra, reforma e venda de imóveis nos EUA. Com isto, este projeto foi desenvolvido para auxiliar o time de negócio a encontrar o melhor momento de compra e venda dos imóveis.

    Com este projeto eles poderão definir os valores de aporte para comprar as casas, quantas devem ser compradas, quais casas comprar e em qual localização, por quanto vender e qual será o lucro presumido.

    1.1. Questões de negócio

    Pnsando na tomada de decisão do time de negócios, podemos consideramos 2 condições:

    1. O time de negócio precisa ter uma ação rápida ao analizar quais casas comprar.
    2. Uma vez comprada essas casas qual seria o melhor momento para vendê-las.

    Desta forma temos as duas __questões de negócio__:

    1. Quais são os melhores imóveis e por quanto comprar?
    2. Qual o melhor período de venda dos imóveis e por quanto vender?
    """
    
    st.markdown(text)

def show(data):
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
    
    return None

def app():
    data = transformacao_dados.pull_data()
    
    st.title("Página Inicial")
    
    intro()
    
    st.header("Base de dados original")
    dt = transformacao_dados.get_data(transformacao_dados.get_path())
    show(dt)
    
    st.header("Atributos")
    atributos()