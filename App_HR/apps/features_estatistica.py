import streamlit      as st
import pandas         as pd

from matplotlib import pyplot as plt
from apps import transformacao_dados

def mostra_histograma(data_set):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    st.header('Histograma')
        
    var_num = data_set.select_dtypes(include=['int64','float64','int32','float32'])
    plt.subplot()
    var_num.hist(figsize=(16,9), bins= 40)
    plt.tight_layout()
    
    st.pyplot()
    
    
    return None

def features(data_set):
    
    st.header('Tabela Features')
    
    text = """
    As features foram desenvolvidas a partir da necessidade de responder as perguntas de negócio e as hipóteses.
    """
    st.markdown(text)
    
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

def estatistica(data_set):
    
    st.header('Tabela Estatística')
    
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
    st.title("Features e Estatística")
    
    data_set = transformacao_dados.pull_data()
    
    features(data_set)
    estatistica(data_set)
    mostra_histograma(data_set)