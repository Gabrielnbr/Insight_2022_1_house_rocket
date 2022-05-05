# 2. Transformações, features e estatística
# Somente textos e tabelas estáticas com as explicações
# Na pate da estatística podemos colcoar filtro de linha e coluna.

import streamlit      as st
import numpy          as np
import pandas            as pd

from matplotlib import pyplot as plt
from apps import transformacao_dados

def mostra_tabela(data_set):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    st.header('Gráficos contagem')
    st.write('Explicar o pq desse gráfico?')
        
    var_num = data_set.select_dtypes(include=['int64','float64','int32','float32'])
    plt.subplot()
    var_num.hist(figsize=(16,9), bins= 40)
    plt.tight_layout()
    
    st.pyplot()
    
    
    return None

def explica_features(data_set):
    
    st.header('Tabela Features')
    st.write('Explicação da criação dessa feature e o pq?')
    
    texto = """
    | Nome_Feature | Descrição |
    | ----------- | --------- |
    | construcao_1955 | Indica se a construcão foi feita antes ou depois de 1955. Para construções a baixo de 1955 o valor é 1, se não o valor é 0.|
    | sem_porao | Indica se o imóvel tem porão ou não. Para imóveis com porão o valor é 1 e sem porão o valor é 0. |
    | ano_venda | Indica exclusivamente o ano de venda do imóvel. |
    | mes | Indica, de forma númeral, cada mês de venda do imóvel |
    | estações | Indica as 4 estções do ano, de forma nominal, sendo: primavera entre o mês 3 e 5, verão entre o mês 6 e 8, outono entre o mês 9 e 11, por fim, inverno no mês 12, 1 e 2 |
    | boa_condição | Indica a boa condição do imóvel através da coluna condição. Foi definido que um local em boas condições deve ter 4 pontos ou mais na coluna condição, se tiver 3 pontos ou menos, não está em boa condição |
    | bom_nivel_construcao | Indica o bom nível de construcão do imóvel através da coluna nivel_construcao. Foi definido que um bom nível de construcão deve ter 10 pontos ou mais na coluna nivel_construcao, se tiver 9 pontos ou menos, não está em um bom nível de construcão |
    """
    
    st.markdown(texto)
    
    return None

def explica_estatística(data_set):
    
    st.header('Tabela Estatística')
    st.write('Explicar para que serve e o pq de está aqui.')
    
    skewness = data_set.skew()
    kurtosis = data_set.kurtosis()
    
    #todo DROPAR COLUNA ID
    tabela_estatistica = pd.DataFrame (data_set.describe().T)
    tabela_estatistica = pd.concat([tabela_estatistica,skewness,kurtosis], axis=1)
    tabela_estatistica.columns = ['Count','Media','Std','Min','25%','Median','75%','Max','Skew','Kurtosis']
    
    tabela_estatistica.drop(['id'], axis=0, inplace=True)
    tabela_estatistica.drop(['Count'], axis=1, inplace=True)
    
    st.dataframe(tabela_estatistica)
    
    return None

def app():
    st.subheader("Features e Estatística")
    
    data_set = transformacao_dados.pull_data()
    
    explica_features(data_set)
    explica_estatística(data_set)
    mostra_tabela(data_set)





# Testado, mas sem chegar a lugar algum
"""def mostra_tabela(data_set):
    
    var_num = data_set.select_dtypes(include=['int64','float64','int32','float32'])
    
    # fig, ax = plt.subplot()
    # fig = plt.hist(var_numericas_2)
    
    #fig = var_num.hist(figsize=(16,9), bins=40)
    #plt.tight_layout()
    #st.plotly_chart()
    
    #st.pyplot(fig)
    
    #plt.figure(figsize=(16,12))
    
    for i in (np.arange(25)+1):
        plt.subplot(5,5,i)
        plt.hist(var_num, x=var_num[i], bins=40)
        plt.plot()
    plt.tight_layout()

    # O mais perto que eu consegui
    fig, ax =plt.subplots(5,5)
    ax = var_num.hist(bins= 40)
    plt.tight_layout()
    st.pyplot(fig)
    
    return None"""