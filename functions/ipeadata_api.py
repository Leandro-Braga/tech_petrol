
import numpy as np
import pandas as pd
import requests


def get_ipeadata():

    # URL da API do Ipeadata para o EMBI+ Risco-Brasil
    url = "http://www.ipeadata.gov.br/api/odata4/ValoresSerie(SERCODIGO='EIA366_PBRENT366')"

    # Realizando a requisição GET
    response = requests.get(url)

    # Verificando o status da requisição
    if response.status_code == 200:
    
        # Convertendo os dados para formato JSON
        data = response.json()
        
        # Extraindo os valores da série temporal
        values = data['value']
        
        # Convertendo para um DataFrame do Pandas
        df_ipea = pd.DataFrame(values)
        # Filtro das colunas
        filtro_ipea = ['VALDATA', 'VALVALOR']
        df_ipea2 = df_ipea[filtro_ipea]
        df_ipea2.columns = ['DATA', 'PRECO']
        
        # Convertendo a coluna DATA para o tipo datetime
        df_ipea2['DATA'] = pd.to_datetime(df_ipea2['DATA'].str[0:10], format='%Y-%m-%d')
        df_ipea2['PRECO'] = df_ipea2['PRECO'].fillna(0)

        df_ipea2.replace(0, np.nan, inplace=True)

        # Preencher os valores NaN com os valores anteriores
        df_ipea2.ffill(inplace=True)

        # Preencher os valores NaN restantes com os valores subsequentes
        df_ipea2.bfill(inplace=True)

        df_ipea2['PRECO_MEDIO'] = pd.cut(df_ipea2['PRECO'], 
                    bins=[0, 9, 10, 20, 30, 40, 50, 60, 100, float('inf')], 
                    labels=['0', '9','10', '20','30', '40', '50', '60', '100+'])
        df_ipea2['PRECO_MEDIO'] = df_ipea2['PRECO_MEDIO'].fillna('0')
            
    else:
        print("Erro ao acessar a API do Ipeadata:", response.status_code)
    
    return df_ipea2
