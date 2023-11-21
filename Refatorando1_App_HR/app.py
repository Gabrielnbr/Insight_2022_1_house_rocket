# ============
# 0 Imports
# ============
from typing_extensions import dataclass_transform
import streamlit as st
from multiapp import MultiApp
from apps import home_page, features_estatistica, hipoteses, questoes_negocio, transformacao_dados

st.set_page_config( layout='wide' )

app = MultiApp()

# Inicialização do app

def ap ():
    # data_tranformado = tranformação aqui, feito 1 vez.
    data_tranformado = transformacao_dados.pull_data()
    
    app.add_app("1. Pagina Inicial", home_page.app, data_tranformado)
    app.add_app("2. Features e Estatistica", features_estatistica.app, data_tranformado)
    app.add_app("3. Hipoteses", hipoteses.app, data_tranformado)
    app.add_app("4. Questões de Negócio", questoes_negocio.app, data_tranformado)

if __name__ == '__main__':
# Talvez a transformação seja aqui antes de chemar o app.run() ou o ap()
    ap()
# Main app
    app.run()