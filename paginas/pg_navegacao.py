from datetime import date, timedelta

import pandas as pd
import streamlit as st

from analise.desctritiva import get_desctritiva, tabela_descritiva
from grafo.grafico_gerais import (box_grafico, grafico_momento_preco,
                                  histograma_grafico, line_grafico)
from models.modelo_app import (modelo_auto_arima, modelo_naive, modelo_prophet,
                               modelo_prophet_previsao)


def init_session_state():

    # # Defina as páginas
    pages = {
        "Introdução": "introducao",
        "Análise Exploratória": "analise_exploratoria",
        "Modelos de Previsão": "modelos_previsao",
    }

    # Adicione a navegação na sidebar
    st.sidebar.title("Navegação")
    selection = st.sidebar.radio("Ir para", list(pages.keys()))

    cor_titulo = '#00ABB3' 
    cor_texto = '#C7C8CC'
    tamanho_texto = '16px'

    if selection == "Introdução":

        st.markdown(f'<h1 style="text-align: left; color: {cor_titulo}; font-size: 40px;">{selection} | Tech Challenge 4</h1>', unsafe_allow_html=True)

        st.markdown(f"""<h1 style="text-align: left; color: {cor_texto}; font-size: {tamanho_texto};">Este projeto analisa as flutuações históricas do preço do petróleo Brent e desenvolve modelos de machine learning para prever valores futuros. O Brent é uma referência crucial no mercado internacional, influenciando preços em transações comerciais. Utilizaremos análises estatísticas e visualização de dados para identificar padrões e fatores como oferta, demanda e eventos geopolíticos que afetam os preços. <br><br> Desenvolveremos 3 modelos de machine learning baseados em séries temporais, combinando CNN e LSTM, para melhorar a precisão das previsões e fornecer insights estratégicos sobre a volatilidade dos preços do petróleo. <br><br>
        Esses modelos não apenas melhorarão a precisão das previsões, mas também ajudarão a compreender melhor os fatores que causam a volatilidade dos preços do petróleo, fornecendo uma base sólida para decisões estratégicas no mercado de energia.</h1>
        """, unsafe_allow_html=True)

        st.subheader("", divider="gray")
        # blue, green, orange, red, violet, gray, grey, rainbow.
        
        st.markdown(f'<h1 style="text-align: left; color: {cor_titulo}; font-size: 40px;">Objetivo</h1>', unsafe_allow_html=True)

        st.markdown(f"""<h1 style="text-align: left; color: {cor_texto}; font-size: {tamanho_texto};">
        1. Criar um dashboard interativo que ofereça insights sobre variações no preço do petróleo Brent, considerando fatores como geopolítica e economia. <br><br>
        2. Desenvolver um modelo de Machine Learning para prever os preços diários do petróleo. <br><br>
        3. Elaborar um plano para o deploy do modelo em produção. <br><br>
        4. Criar um MVP usando Streamlit para apresentar o modelo e os insights de forma acessível.</h1>
        """, unsafe_allow_html=True)
        
     
        st.subheader("", divider="gray")

        st.markdown(f'<h1 style="text-align: left; color: {cor_titulo}; font-size: 40px;">Instituto de Pesquisa Econômica Aplicada (IPEA)</h1>', unsafe_allow_html=True)
        
        st.markdown(""" 
            O Instituto de Pesquisa Econômica Aplicada (IPEA) é uma fundação pública federal brasileira, vinculada ao Ministério do Planejamento e Orçamento. Criado em 1964, o IPEA tem como missão fornecer suporte técnico e institucional às ações governamentais para a formulação e reformulação de políticas públicas e programas de desenvolvimento econômico e social.

            ### Tabela de Preço do Barril de Petróleo Brent

            A tabela do Preço do Barril de Petróleo Brent do IPEA faz parte do Ipeadata, uma base de dados macroeconômicos, financeiros e regionais. Esta tabela fornece dados históricos sobre os preços do petróleo Brent, que são essenciais para análises econômicas e para entender as flutuações de preços no contexto global.

            O IPEA disponibiliza esses dados para o público, permitindo sua utilização em estudos, gráficos e outras análises, desde que a fonte seja citada. A série histórica dos preços do petróleo Brent é uma ferramenta valiosa para pesquisadores, economistas e formuladores de políticas, ajudando a monitorar e analisar as tendências do mercado de petróleo ao longo dos anos.

            Para mais detalhes, acessar o site oficial do Ipeadata: [Ipeadata](http://ipeadata.gov.br/Default.aspx) | [Ipeadata Tabela Preço do Barril de Petroleo Brent](http://www.ipeadata.gov.br/ExibeSerie.aspx?module=m&serid=1650971490&oper=view)
            """)


    elif selection == "Análise Exploratória":

        st.markdown(f'<h1 style="text-align: left; color: {cor_titulo}; font-size: 40px;">{selection}</h1>', unsafe_allow_html=True)
        
        st.subheader("", divider="gray")

        tab1, tab2 = st.tabs(['📒 Análise Descritiva', '💵 Analisando a Variação do Preço'])
 

        with tab1:
            df = get_desctritiva() # IPEADATA
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f'<h1 style="text-align: left; color: {cor_texto}; font-size: 18px;">Tabela descritiva:</h1>', unsafe_allow_html=True)
                
                st.table(df[['PRECO']].describe().T.reset_index()[['count', 
                                                                   'mean', 
                                                                   'std', 
                                                                   'min', 
                                                                   '25%', 
                                                                   '50%', 
                                                                   '75%', 
                                                                   'max']])
            with col2:

                count, mean, std, min, q25, q50, q75, max = tabela_descritiva(df)
 
                st.write(f">Apresentamos a tabela de análise descritiva da distribuição de preços ao longo das décadas. Os dados consistem em :blue[{count}] observações, com uma média de :blue[{mean}] e um desvio padrão de :blue[{std}]. O valor mínimo registrado é **:green[{min}]**, enquanto o valor máximo é **:red[{max}]**. Os quartis mostram que **:orange[25%]** dos dados estão abaixo de :blue[{q25}], **:orange[50%]** abaixo de :blue[{q50}] (mediana) e **:orange[75%]** abaixo de :blue[{q75}], proporcionando uma visão detalhada da distribuição e variabilidade dos preços.", unsafe_allow_html=True)


            st.subheader("", divider="gray")

            texto_titulo_base = 'Preços do Petroleo Brent ao Longo dos Anos'

            st.markdown(f'<h1 style="text-align: left; color: {cor_texto}; font-size: 18px;">{texto_titulo_base}:</h1>', unsafe_allow_html=True)

            st.markdown(""" 
                Este gráfico apresenta a evolução dos preços do petróleo Brent ao longo dos anos, conforme registrado pelo IPEADATA. Vamos analisar os principais pontos:

                - **:orange[Período de Estabilidade (1986-2000)]**: Durante esse período, os preços do petróleo Brent permaneceram relativamente estáveis, flutuando principalmente entre \$20 e \$40.
                
                - **:orange[Alta de Preços (2000-2008)]**: A partir do ano 2000, observamos um aumento significativo nos preços, culminando em um pico próximo de \$140 em 2008. Esse aumento pode ser associado a fatores geopolíticos, aumento da demanda global e restrições na oferta.

                - **:orange[Queda e Recuperação (2008-2014)]**: Após o pico de 2008, houve uma queda acentuada nos preços devido à crise financeira global, seguida por uma recuperação gradual até 2014.

                - **:orange[Declínio e Flutuações (2014-2020)]**: Entre 2014 e 2020, os preços do petróleo Brent apresentaram declínios e oscilações, refletindo as variações na oferta e demanda global, bem como as tensões geopolíticas.

                - **:orange[Recuperação Recente (2020-2025)]**: Observa-se uma recuperação nos preços a partir de 2020, embora com volatilidade, refletindo as incertezas econômicas e as variações na produção de petróleo.

                O gráfico usa uma paleta de cores para indicar diferentes faixas de preços, facilitando a visualização das flutuações ao longo do tempo.
                """, unsafe_allow_html=True)

            x_coluna = 'DATA'
            y_coluna = 'PRECO'
            categoria_coluna = 'PRECO_MEDIO'
            titulo_data = 'Preços do Petroleo'
            legenda = 'IPEADATA'

            line_grafico(df, x_coluna, y_coluna, categoria_coluna, titulo_data, legenda)

            st.subheader("", divider="gray")

            texto_titulo_base = 'Histograma dos Preços do Petroleo Brent'

            st.markdown(f'<h1 style="text-align: left; color: {cor_texto}; font-size: 18px;">{texto_titulo_base}:</h1>', unsafe_allow_html=True)

            st.markdown("""
                Este gráfico apresenta a distribuição dos preços do petróleo Brent ao longo dos anos, conforme registrado pelo IPEADATA. Vamos analisar os principais pontos:

                - **:orange[Pico de Preços Baixos]**: A maioria dos preços está concentrada na faixa entre **\$10 e \$20**, indicando que historicamente, o preço do petróleo Brent permaneceu baixo por um período significativo de tempo.
                
                - **:orange[Distribuição de Preços Médios]**: Observa-se uma quantidade moderada de preços na faixa entre **\$30 e \$60**, mostrando que houve períodos de aumento nos preços, mas não tão frequentes quanto os preços mais baixos.

                - **:orange[Alta de Preços]**: Há uma presença notável de preços acima de **\$100**, refletindo os picos de preços mais recentes devido a diversos fatores econômicos e geopolíticos.

                - **:orange[Menor Frequência em Altos Valores]**: Preços acima de **\$60** são menos frequentes, indicando que valores extremamente altos são menos comuns na distribuição histórica dos preços do petróleo Brent.
                """)

            x_coluna = 'PRECO'
            y_coluna = 'PRECO_MEDIO'
            categoria_coluna = 'PRECO_MEDIO'
            titulo_data = 'Histograma dos Preços do Petroleo'
            legenda = 'Media IPEADATA'

            histograma_grafico(df, x_coluna, y_coluna, titulo_data, legenda)

            st.subheader("", divider="gray")

            texto_titulo_base = 'Gráfico Box Plot dos Preços do Petroleo Brent'

            st.markdown(f'<h1 style="text-align: left; color: {cor_texto}; font-size: 18px;">{texto_titulo_base}:</h1>', unsafe_allow_html=True)

            st.markdown("""
                Este gráfico box plot apresenta a distribuição dos preços do petróleo Brent ao longo dos anos. Vamos analisar os principais pontos:

                - **:orange[Mediana]**: 
                    - A linha dentro da caixa representa a mediana dos preços, que é aproximadamente **\$34,4**. Isso indica que metade dos preços do petróleo Brent foram inferiores a esse valor, enquanto a outra metade foi superior.

                - **:orange[Quartis]**:
                    - O primeiro quartil (Q1) está em **\$18,63**, indicando que **25%** dos preços do petróleo Brent foram inferiores a esse valor.
                    - O terceiro quartil (Q3) está em **\$45,5**, mostrando que **75%** dos preços foram inferiores a esse valor.

                - **:orange[Valores Extremos (Outliers)]**:
                    - O valor mínimo é aproximadamente **R$9,1**.
                    - O valor máximo é aproximadamente **R$143,95**.
                
                - **:orange[Intervalo Interquartil (IQR)]**:
                    - O intervalo interquartil (IQR) é a diferença entre Q3 e Q1, que é aproximadamente **\$26,87**. Este valor representa a dispersão do meio **50%** dos dados.

                - **:orange[Caixa]**:
                    - A caixa do gráfico mostra onde estão concentrados os **50%** intermediários dos preços, entre os valores de Q1 e Q3.

                - **:orange[Extensão (Whiskers)]**:
                    - As linhas que se estendem das caixas (whiskers) mostram a variação dos dados fora dos quartis, mas dentro de 1,5 vezes o intervalo interquartil a partir dos quartis.

                Este gráfico revela que, ao longo dos anos, a maioria dos preços do petróleo Brent se concentrou entre **\$18,63** e **\$45,5**, com alguns valores fora dessa faixa, indicando períodos de volatilidade significativa.
                """)
    
            x_coluna = 'PRECO'
            y_coluna = 'PRECO_MEDIO'
            categoria_coluna = 'PRECO_MEDIO'
            titulo_data = 'Gráfico Box Plot dos Preços do Petroleo'
            legenda = 'Media IPEADATA'

            box_grafico(df, x_coluna, y_coluna, titulo_data, legenda)



        with tab2:

            st.markdown("""
            ### Análise do Gráfico: Evolução do Preço do Barril de Petróleo Brent

            O gráfico ilustra a evolução dos preços do barril de petróleo Brent ao longo das décadas, de 1987 até hoje, destacando momentos chave que influenciaram significativamente as flutuações dos preços. Ao longo desse período, eventos geopolíticos, econômicos e sociais desempenharam papéis cruciais na variação dos preços desta commodity essencial para a economia global. Vamos analisar esses eventos e seu impacto nos preços do petróleo:

            1. **:orange[Guerra do Golfo (1990-1991)]**:
                - A invasão do Kuwait pelo Iraque em agosto de 1990 levou a um aumento significativo nos preços do petróleo devido à incerteza sobre a oferta. 
                - Fonte: [g1.globo.com](https://g1.globo.com/mundo/noticia/2020/08/02/o-que-mudou-no-kuwait-30-anos-depois-da-invasao-do-iraque-por-saddam-hussein.ghtml)

            2. **:orange[Atentados terroristas nos EUA (2001)]**:
                - Os ataques de 11 de setembro de 2001 causaram uma alta nos preços do petróleo devido ao medo de instabilidade geopolítica e interrupções no fornecimento.
                - Fonte: [BBC News](https://www.bbc.com/portuguese/internacional-55351015)

            3. **:orange[Guerra do Iraque (2003-2011)]**:
                - A invasão do Iraque pelos EUA em março de 2003 resultou em preocupações sobre a produção de petróleo e sua distribuição, levando a uma alta nos preços.
                - Fonte: [The Guardian](https://www.theguardian.com/world/2004/sep/16/iraq.iraq)

            4. **:orange[Crise financeira global (2007-2008)]**:
                - A crise financeira de 2007-2008 provocou uma queda acentuada na demanda por petróleo, resultando em uma queda abrupta nos preços.
                - Fonte: [exame.com](https://exame.com/economia/ha-10-anos-crise-financeira-de-2008-arrasava-a-economia-mundial/)

            5. **:orange[Primavera Árabe (2010-2012)]**:
                - A série de protestos e revoluções no mundo árabe criou incertezas sobre a produção de petróleo, levando a uma volatilidade nos preços.
                - Fonte: [BBC News](https://www.bbc.com/portuguese/internacional-55379502)

            6. **:orange[Guerra Civil na Líbia (2011)]**:
                - O conflito na Líbia, um dos maiores produtores de petróleo da África, causou interrupções na oferta, resultando em picos de preço.
                - Fonte: [g1.globo](https://g1.globo.com/revolta-arabe/noticia/2011/02/entenda-crise-na-libia.html)

            7. **:orange[Conflito na Síria (2011~)]**:
                - O conflito sírio aumentou a instabilidade na região, afetando os preços do petróleo devido às preocupações com a oferta.
                - Fonte: [BBC News](https://www.bbc.com/portuguese/internacional-56378202)

            8. **:orange[OPEP mantém ritmo de produção (2014)]**:
                - Em 2014, a decisão da OPEP de manter os níveis de produção apesar do excesso de oferta levou a uma queda nos preços do petróleo.
                - Fonte: [exame.com](https://exame.com/invest/mercados/opep-mantem-producao-para-nao-desequilibrar-nivel-de-precos/)

            9. **:orange[Grande produção e baixa demanda (2015)]**:
                - A combinação de alta produção e baixa demanda global em 2015 causou uma queda significativa nos preços do petróleo.
                - Fonte: [embrapa](https://www.embrapa.br/visao/intensificacao-e-sustentabilidade-dos-sistemas-de-producao-agricolas)

            10. **:orange[Pandemia de COVID-19 (2020-2023)]**:
                - A pandemia de COVID-19 resultou em uma redução drástica na demanda por petróleo, causando uma queda acentuada nos preços.
                - Fonte: [CNN Brasil](https://www.cnnbrasil.com.br/economia/macroeconomia/opep-reduz-projecao-de-demanda-por-petroleo-por-causa-do-coronavirus/)

            11. **:orange[Recuperação econômica pós-COVID (2021~)]**:
                - A recuperação econômica após o auge da pandemia levou a um aumento na demanda por petróleo, resultando em uma recuperação dos preços.
                - Fonte: [International Energy Agency](https://www.iea.org/reports/oil-market-report-january-2021)

            12. **:orange[Conflito Rússia-Ucrânia (2022~)]**:
                - A invasão da Ucrânia pela Rússia em 2022 criou preocupações sobre a oferta de petróleo, resultando em picos de preços.
                - Fonte: [CNN Brasil](https://www.cnnbrasil.com.br/internacional/analise-russia-faz-maior-avanco-na-ucrania-desde-julho-de-2022/)

            13. **:orange[Decisões da OPEC+ e COVID-19 (2022-2023)]**:
                - As decisões da OPEC+ sobre os níveis de produção, juntamente com os efeitos contínuos da COVID-19, continuaram a influenciar os preços do petróleo.
                - Fonte: [CNBC](https://www.cnbc.com/2021/12/01/opec-meeting-oil-output-policy-in-focus-as-omicron-rattles-markets.html)
                        """)

            grafico_momento_preco(df)

            st.markdown("""
                Em janeiro de 2022 e janeiro de 2023, vários fatores-chave influenciaram as flutuações e quedas nos preços do petróleo Brent:

                1. **:orange[Disrupções na Cadeia de Suprimentos e Tensões Geopolíticas]**: O conflito entre Rússia e Ucrânia impactou significativamente os preços do petróleo. As sanções sobre as exportações de petróleo russo e o embargo da UE criaram incertezas na cadeia de suprimentos global, levando à volatilidade dos preços. As exportações de petróleo da Rússia diminuíram devido a essas sanções, mas recuperaram-se parcialmente, mantendo a incerteza no mercado. 
                Fontes:[[IEA Disrupções](https://www.iea.org/reports/oil-market-report-january-2023)] [[IEA Tensões](https://www.eia.gov/outlooks/steo/report/BTL/2023/01-brentprice/article.php)].

                2. **:orange[Fatores Econômicos Globais]**: Na segunda metade de 2022, os preços do petróleo começaram a cair após um aumento acentuado na primeira metade. Essa queda deveu-se à desaceleração da atividade econômica global, alta inflação e aumento das taxas de juros, que, coletivamente, reduziram a demanda.
                Fontes:[[IEA inflação](https://www.eia.gov/todayinenergy/detail.php?id=50858)] [[IEA Econômicos](https://www.eia.gov/todayinenergy/detail.php?id=55079)].

                3. **:orange[Impacto da COVID-19]**: O levantamento das restrições da COVID-19 na China no final de 2022 inicialmente sugeriu um aumento na demanda. No entanto, o aumento esperado na demanda foi compensado pela desaceleração econômica em outras regiões e por medidas de alta eficiência energética.
                Fontes:[[IEA China’s Covid-restrictions](https://www.iea.org/reports/oil-market-report-january-2023)]

                4. **:orange[Decisões da OPEC+]**: As decisões de produção da OPEC+ desempenharam um papel crucial. Em 2022, a OPEC+ aumentou a produção para atender à demanda em recuperação pós-pandemia, mas o ritmo desacelerou significativamente em 2023, contribuindo para um equilíbrio mais apertado da oferta.
                Fontes:[[IEA OPEC+](https://www.eia.gov/todayinenergy/detail.php?id=50858)] [[IEA produção](https://www.eia.gov/outlooks/steo/report/BTL/2023/01-brentprice/article.php)]

                5. **:orange[Dinâmica das Refinarias dos EUA e Globais]**: Paradas nas refinarias, particularmente nos EUA devido a problemas relacionados ao clima, também afetaram os preços. O processamento global de refinarias aumentou, o que equilibrou algumas preocupações com a oferta, mas manteve os preços sob controle.
                Fontes:[[IEA Report Jan/2023](https://www.iea.org/reports/oil-market-report-january-2023)]

                Esses fatores contribuíram coletivamente para a dinâmica dos preços do petróleo observada no início de 2022 e 2023.                        
                """)

            st.markdown("""### Conclusão \n\n Os preços do petróleo Brent ao longo das últimas décadas foram significativamente influenciados por eventos geopolíticos e econômicos. Cada ponto destacado no gráfico representa um evento que teve um impacto notável nos preços, refletindo a importância do petróleo na economia global e a sensibilidade do mercado a eventos disruptivos.
            """)



    elif selection == "Modelos de Previsão":

        st.markdown(f'<h1 style="text-align: left; color: {cor_titulo}; font-size: 40px;">{selection}</h1>', unsafe_allow_html=True)

        st.subheader("", divider="gray")

        tab1, tab2, tab3 = st.tabs(['👾 Modelo Naive', '💻 Modelo AutoARIMA', '🤖 Modelo Meta Prophet'])

        df = get_desctritiva() # IPEADATA

        with tab1:
            st.markdown(""" 
            ### Modelo Naive e Métrica WMAPE

            🔍 **:orange[Modelo Naive]:**
            O Modelo Naive é uma abordagem de previsão extremamente simples que assume que o valor futuro de uma série temporal será igual ao valor atual ou mais recente. Em outras palavras, ele não leva em consideração nenhum padrão ou tendência nos dados históricos. É frequentemente usado como um ponto de referência inicial para comparação com modelos mais sofisticados.

            🔢 **:orange[Métrica WMAPE] (Weighted Mean Absolute Percentage Error):**
            A métrica WMAPE é usada para avaliar a precisão das previsões. Ela calcula o erro absoluto médio ponderado pela magnitude dos valores reais, expressando-o como uma porcentagem. A fórmula é:
            """)
            st.latex(r"WMAPE = \frac{\sum | \text{Valor Real} - \text{Valor Previsto} |}{\sum \text{Valor Real}} \times 100 \%")
            
            if st.button('Executar Modelo Naive', key='Naive'):
                with st.status("Naive", expanded=True):
                    var_wmape, texto_status_modelo = modelo_naive(df)
                    st.write(f'**:orange[{texto_status_modelo}]** **wmape:** :red[{var_wmape}]')
                
                st.markdown("<hr>", unsafe_allow_html=True)
                
                st.markdown("""
                ```Vale notar que o modelo teve suas validações efetuadas com base na data de 18/05/2024, portanto a performance auferida pela biblioteca começa a ser considerada a partir dos dias no futuro, mais especificamente em 19/05/2024 até 01/07/2024 que é a última data a ser avaliada no dataset.``` """)
            
            st.markdown(""" 
            ⚠️ **:orange[Por que não é bom para este caso]:**
            - **Alta Volatilidade:** O preço do petróleo Brent é altamente volátil, com frequentes flutuações significativas. O Modelo Naive não consegue capturar essas variações, resultando em previsões ineficazes.
            - **WMAPE Elevado:** O gráfico indica um **WMAPE de :red[101.05%]**, o que significa que o erro das previsões é aproximadamente igual à magnitude dos valores reais. Isso evidencia que o modelo não está fornecendo previsões precisas e está falhando em acompanhar as mudanças nos preços.

            📝 **:orange[Conclusão]:**
            O Modelo Naive não é adequado para prever o preço do petróleo Brent devido à sua incapacidade de lidar com a volatilidade e mudanças dinâmicas dos preços. A métrica WMAPE alta reforça a necessidade de modelos mais avançados que possam capturar padrões e tendências nos dados históricos.
            """)


        with tab2:
            st.markdown(""" 
            ### Modelo AutoARIMA e Métrica WMAPE

            🔍 **:orange[Modelo AutoARIMA]:**
            O modelo AutoARIMA (AutoRegressive Integrated Moving Average) é uma abordagem estatística que combina auto-regressão, diferenciação e média móvel para prever séries temporais. O AutoARIMA ajusta automaticamente os parâmetros \( p \), \( d \) e \( q \) do modelo ARIMA para minimizar o erro de previsão. Ele é útil para dados com padrões sazonais e tendências complexas.

            🔢 **:orange[Métrica WMAPE] (Weighted Mean Absolute Percentage Error):**
            A métrica WMAPE é usada para avaliar a precisão das previsões. Ela calcula o erro absoluto médio ponderado pela magnitude dos valores reais, expressando-o como uma porcentagem. A fórmula é:
            """)
            st.latex(r"WMAPE = \frac{\sum | \text{Valor Real} - \text{Valor Previsto} |}{\sum \text{Valor Real}} \times 100 \%")
            
            if st.button('Executar Modelo AutoARIMA', key='AutoARIMA'):
                with st.status("AutoARIMA", expanded=True):
                    var_wmape, texto_status_modelo =modelo_auto_arima(df)
                    st.write(f'**:orange[{texto_status_modelo}]** **wmape:** :red[{var_wmape}]')

                st.markdown("<hr>", unsafe_allow_html=True)

                st.markdown("""
                ```Vale notar que o modelo teve suas validações efetuadas com base na data de 18/05/2024, portanto a performance auferida pela biblioteca começa a ser considerada a partir dos dias no futuro, mais especificamente em 19/05/2024 até 01/07/2024 que é a última data a ser avaliada no dataset.```   
                """)
            
            st.markdown(""" 
            ⚠️ **:orange[Por que não é bom para este caso]:**
            - **Complexidade dos Dados:** Apesar do AutoARIMA ser mais sofisticado que o modelo Naive, ele ainda não está conseguindo capturar a alta volatilidade e os picos súbitos nos preços do petróleo Brent.
            - **WMAPE Elevado:** O gráfico mostra um **WMAPE de :red[113.60%]**, indicando que o erro das previsões é maior que a magnitude dos valores reais. Isso sugere que o modelo está tendo dificuldades significativas para prever os preços corretamente.

            📝 **:orange[Conclusão]:**
            Embora o modelo AutoARIMA seja mais avançado que o Naive, ele não está conseguindo prever adequadamente os preços do petróleo Brent, conforme evidenciado pelo alto valor de WMAPE. Isso reforça a necessidade de explorar modelos ainda mais sofisticados ou híbridos que possam capturar melhor as dinâmicas complexas e a volatilidade dos preços do petróleo.
            """)


        with tab3:
            st.markdown(""" 
            ### Modelo Prophet e Métrica WMAPE

            🔍 **:orange[Modelo Prophet]:**
            O Prophet é um modelo de previsão desenvolvido pelo Facebook, projetado para lidar com séries temporais que possuem sazonalidades múltiplas e efeitos de feriados. Ele é robusto para lidar com dados faltantes e mudanças nos dados históricos, o que o torna ideal para séries temporais com comportamentos complexos, como o preço do petróleo Brent.

            🔢 **:orange[Métrica WMAPE] (Weighted Mean Absolute Percentage Error):**
            A métrica WMAPE é usada para avaliar a precisão das previsões. Ela calcula o erro absoluto médio ponderado pela magnitude dos valores reais, expressando-o como uma porcentagem. A fórmula é:
            """)

            st.latex(r"WMAPE = \frac{\sum | \text{Valor Real} - \text{Valor Previsto} |}{\sum \text{Valor Real}} \times 100 \%")

            if st.button('Executar Modelo Meta Prophet', key='Meta Prophet'):
                with st.status("**Modelo Meta Prophet**", expanded=True):
                    var_wmape, texto_status_modelo = modelo_prophet(df)
                    st.write(f'**:blue[{texto_status_modelo}]** **wmape:** :green[{var_wmape}]')
                
                st.markdown("<hr>", unsafe_allow_html=True)
                
                st.markdown("""
                ```Vale notar que o modelo teve suas validações efetuadas com base na data de 18/05/2024, portanto a performance auferida pela biblioteca começa a ser considerada a partir dos dias no futuro, mais especificamente em 19/05/2024 até 01/07/2024 que é a última data a ser avaliada no dataset.```   
                """)

            st.markdown(""" 
            📈 **:orange[Desempenho do Prophet]:**
            - **:orange[Baixo WMAPE]:** O gráfico mostra um **WMAPE de :green[5.70%]**, indicando que o erro das previsões é muito pequeno em relação à magnitude dos valores reais. Isso demonstra que o modelo Prophet está capturando muito bem as dinâmicas do preço do petróleo Brent.

            📝 **:orange[Comparação com Outros Modelos]:**
            1. **:blue[Modelo Naive]:**
                - **WMAPE:** **:red[101.05%]**
                - **Desempenho:** Muito fraco, incapaz de capturar a volatilidade dos preços.
                
            2. **:blue[Modelo AutoARIMA]:**
                - **WMAPE:** **:red[113.60%]**
                - **Desempenho:** Inferior ao Naive, com dificuldade significativa em prever os preços corretamente.

            3. **:blue[Modelo Prophet]:**
                - **WMAPE:** **:green[5.70%]**
                - **Desempenho:** Excelente, com previsões precisas e capacidade de capturar padrões sazonais e tendências.

            💡 **:orange[Conclusão]:**
            O modelo Prophet é claramente superior aos modelos Naive e AutoARIMA na previsão do preço do petróleo Brent. Sua capacidade de lidar com dados complexos e padrões sazonais, juntamente com um WMAPE muito baixo, faz dele a escolha ideal para previsões precisas nesta aplicação. Este modelo consegue fornecer previsões confiáveis que podem ser usadas para tomadas de decisão estratégicas no mercado de energia.
            """)

            st.markdown("""
                    ### Previsão e Análise dos Dados Previstos pelo Modelo Prophet """)
            

            with st.status("**:orange[Meta Prophet Previsão]**", expanded=True):

                DATA_INICIAL = date(2024, 4, 2)

                with st.container():
                    col, _ = st.columns([2, 6])

                    with col:
                        min_date = DATA_INICIAL
                        max_date = DATA_INICIAL + timedelta(days=90)
                        end_date = st.date_input(
                            "Data máxima de previsão",
                            key="dt_input_prophet",
                            min_value=min_date,
                            max_value=max_date,
                            value=max_date,
                        )

                
                df_futuro, media_valores, mediana_valores, desvio_padrao_valores = modelo_prophet_previsao(df, end_date)

                st.markdown("""**O modelo teve suas validações efetuadas na data base do mês 04/2024, mais especificamente em 02/04/2024 até 01/07/2024 que é a última data a ser avaliada no dataset.**""")

                st.markdown("""
                #### Tabela de Tendência e Valor Previsto
                A tabela exibe as datas, a tendência, o valor previsto e a diferença percentual entre a previsão e o valor real para os últimos dias de junho e início de julho de 2024.""")

                min_date = pd.to_datetime(min_date)
                max_date = pd.to_datetime(max_date)

                df_futuro = df_futuro[(df_futuro['Data'] >= min_date) & (df_futuro['Data'] <= max_date)]
                
                df_futuro['Data'] = df_futuro['Data'].dt.strftime('%d/%m/%Y')

                st.dataframe(df_futuro, use_container_width=True, hide_index=True)

                st.markdown(f"""
                        #### Análise Comparativa

                        1. **:orange[Média das Previsões]:** A média das previsões (**:orange[{media_valores:.2f}]**) está abaixo da mediana (**:orange[{mediana_valores:.2f}]**), indicando uma distribuição assimétrica onde alguns valores muito baixos puxam a média para baixo.
                        2. **:orange[Mediana das Previsões]:** A mediana é uma medida robusta de tendência central que não é afetada por valores extremos, dando uma ideia clara do "valor típico" das previsões.
                        3. **:orange[Desvio Padrão]:** Um desvio padrão de (**:orange[{desvio_padrao_valores:.2f}]**) mostra que as previsões têm uma variabilidade significativa, refletindo a volatilidade dos preços do petróleo.

                        ### Conclusão
                        O modelo Prophet apresenta previsões precisas, como demonstrado pela baixa diferença percentual na tabela. A análise estatística confirma a robustez do modelo na captura das tendências dos preços do petróleo Brent. O uso da média móvel no gráfico ajuda a visualizar tendências subjacentes, tornando a previsão mais compreensível e útil para tomadas de decisão estratégicas.  
                            """)
                
                
            st.markdown("<hr>", unsafe_allow_html=True)

            max_valor_previsto = df_futuro['Valor Previsto'].max()
            max_valor_data = df_futuro[df_futuro['Valor Previsto'] == max_valor_previsto]['Data'].values[0]
   
            st.markdown(f""" 
            ### Insights para Investidores sobre os Preços do Petróleo Brent

            1. **📈 :orange[Estabilidade de Curto Prazo nas Previsões]:**
                - As previsões do modelo Prophet para o final de junho e início de julho de 2024 mostram uma variação mínima, com preços previstos ao redor de **:blue[{media_valores:.2f}] USD**. A diferença percentual máxima observada fica em torno de **:blue[5%]**, sugerindo uma fase de relativa estabilidade de curto prazo. Isso pode ser um sinal positivo para investidores que buscam minimizar riscos imediatos em suas posições de mercado.

            2. **🔄 :orange[Alta Variabilidade Histórica]:**
                - Com um desvio padrão de **:blue[{desvio_padrao_valores:.2f}]**, os dados históricos indicam alta volatilidade nos preços do petróleo Brent. Investidores devem estar cientes de que, embora as previsões de curto prazo sejam estáveis, a história recente mostra que o mercado pode ser altamente imprevisível. Estratégias de hedge podem ser necessárias para mitigar possíveis oscilações de preço.

            3. **📊 :orange[Tendência de Longo Prazo Positiva]:**
                - A análise das tendências e das médias móveis de 7 dias sugere que, apesar das flutuações de curto prazo, o mercado tem se recuperado de quedas anteriores, mantendo uma tendência ascendente. Investidores de longo prazo podem considerar esta resiliência histórica como um indicativo de potencial crescimento futuro, aproveitando possíveis recuperações pós-crise.

            4. **🔍 :orange[Foco em Datas Específicas]:**
                - A tabela detalhada de previsões fornece uma visão granular das expectativas de preços. Notando a ligeira queda prevista para **{max_valor_data}** (com **:blue[{max_valor_previsto}] USD**) seguida de uma recuperação, investidores podem planejar suas estratégias de compra e venda aproveitando pequenas janelas de oportunidade para maximizar ganhos ou minimizar perdas em torno dessas datas.
            """)
            

    # cor_sidebar = '#304463' # Atual
    # cor_sidebar = '#005C78'

    st.markdown("""
    <style>
        [data-testid=stSidebar] {background-color: #304463;}
    </style> """, unsafe_allow_html=True)

    with st.sidebar:
        
        st.divider()

        st.subheader("Alunos:")
        st.write("**Leandro Braga Alves** <br> RM :orange[353057] | 3DTAT", unsafe_allow_html=True)
        st.write("**Rodrigo Mitsuo Yoshida** <br> RM :orange[35274] | 3DTAT", unsafe_allow_html=True)
        st.write("**Roberto Yukio Ihara** <br> RM :orange[35274] | 3DTAT", unsafe_allow_html=True)

        st.divider()




    
