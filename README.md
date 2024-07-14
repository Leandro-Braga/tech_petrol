# Previsão dos Preços do Petróleo Brent

Bem-vindo ao repositório do projeto de previsão dos preços do petróleo Brent, desenvolvido para o 4º Tech Challenge da FIAP. Este projeto utiliza modelos estatísticos e de machine learning para prever os preços futuros do petróleo Brent, analisando dados históricos e tendências de mercado.

## Descrição do Projeto

O objetivo deste projeto é demonstrar a eficácia de diferentes modelos de previsão para os preços do petróleo Brent. Foram testados três modelos principais:

1. **Modelo Naive**
2. **Modelo AutoARIMA**
3. **Modelo Prophet**

### Insights e Resultados

1. **Modelo Naive**:
   - **Desempenho:** Fraco, com um WMAPE de 101.05%.
   - **Conclusão:** Incapaz de capturar a volatilidade dos preços.

2. **Modelo AutoARIMA**:
   - **Desempenho:** Inferior ao Naive, com um WMAPE de 113.60%.
   - **Conclusão:** Dificuldades significativas em prever os preços corretamente.

3. **Modelo Prophet**:
   - **Desempenho:** Excelente, com um WMAPE de 5.70%.
   - **Conclusão:** Captura bem as dinâmicas do mercado e fornece previsões precisas.

### Gráficos e Tabelas

#### Gráfico de Previsões do Modelo Prophet

![Gráfico de Previsões](path_to_image)

#### Tabela de Tendência e Valor Previsto

| Data       | Tendência | Valor Previsto | Diferença Percentual (%) |
|------------|-----------|----------------|--------------------------|
| 30/06/2024 | 82.62     | 86.12          | 4.06                     |
| 29/06/2024 | 82.63     | 86.20          | 4.14                     |
| 28/06/2024 | 82.63     | 86.29          | 4.24                     |
| 27/06/2024 | 82.64     | 86.03          | 3.95                     |
| 26/06/2024 | 82.64     | 86.08          | 4.00                     |
| 25/06/2024 | 82.64     | 86.37          | 4.31                     |
| 24/06/2024 | 82.64     | 86.55          | 4.51                     |
| 23/06/2024 | 82.65     | 86.60          | 4.57                     |
| 22/06/2024 | 82.62     | 86.65          | 4.62                     |
| 01/07/2024 | 82.62     | 86.06          | 3.99                     |

## Acessos e Repositórios

- **Link Streamlit:** (Irei adicionar em breve)
- **Repositório do app Streamlit para o 4º Tech Challenge da FIAP:** [GIT Streamlit](https://github.com/Leandro-Braga/tech_petrol.git)
- **Acesse o repositório para obter o código Python do app Streamlit:** [https://github.com/Leandro-Braga/tech_petrol.git](https://github.com/Leandro-Braga/tech_petrol.git)
- **Acesse o repositório para obter o notebook do projeto:** [GIT Notebook](https://github.com/Leandro-Braga/tech_petrol/tree/96adf336b7f273316fb154623b1a0c4a06550222/notebook)

### Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/Leandro-Braga/tech_petrol.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd tech_petrol
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o aplicativo Streamlit:
   ```bash
   streamlit run app.py
   ```

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**Autor:** Leandro Braga

---

Este projeto foi desenvolvido como parte do 4º Tech Challenge da FIAP. Agradecemos a todos os envolvidos e esperamos que este trabalho contribua para a compreensão e previsão dos preços do petróleo Brent.
