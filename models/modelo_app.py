import os
import warnings

import joblib
import pandas as pd
import streamlit as st

from functions.calculation import (calcula_derivada,
                                   calcular_e_exibir_diferenca,
                                   data_inicio_fim_dataframe, datas_faltantes,
                                   hyperparametros_prophet, media_movel,
                                   renomeia_colunas, split_treino_teste,
                                   subtracao_MV_STL, teste_dickey_fuller,
                                   transformacao_locaritmica, wmape)
from grafo.grafico_gerais import (plot_forecast, plot_forecast_predict,
                                  plot_forecast_prophet)
from models.modelos import auto_arima_model, naive_model, prophet_model

warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)



def modelo_naive(df_oleo):
    
    start_date = pd.to_datetime('2020-01-01')
    end_date = pd.to_datetime('2024-07-01')
    dias_treino = 1100
    dias_teste = 44

    df = data_inicio_fim_dataframe(df_oleo, start_date, end_date)
    df = df[['PRECO']]


    qtd_dias_ibovespa = len(df)

    if dias_treino + dias_teste > qtd_dias_ibovespa:
        print(f"A quantidade de dias de treino e teste não pode ser maior que {qtd_dias_ibovespa}.")
    
    df_close_last = datas_faltantes(df)

    retorno_teste_df = teste_dickey_fuller(df_close_last)   

    if retorno_teste_df['p-value'] > 0.05:
        print('A série NÃO é estacionária.')
    else:
        print('A série é estacionária.')

    ts_log = transformacao_locaritmica(df_close_last)
    
    # Média Móvel
    moving_avg = media_movel(df_close_last, 12)

    ts_log_moving_avg_diff = subtracao_MV_STL(ts_log, moving_avg)
    
    retorno_teste_df = teste_dickey_fuller(ts_log_moving_avg_diff)    

    if retorno_teste_df['p-value'] > 0.05:
        print('A série NÃO é estacionária.')
    else:
        print('A série é estacionária.')
        df_diff = ts_log_moving_avg_diff.copy()

        
    if retorno_teste_df['p-value'] > 0.05:
        
        df_diff = calcula_derivada(ts_log_moving_avg_diff)
                        
        retorno_teste_df = teste_dickey_fuller(df_diff)
        
    
    df_modelo = renomeia_colunas(df_diff)

    treino, teste, h =  split_treino_teste(df_modelo, dias_treino, dias_teste)

    model1, forecast_df1 = naive_model(treino, teste, h)

    wmape1 = wmape(forecast_df1['y'].values, forecast_df1['Naive'].values)

    plot_forecast('Naive', treino, forecast_df1)

    if wmape1 <= 0.30:

        var_wmape = f"{wmape1:.2%}"
        texto_status_modelo = 'O modelo prever muito bem.'

        return var_wmape, texto_status_modelo
    else:

        var_wmape = f"{wmape1:.2%}"
        texto_status_modelo = 'O modelo não prever muito bem.'

        return var_wmape, texto_status_modelo


def modelo_auto_arima(df_oleo):

    start_date = pd.to_datetime('2020-01-01')
    end_date = pd.to_datetime('2024-07-01')
    dias_treino = 1100
    dias_teste = 44

    df = data_inicio_fim_dataframe(df_oleo, start_date, end_date)
    df = df[['PRECO']]

    qtd_dias_ibovespa = len(df)

    if dias_treino + dias_teste > qtd_dias_ibovespa:
        print(f"A quantidade de dias de treino e teste não pode ser maior que {qtd_dias_ibovespa}.")
    
    df_close_last = datas_faltantes(df)
    
    retorno_teste_df = teste_dickey_fuller(df_close_last)   

    if retorno_teste_df['p-value'] > 0.05:
        print('A série NÃO é estacionária.')
    else:
        print('A série é estacionária.')

    ts_log = transformacao_locaritmica(df_close_last)
    
    # Média Móvel
    moving_avg = media_movel(df_close_last, 12)

    ts_log_moving_avg_diff = subtracao_MV_STL(ts_log, moving_avg)
    
    retorno_teste_df = teste_dickey_fuller(ts_log_moving_avg_diff)    

    if retorno_teste_df['p-value'] > 0.05:
        print('A série NÃO é estacionária.')
    else:
        print('A série é estacionária.')
        df_diff = ts_log_moving_avg_diff.copy()

        
    if retorno_teste_df['p-value'] > 0.05:
        
        df_diff = calcula_derivada(ts_log_moving_avg_diff)
                        
        retorno_teste_df = teste_dickey_fuller(df_diff)
        
    
    df_modelo = renomeia_colunas(df_diff)

    treino, teste, h =  split_treino_teste(df_modelo, dias_treino, dias_teste)

    h = 10  # Horizonte de previsão

    # Rodar o modelo AutoARIMA e gerar previsões
    model2, forecast_df2 = auto_arima_model(treino, teste, h)

    # Calcular WMAPE
    wmape2 = wmape(forecast_df2['y'].values, forecast_df2['AutoARIMA'].values)

    # Plotar o gráfico das previsões
    plot_forecast('AutoARIMA', treino, forecast_df2)

    if wmape2 <= 0.30:

        var_wmape = f"{wmape2:.2%}"
        texto_status_modelo = 'O modelo prever muito bem.'

        return var_wmape, texto_status_modelo
    else:

        var_wmape = f"{wmape2:.2%}"
        texto_status_modelo = 'O modelo não prever muito bem.'

        return var_wmape, texto_status_modelo


def modelo_prophet(df_oleo):

    start_date = pd.to_datetime('2020-01-01')
    end_date = pd.to_datetime('2024-07-01')
    dias_treino = 1100
    dias_teste = 44

    df = data_inicio_fim_dataframe(df_oleo, start_date, end_date)
    df = df[['PRECO']]

    qtd_dias_ibovespa = len(df)

    if dias_treino + dias_teste > qtd_dias_ibovespa:
        print(f"A quantidade de dias de treino e teste não pode ser maior que {qtd_dias_ibovespa}.")
    
    df_close_last = datas_faltantes(df)
    
    retorno_teste_df = teste_dickey_fuller(df_close_last)   

    # Exemplo de uso com o modelo Prophet
    df_modelo_prophet = renomeia_colunas(df_close_last)
    treino_prophet, teste_prophet, h = split_treino_teste(df_modelo_prophet, dias_treino, dias_teste)


    best_params, best_mae = hyperparametros_prophet(treino_prophet)

    model3, forecast3, forecast_df3 = prophet_model(
        treino_prophet, 
        teste_prophet, 
        h, 
        best_params['changepoint_prior_scale'], 
        best_params['seasonality_prior_scale']
    )

    wmape3 = wmape(forecast_df3['y'].values, forecast_df3['yhat'].values)

    plot_forecast_prophet('Prophet', treino_prophet, forecast_df3, forecast_col='yhat')


    if wmape3 <= 0.30:

        var_wmape = f"{wmape3:.2%}"
        texto_status_modelo = 'O modelo prever muito bem.'

        return var_wmape, texto_status_modelo
    
    else:

        var_wmape = f"{wmape3:.2%}"
        texto_status_modelo = 'O modelo não prever muito bem.'

        return var_wmape, texto_status_modelo


def modelo_prophet_previsao(df_oleo, end_date):
    
    start_date = pd.to_datetime('2020-01-01')

    dias_treino = 1100
    dias_teste = 44

    df = data_inicio_fim_dataframe(df_oleo, start_date, end_date)
    df = df[['PRECO']]

    qtd_dias_ibovespa = len(df)

    if dias_treino + dias_teste > qtd_dias_ibovespa:
        print(f"A quantidade de dias de treino e teste não pode ser maior que {qtd_dias_ibovespa}.")
    
    df_close_last = datas_faltantes(df)
    
    retorno_teste_df = teste_dickey_fuller(df_close_last)   

    if retorno_teste_df['p-value'] > 0.05:
        print('A série NÃO é estacionária.')
    else:
        print('A série é estacionária.')

    ts_log = transformacao_locaritmica(df_close_last)
    
    # Média Móvel
    moving_avg = media_movel(df_close_last, 12)

    ts_log_moving_avg_diff = subtracao_MV_STL(ts_log, moving_avg)
    
    retorno_teste_df = teste_dickey_fuller(ts_log_moving_avg_diff)    

    if retorno_teste_df['p-value'] > 0.05:
        print('A série NÃO é estacionária.')
    else:
        print('A série é estacionária.')
        df_diff = ts_log_moving_avg_diff.copy()

        
    if retorno_teste_df['p-value'] > 0.05:
        
        df_diff = calcula_derivada(ts_log_moving_avg_diff)
                        
        retorno_teste_df = teste_dickey_fuller(df_diff)


    df_modelo = renomeia_colunas(df_diff)


    # Caminho relativo do modelo
    caminho_relativo_modelo = './models/model_teste/modelo_treinado.pkl'

    # Verificar a pasta de trabalho atual
    # pasta_trabalho_atual = os.getcwd()

    # Construir o caminho absoluto do modelo
    caminho_absoluto_modelo = os.path.abspath(caminho_relativo_modelo)

    # Verificar se o arquivo existe no caminho absoluto
    if os.path.isfile(caminho_absoluto_modelo):
                
        # Carregar o modelo
        modelo = joblib.load(caminho_absoluto_modelo)
        predicoes = modelo.predict(df_modelo)

        df_futuro = calcular_e_exibir_diferenca(predicoes)
        
        df_futuro['Tendência'] = df_futuro['Tendência'].round(2)
        df_futuro['Valor Previsto'] = df_futuro['Valor Previsto'].round(2)
        df_futuro['Diferença Percentual (%)'] = df_futuro['Diferença Percentual (%)'].round(2)

    else:
        st.write("O arquivo não foi encontrado no caminho especificado.")


    st.markdown(""" 
    #### Gráfico de Média Móvel
    O gráfico apresenta a previsão do preço do petróleo Brent, a tendência ao longo do tempo e a média móvel de 7 dias. A média móvel suaviza as flutuações diárias e ajuda a identificar tendências de longo prazo.""")

    media_valores, mediana_valores, desvio_padrao_valores = plot_forecast_predict(predicoes, 
                      cor_previsao='#FF7F3E', 
                      cor_tendencia='#3AA6B9', 
                      cor_media_movel='#000000')

    return df_futuro, media_valores, mediana_valores, desvio_padrao_valores


