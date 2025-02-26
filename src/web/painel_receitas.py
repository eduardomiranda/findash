import sys
  
# append the path of the parent directory
sys.path.append(".")


import datetime
import locale
import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

from src.data.data_loader import get_data
from src.utils.myplot import barh_chart, pie_chart
from src.utils.login import streamit_login


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

streamit_login()

if st.session_state.logged_in:

    df = None
    if 'df' not in st.session_state:
        st.session_state.df = get_data(st.secrets['dados']['file_id'])

    df = st.session_state.df



    # Título do aplicativo
    # st.title('💸 Análise de Despesas')

    col11, col12 = st.columns(2)
    inicio = col11.date_input("Início", datetime.date(2024, 1, 1))
    fim    = col12.date_input("Fim", datetime.date(2024, 12, 31))

    st.divider()


    df["Data efetiva"] = pd.to_datetime(df["Data efetiva"]).dt.date
    df =  df.loc[(df['Data efetiva'] >= inicio) & (df['Data efetiva'] <= fim)]


    df = df[ (df['Tipo'] == 'Receita') & (~df['Categoria'].isin(['Remunera+', 'Resgate', 'Devolução'])) ]

    receitas_totais = locale.currency(df['Valor efetivo'].sum(), grouping=True)
    st.metric("Receitas Totais", receitas_totais, "" )


    df_categoria_dresult = df[df['Categoria'] == 'Vendas'].groupby(['Contato'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=True)

    df_groupby_column_name = 'Contato'
    df_column_values_name = 'Valor efetivo'
    xlabel = 'Valor Efetivo (R$)'
    ylabel = 'Contato'
    title  = 'Receitas totais'

    chart = barh_chart(df_categoria_dresult, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title)
    st.pyplot(chart)


    st.dataframe(df)

    # # Combobox para seleção de categoria
    # categorias = df['Categoria'].unique()
    # categoria_selecionada = st.selectbox('Selecione a Categoria:', categorias)

    # # Filtra as subcategorias com base na categoria selecionada
    # subcategorias = df[df['Categoria'] == categoria_selecionada]['Subcategoria'].unique()


    # df_filtrado = df[df['Categoria'] == categoria_selecionada]

    # # Cria o gráfico Matplotlib
    # if not df_filtrado.empty:

    #     df_dresult = None
    #     df_groupby_column_name = None
    #     ylabel = None

    #     if 1 < len(subcategorias):
    #         df_dresult = df_filtrado.groupby(['Categoria','Subcategoria'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)
    #         df_groupby_column_name = 'Subcategoria'
    #         ylabel = 'Subcategoria'
    #     else:
    #         df_dresult = df_filtrado.groupby(['Categoria','Contato'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)
    #         df_groupby_column_name = 'Contato'
    #         ylabel = 'Contato'


    #     df_column_values_name = 'Valor efetivo'
    #     xlabel = 'Valor Efetivo (R$)'
    #     title  = categoria_selecionada

    #     chart = barh_chart(df_dresult, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title)
    #     st.pyplot(chart)

    #     st.dataframe(df_filtrado.sort_values('Valor efetivo', ascending=True))

    # else:
    #     st.write("Nenhum dado encontrado para a seleção atual.")