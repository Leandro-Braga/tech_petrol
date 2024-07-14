
import warnings

import pandas as pd
import streamlit as st
from PIL import Image

from paginas.pg_navegacao import init_session_state

warnings.filterwarnings('ignore')

## --- Formatação de valores --- ##
pd.options.display.float_format = "{:.2f}".format


# -- imagens e logos -- #
img = './image/petrolv1.png'
img = Image.open(img)

# --- Configurações da página 'Geral' --- #

st.set_page_config(
    page_title='Petróleo - Modelos Preditivo',
    page_icon=img,
    layout='wide',
    initial_sidebar_state='expanded',
    # initial_sidebar_state='collapsed',
    menu_items={
        'Get Help': 'https://www.google.com.br/',
        'Report a bug': "https://www.google.com.br/",
        'About': "Esse app foi desenvolvido pela Grupo 38 FIAP."
    }
)

## --- Início da sessão do Streamlit --- ##
init_session_state()


