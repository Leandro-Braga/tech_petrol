from prophet import Prophet
from statsforecast import StatsForecast
from statsforecast.models import AutoARIMA, Naive

# from fbprophet import Prophet

# from statsforecast import StatsForecast
# from statsforecast.models import AutoARIMA


def naive_model(treino, valid, h):
        
    model = StatsForecast(models=[Naive()], freq='D', n_jobs=-1)
    model.fit(treino)

    forecast_df = model.predict(h=h, level=[90])
    forecast_df = forecast_df.reset_index().merge(valid, on=['ds', 'unique_id'], how='left')
    
    return model, forecast_df


def auto_arima_model(treino, valid, h):
    
    # Garantir que apenas as colunas necessárias estão presentes
    treino = treino[['unique_id', 'ds', 'y']]
    valid = valid[['unique_id', 'ds', 'y']]
    
    # Instanciar e treinar o modelo AutoARIMA
    model = StatsForecast(models=[AutoARIMA(season_length=7)], freq='D', n_jobs=-1)
    model.fit(treino)
    
    # Prever usando o modelo treinado
    forecast_df = model.predict(h=h, level=[90])
    forecast_df = forecast_df.reset_index().merge(valid, on=['ds', 'unique_id'], how='left')
    
    return model, forecast_df

### - Modelo Original - ###
def prophet_model(treino, valid, h, cps, sps):
        
    model = Prophet(daily_seasonality=True,seasonality_mode='multiplicative',changepoint_prior_scale=cps,seasonality_prior_scale=sps)
    model.fit(treino)

    future = model.make_future_dataframe(periods=h)
    forecast = model.predict(future)

    # fazendo previsões com os dados de teste
    test_forecast = model.predict(valid)
    
    # olhando os resultados das previsões com os dados de teste
    forecast_df = test_forecast.reset_index().merge(valid, on=['ds'], how='left')

    return model, forecast, forecast_df





# def prophet_model(treino, valid, h, cps, sps):
#     # Definir e ajustar o modelo Prophet
#     # model = Prophet(
#     #     daily_seasonality=True,
#     #     weekly_seasonality=False,
#     #     yearly_seasonality=True,
#     #     seasonality_mode='multiplicative',
#     #     changepoint_prior_scale=cps,
#     #     seasonality_prior_scale=sps,
#     #     holidays_prior_scale=10.0,
#     #     changepoint_range=0.8
#     # )

#     model = Prophet(daily_seasonality=True,
#                     seasonality_mode='multiplicative',
#                     changepoint_prior_scale=cps,
#                     seasonality_prior_scale=sps,
#                     holidays_prior_scale=10.0)

    
#     model.add_country_holidays(country_name='BR')
#     model.fit(treino)

#     # Fazer previsões para o futuro
#     future = model.make_future_dataframe(periods=h)
#     forecast = model.predict(future)

#     # Fazer previsões com os dados de teste
#     test_forecast = model.predict(valid)
    
#     # Combinar previsões com dados reais
#     forecast_df = test_forecast[['ds', 'yhat']].merge(valid[['ds', 'y']], on='ds', how='left')

#     return model, forecast, forecast_df




