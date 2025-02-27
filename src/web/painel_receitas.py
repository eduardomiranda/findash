import sys
  
# append the path of the parent directory
sys.path.append(".")


import datetime
import locale
import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

from src.data.dados_bancarios import dados_bancarios
from src.utils.myplot import barh_chart, pie_chart
from src.utils.login import streamit_login


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

streamit_login()

if st.session_state.logged_in:

    df_dados_bancarios = None
    if 'df_dados_bancarios' not in st.session_state:
        dados_banc = dados_bancarios(st.secrets['dados']['file_id_dados_bancarios'])
        st.session_state.df_dados_bancarios = dados_banc.df

    df_dados_bancarios = st.session_state.df_dados_bancarios



    # Título do aplicativo
    # st.title('💸 Análise de Despesas')

    col11, col12 = st.columns(2)
    inicio = col11.date_input("Início", datetime.date(2024, 1, 1))
    fim    = col12.date_input("Fim", datetime.date(2024, 12, 31))

    st.divider()

    st.title('Dados das contas bancárias')

    df_dados_bancarios["Data efetiva"] = pd.to_datetime(df_dados_bancarios["Data efetiva"]).dt.date
    df_dados_bancarios =  df_dados_bancarios.loc[(df_dados_bancarios['Data efetiva'] >= inicio) & (df_dados_bancarios['Data efetiva'] <= fim)]


    df_dados_bancarios = df_dados_bancarios[ (df_dados_bancarios['Tipo'] == 'Receita') & (~df_dados_bancarios['Categoria'].isin(['Remunera+', 'Resgate', 'Devolução'])) ]

    receitas_totais = locale.currency(df_dados_bancarios['Valor efetivo'].sum(), grouping=True)
    st.metric("Receitas Totais", receitas_totais, "" )


    df_categoria_result = df_dados_bancarios[df_dados_bancarios['Categoria'] == 'Vendas'].groupby(['Contato'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=True)

    df_groupby_column_name = 'Contato'
    df_column_values_name = 'Valor efetivo'
    xlabel = 'Valor Efetivo (R$)'
    ylabel = 'Contato'
    title  = 'Receitas totais'

    chart = barh_chart(df_categoria_result, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title)
    st.pyplot(chart)

    if st.button("Show me the data!", type="primary", key="04067110-0e6f-4506-8bb3-be45ac465ec4" ):
        st.dataframe(df_dados_bancarios)
