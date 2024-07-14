import pandas as pd
from functions.ipeadata_api import get_ipeadata
import streamlit as st


@st.cache_data
def get_desctritiva():
    "Busca dados do api do IPEAdata e retorna um DataFrame"
    df_ipea = get_ipeadata()
    return df_ipea


def tabela_descritiva(df):
    
    df2 = df[['PRECO']].describe().T

    return (df2['count'][0].round(2), 
            df2['mean'][0].round(2),
            df2['std'][0].round(2),
            df2['min'][0].round(2),
            df2['25%'][0].round(2),
            df2['50%'][0].round(2),
            df2['75%'][0].round(2),
            df2['max'][0].round(2))
    

