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
from src.utils.misc import formar_valor_monetario


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

streamit_login()

if st.session_state.logged_in:

    if 'dados_bancarios' not in st.session_state:

        file_id = st.secrets['dados']['dados_bancarios_file_id']
        dados_banc = dados_bancarios(file_id)
        st.session_state.dados_bancarios = dados_banc

    dados_bancarios = st.session_state.dados_bancarios

    col11, col12 = st.columns(2)
    inicio = col11.date_input("Início", datetime.date(2024, 1, 1))
    fim    = col12.date_input("Fim", datetime.date(2024, 12, 31))

    st.divider()


    col11, col12 = st.columns(2)
    col21, col22 = st.columns(2)

    with col11:
        receitas_totais = dados_bancarios.receitas_totais_no_periodo(inicio, fim)
        st.metric("Receitas totais no período", formar_valor_monetario(receitas_totais), "" , border = True)

    with col12:
        receitas_totais_por_clientes = dados_bancarios.receitas_totais_por_clientes_no_periodo(inicio, fim)
        st.metric("Receitas totais por clientes", formar_valor_monetario(receitas_totais_por_clientes), "" , border = True)

    with col21:
        receitas_financeiras = dados_bancarios.receitas_financeiras_no_periodo(inicio, fim)
        st.metric("Receitas financeiras (Exemplo: Juros semestrais dos títulos)", formar_valor_monetario(receitas_financeiras), "" , border = True)

    with col22:
        outras_receitas = dados_bancarios.outras_receitas_no_periodo(inicio, fim)
        st.metric("Outras receitas (Exemplo: Comissão de vendas)", formar_valor_monetario(outras_receitas), "" , border = True)


    st.divider()

    df_categoria_result = dados_bancarios.get_receitas_por_contato(inicio, fim)

    ylabel = df_groupby_column_name = df_categoria_result.columns.values[0]
    xlabel = df_column_values_name = df_categoria_result.columns.values[1]
    title  = 'Receitas totais por clientes'

    chart = barh_chart(df_categoria_result, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title)
    st.pyplot(chart)

    if st.button("Show me the data!", type="primary", key="04067110-0e6f-4506-8bb3-be45ac465ec4" ):
        st.dataframe(dados_bancarios. filtrar_receita_por_periodo(inicio, fim))
