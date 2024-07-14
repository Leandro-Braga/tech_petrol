
import plotly.express as px


def bar_grafico(df, x_coluna, y_coluna):
   
    cor_clara = '#DCF2F1'

    df = df.groupby(x_coluna)[[y_coluna]].sum().sort_values(y_coluna, ascending=False).reset_index().head(10)

    # Criação do gráfico com Plotly Express
    fig = px.bar(df, x=x_coluna, y=y_coluna,
                # orientation='h',
                title=f'Valores totais por Categorização',
                labels={x_coluna:x_coluna, y_coluna:y_coluna},
                text_auto='.2s',

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
            namelength=-1  # Mostra o nome completo mesmo que seja longo
        ),
        
        # Aumentar o tamanho do rótulo das barras
        textfont=dict(size=20, color='white')
    )

    fig.show()


