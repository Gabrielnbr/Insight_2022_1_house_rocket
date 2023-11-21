# ============
# 0 Imports
# ============
import streamlit as st
from multiapp import MultiApp
from apps import home_page, features_estatistica, hipoteses, questoes_negocio

st.set_page_config( layout='wide' )

app = MultiApp()

# Inicialização do app
app.add_app("1. Pagina Inicial", home_page.app)
app.add_app("2. Features e Estatistica", features_estatistica.app)
app.add_app("3. Hipoteses", hipoteses.app)
app.add_app("4. Questões de Negócio", questoes_negocio.app)

# Main app
app.run()