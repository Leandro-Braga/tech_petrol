
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def bar_grafico(df, x_coluna, y_coluna):
   
    cor_clara = '#DCF2F1'

    df = df.groupby(x_coluna)[[y_coluna]].sum().sort_values(y_coluna, ascending=False).reset_index().head(10)

    # Criação do gráfico com Plotly Express
    fig = px.bar(df, x=x_coluna, y=y_coluna,
                # orientation='h',
                title=f'Valores totais por Categorização',
                labels={x_coluna:x_coluna, y_coluna:y_coluna},
                text_auto='.2s',
                color=x_coluna,

                color_discrete_sequence=px.colors.qualitative.Prism ## OK (TEM VERDE)

                )

    fig.update_layout(
    title_font=dict(size=20),
    plot_bgcolor='rgba(0, 0, 0, 0)', 
    paper_bgcolor='rgba(0, 0, 0, 0)', 
    font_color='white',
    xaxis_tickangle=-25,
    yaxis_tickprefix='R$ ',
    legend=dict(font=dict(size=18)),
    width=1200,
    height=500,
    # Tamanho do gráfico
    # width=1080,
    # height=980,
    
    # Configurar cor e tamanho da fonte dos rótulos dos eixos
    xaxis=dict( # xaxis=dict(gridcolor='red'), 
        title=dict(text='', font=dict(size=20, color=cor_clara)), 
        tickfont=dict(size=15, color=cor_clara)
    ),

    yaxis=dict(gridcolor=cor_clara,
        title=dict(text='Valor', font=dict(size=18, color=cor_clara)),  
        tickfont=dict(size=18, color=cor_clara),
        tickprefix='R$ ',
    ),
        )
    

    fig.update_traces(
        # Configurar a cor e a fonte do hover_data
        hoverlabel=dict(
            bgcolor='#0C2D57',  
            font=dict(family='Arial', size=20, color='white'), 
            namelength=-1  # Mostra o nome completo mesmo que seja longo  
        ),   

        # Aumentar o tamanho do rótulo das barras
        textfont=dict(size=20, color='white')
    )


    fig.show()
    # st.plotly_chart(fig)
        

def line_grafico(df, x_coluna, y_coluna, categoria_coluna, titulo_data, legenda):
    
    cor_clara = '#DCF2F1'


    # Criação do gráfico com Plotly Express
    fig = px.line(df, x=x_coluna, y=y_coluna, color=categoria_coluna,
                  title=f'Valores por: {titulo_data} - ({legenda})',
                  labels={x_coluna: x_coluna, y_coluna: y_coluna},
                  color_discrete_sequence=px.colors.sequential.Agsunset,
                  markers=True)
   

    # Atualizar o layout do gráfico
    fig.update_layout(
        title_font=dict(size=20),
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        paper_bgcolor='rgba(0, 0, 0, 0)', 
        font_color='white',
        xaxis_tickangle=-30,
        yaxis_tickprefix='R$ ',
        legend=dict(font=dict(size=20)),

        # Tamanho do gráfico
        width=1200,
        height=600,

        xaxis=dict(
            title=dict(text='', font=dict(size=18, color=cor_clara)),
            tickfont=dict(size=18, color=cor_clara)
        ),

        yaxis=dict(
            gridcolor=cor_clara,
            title=dict(text='Valor', font=dict(size=18, color=cor_clara)),
            tickfont=dict(size=18, color=cor_clara),
            tickprefix='R$ ',
        ),
    )

    # Configurar o tamanho da linha
    fig.update_traces(
        line=dict(width=4),  
        marker=dict(size=9),  
        # Configurar a cor e a fonte do hover_data
        hoverlabel=dict(
            bgcolor='#0C2D57',  
            font=dict(family='Arial', size=16, color='white'), 
            # font=dict(family='Arial', size=16, color='#000000'), 
            namelength=-1  # Mostra o nome completo mesmo que seja longo
        ),
        
        # Aumentar o tamanho do rótulo das barras
        textfont=dict(size=20, color='white')
    )

    # fig.show()
    st.plotly_chart(fig)


def histograma_grafico(df, x_coluna, y_coluna, titulo_data, legenda):
    fig = px.histogram(
        df, 
        x=x_coluna, 
        color=y_coluna, 
        color_discrete_sequence=px.colors.sequential.Agsunset,
        title=titulo_data
    )
    fig.update_layout(
        title_font=dict(size=20),
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        paper_bgcolor='rgba(0, 0, 0, 0)', 
        font_color='white',
        legend_title_text=legenda,
        # Tamanho do gráfico
        width=1200,
        height=600,
        # template='plotly_dark'
    )

    st.plotly_chart(fig)


def box_grafico(df, x_coluna, y_coluna, titulo_data, legenda):
    fig = px.box(
        df, 
        x=x_coluna, 
        color_discrete_sequence=px.colors.sequential.Blues, 
        labels={x_coluna: y_coluna}, 
        orientation='h', 
        hover_data=['PRECO'], 
        hover_name='PRECO'
    )
    
    fig.update_layout(
        title=titulo_data,
        title_font=dict(size=20),
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        paper_bgcolor='rgba(0, 0, 0, 0)', 
        font_color='white',
        legend_title_text=legenda,
        width=1200,
        height=600,
    )
    
    st.plotly_chart(fig)


def grafico_momento_preco(df_oleo):
    
    # Função para plotar momentos chave no gráfico
    
    def plot_momentos_chaves_preco_petroleo(fig, df_oleo, evento):
        for ponto, id_evento in evento.items():
            if not df_oleo.query(f'DATA == "{ponto}"').empty:
                fig.add_trace(go.Scatter(
                    x=[ponto], 
                    y=[float(df_oleo.query(f'DATA == "{ponto}"')['PRECO'])], 
                    mode='markers+text', 
                    marker=dict(size=12, symbol='circle', color='red', line=dict(width=1, color='red')),
                    text=[id_evento.split('.')[0]],  # Apenas o número do evento
                    textposition="top center",
                    textfont=dict(color='red', size=14, family="Arial Black"),
                    hovertext=[id_evento],  # Texto do evento para o hover
                    hoverinfo="text",  # Exibir apenas o texto no hover
                    showlegend=False,
                    hoverlabel=dict(
                            bgcolor='#973131',
                            # bgcolor='#E4003A',
                            font=dict(family='Arial', size=13, color='white'))
                ))

    # Função para definir a legenda personalizada
    def set_legenda(fig):
        fig.update_layout(
            legend=dict(
                title='Legenda',
                itemsizing='constant'
            )
        )

    # Eventos chave
    eventos = {
        '1990-08-02': '1. Guerra do Golfo (1990-1991)',
        '2001-09-11': '2. Atentados terroristas nos EUA (2001)',
        '2003-03-20': '3. Guerra do Iraque (2003-2011)',
        '2007-08-01': '4. Crise financeira global (2007-2008)',
        '2010-12-20': '5. Primavera Árabe (2010-2012)',
        '2011-02-17': '6. Guerra Civil na Líbia (2011)',
        '2011-03-15': '7. Conflito na Síria (a partir de 2011)',
        '2014-11-28': '8. OPEP mantém ritmo de produção (2014)',
        '2015-01-02': '9. Grande produção e baixa demanda (2015)',
        '2020-01-30': '10. Pandemia de COVID-19 (2020-2022)',
        '2021-07-01': '11. Recuperação econômica pós-COVID (2021-presente)',
        '2022-02-24': '12. Conflito Rússia-Ucrânia (2022-presente)',
        '2023-01-04': '13. Decisões da OPEC+ e COVID-19 (2022-2023)'
    }

    # Parâmetros de personalização
    titulo_cor = 'white'
    eixo_x_cor = 'white'
    eixo_y_cor = 'white'
    linha_cor = '#405D72'

    # Criar o gráfico
    fig = go.Figure()

    # Adicionar a linha do gráfico
    fig.add_trace(go.Scatter(
        x=df_oleo['DATA'], 
        y=df_oleo['PRECO'], 
        mode='lines', 
        name='Preço do Petróleo',
        line=dict(color=linha_cor)
    ))

    # Plotar os momentos chave
    plot_momentos_chaves_preco_petroleo(fig, df_oleo, eventos)

    # Personalizar cores do título e eixos
    fig.update_layout(
        title='Evolução do preço do barril de petróleo Brent ao longo das décadas (1987 até hoje)',
        title_font=dict(color=titulo_cor, size=20),
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        paper_bgcolor='rgba(0, 0, 0, 0)', 
        width=1200,
        height=600,
        xaxis=dict(title='Ano', title_font=dict(color=eixo_x_cor), tickfont=dict(color=eixo_x_cor)),
        yaxis=dict(title='Preço em US$', title_font=dict(color=eixo_y_cor), tickfont=dict(color=eixo_y_cor)),
        showlegend=False
    )

    # Definir a legenda personalizada
    set_legenda(fig)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)


def plot_forecast(model_name, treino, forecast_df):

    # Parâmetros de personalização
    titulo_cor = 'white'
    eixo_x_cor = 'white'
    eixo_y_cor = 'white'
    # linha_cor = '#405D72'
    
    # Função para plotar os dados de treino, teste e previsões
    # Adicionar colunas de tipo
    treino['tipo'] = 'Treino'
    forecast_df['tipo'] = f'Previsão {model_name}'

    # Combinar dados de treino e previsão
    df_treino_teste = treino[['ds', 'y', 'tipo']]
    df_previsao = forecast_df[['ds', model_name, 'y', 'tipo']].rename(columns={model_name: 'Previsão'})

    # Plotar gráfico
    fig = px.line(df_treino_teste, x='ds', y='y', color='tipo')
    fig.add_scatter(x=df_previsao['ds'], y=df_previsao['Previsão'], mode='lines', name=f'Previsão {model_name}', line=dict(color='orange'))
    fig.add_scatter(x=df_previsao['ds'], y=df_previsao['y'], mode='lines', name='Real', line=dict(color='blue'))

    fig.update_layout(
        title=f'Treino, Teste e Previsões do Modelo {model_name}',
        title_font=dict(color=titulo_cor, size=20),
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        paper_bgcolor='rgba(0, 0, 0, 0)', 
        width=1200,
        height=600,
        xaxis=dict(title='Ano', title_font=dict(color=eixo_x_cor), tickfont=dict(color=eixo_x_cor)),
        yaxis=dict(title='Preço em US$', title_font=dict(color=eixo_y_cor), tickfont=dict(color=eixo_y_cor)),
    )
    
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)


def plot_forecast_prophet(model_name, treino, forecast_df, forecast_col='Previsão'):
   
    # Parâmetros de personalização
    titulo_cor = 'white'
    eixo_x_cor = 'white'
    eixo_y_cor = 'white'

    # Adicionar colunas de tipo
    treino['tipo'] = 'Treino'
    forecast_df['tipo'] = f'Previsão {model_name}'

    # Combinar dados de treino e previsão
    df_treino_teste = treino[['ds', 'y', 'tipo']]
    df_previsao = forecast_df[['ds', forecast_col, 'y', 'tipo']].rename(columns={forecast_col: 'Previsão'})

    # Plotar gráfico
    fig = px.line(df_treino_teste, x='ds', y='y', color='tipo')
    fig.add_scatter(x=df_previsao['ds'], y=df_previsao['Previsão'], mode='lines', name=f'Previsão {model_name}', line=dict(color='orange'))
    fig.add_scatter(x=df_previsao['ds'], y=df_previsao['y'], mode='lines', name='Real', line=dict(color='blue'))

    fig.update_layout(
        title=f'Treino, Teste e Previsões do Modelo {model_name}',
        title_font=dict(color=titulo_cor, size=20),
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        paper_bgcolor='rgba(0, 0, 0, 0)', 
        width=1200,
        height=600,
        xaxis=dict(title='Ano', title_font=dict(color=eixo_x_cor), tickfont=dict(color=eixo_x_cor)),
        yaxis=dict(title='Preço em US$', title_font=dict(color=eixo_y_cor), tickfont=dict(color=eixo_y_cor)),
    )  
    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)


def plot_forecast_predict(df_previsao, 
                          cor_previsao='blue', 
                          cor_tendencia='red', 
                          cor_media_movel='green'):
    
    # Parâmetros de personalização
    titulo_cor = 'white'
    eixo_x_cor = 'white'
    eixo_y_cor = 'white'

    # Converter a coluna de data para datetime
    df_previsao['ds'] = pd.to_datetime(df_previsao['ds'])

    # Formatar a coluna de data para o formato dia/mês/ano
    df_previsao['ds'] = df_previsao['ds'].dt.strftime('%d/%m/%Y')

   
    # Criar um gráfico usando plotly.graph_objects para personalização avançada
    fig = go.Figure()

    # Adicionar a linha de previsões
    fig.add_trace(go.Scatter(x=df_previsao['ds'], 
                             y=df_previsao['yhat'], 
                             mode='lines', 
                             name='Previsão', 
                             line=dict(color=cor_previsao)))

    # Adicionar a linha de tendência
    fig.add_trace(go.Scatter(x=df_previsao['ds'], 
                             y=df_previsao['trend'], 
                             mode='lines', 
                             name='Tendência', 
                             line=dict(color=cor_tendencia)))

    # Calcular a média móvel de 7 dias
    df_previsao['media_movel_7d'] = df_previsao['yhat'].rolling(window=7).mean()

    # Adicionar a média móvel ao gráfico
    fig.add_trace(go.Scatter(x=df_previsao['ds'], 
                             y=df_previsao['media_movel_7d'], 
                             mode='lines', 
                             name='Média Móvel 7 dias', 
                             line=dict(color=cor_media_movel)))

    # Atualizar layout do gráfico
    fig.update_layout(
        title='Previsões do Modelo',
        title_font=dict(color=titulo_cor, size=20),
        plot_bgcolor='rgba(0, 0, 0, 0)', 
        paper_bgcolor='rgba(0, 0, 0, 0)', 
        width=1200,
        height=600,
        xaxis=dict(title='Data', title_font=dict(color=eixo_x_cor), tickfont=dict(color=eixo_x_cor)),
        yaxis=dict(title='Preço em US$', title_font=dict(color=eixo_y_cor), tickfont=dict(color=eixo_y_cor)),
        xaxis_tickformat='%d/%m/%Y', # Formatar datas no eixo X
    )

    # Adicionar alguma análise estatística interessante
    media_valores = df_previsao['yhat'].mean()
    mediana_valores = df_previsao['yhat'].median()
    desvio_padrao_valores = df_previsao['yhat'].std()

    st.write(f"📊 **Média das previsões:** :orange[{media_valores:.2f}]")
    st.write(f"📊 **Mediana das previsões:** :orange[{mediana_valores:.2f}]")
    st.write(f"📊 **Desvio padrão das previsões:** :orange[{desvio_padrao_valores:.2f}]")

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)

    return media_valores, mediana_valores, desvio_padrao_valores


