import streamlit as st 
import pandas as pd # type: ignore
import plotly.express as px # type: ignore

# Configuração da página do Streamlit e leitura do arquivo CSV
st.set_page_config(layout='wide', page_title='Supermarket Sales')
df = pd.read_csv('supermarket_sales.csv', sep=';', decimal=',')

# Convertendo a coluna 'Date' para o tipo datetime e ordenando os dados por data
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by='Date')

# Criando a coluna 'Month' que combina o ano e mês da data para facilitar a análise mensal
df['Month'] = df['Date'].apply(lambda x: str(x.year) + '-' + str(x.month))

# Cria um seletor de mês na sidebar, permitindo ao usuário escolher o mês de interesse
month: str = st.sidebar.selectbox('Mês', df['Month'].unique())
df_filtered = df[df['Month'] == month]

# Calculando o total de vendas por cidade
city_total = df_filtered.groupby('City')['Total'].sum().reset_index()

# Calculando a média de avaliações por cidade
city_mean = df_filtered.groupby('City')['Rating'].mean().reset_index()

# Criando os layouts para os gráficos
col1, col2 = st.columns(2) # Cria um layout de 2 colunas
col3, col4, col5 = st.columns(3) # Cria um layout de 3 colunas

# Criando gráficos interativos e exibindo nos layouts
# Visualização das vendas por dia
fig_date = px.bar(df_filtered, x='Date', y='Total', title='Faturamento por dia', 
                  color='City')
col1.plotly_chart(fig_date)

# Visualização do tipo de produto
fig_prod = px.bar(df_filtered, x='Date', y='Product line',
                   title='Faturamento por tipo de produto', orientation='h',
                   color='City')
col2.plotly_chart(fig_prod)

# Visualização das vendas por filial
fig_city = px.bar(city_total, x='City', y='Total', title='Faturamento por filial')
col3.plotly_chart(fig_city)

# Visualização das formas de pagamento
fig_kind = px.pie(df_filtered, values='Total', names='Payment', 
                 title='Faturamento por tipo de pagamento')
col4.plotly_chart(fig_kind)

# Visualização das avaliações por filial
fig_rating = px.bar(city_mean, x='City', y='Rating', title='Avaliação', 
                    color='City')
col5.plotly_chart(fig_rating)

