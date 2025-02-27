import sys
  
# append the path of the parent directory
sys.path.append(".")


import datetime
import locale
import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

from src.data.dados_faturamentos import dados_faturamentos
from src.utils.myplot import receita_bruta_por_produto_e_ano, receita_por_ano_produto_tipo
from src.utils.login import streamit_login


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

streamit_login()

if st.session_state.logged_in:

    df_dados_faturamentos = None
    if 'df_dados_faturamentos' not in st.session_state:

        file_id    = st.secrets['dados']['file_id_notas_fiscais_emitidas']
        sheet_name = st.secrets['dados']['sheet_name_notas_fiscais_emitidas']
        dados_fat = dados_faturamentos(file_id, sheet_name) 

        st.session_state.df_dados_faturamentos = dados_fat.df
    
    df_dados_faturamentos = st.session_state.df_dados_faturamentos

    # df_agg = df_dados_faturamentos.groupby(['Ano', 'Produto','Serviço ou \nLicença?'])['Valor Serviços(R$)'].sum()

    df_agg = df_dados_faturamentos[df_dados_faturamentos["Serviço ou \nLicença?"].isin(["Licença", "Serviço"])].groupby(["Ano", "Produto"])["Valor Serviços(R$)"].sum().unstack().fillna(0)

    fig = receita_bruta_por_produto_e_ano(df_agg)
    st.pyplot(fig)

    # Agrupar os dados por ano, produto e tipo
    df_agg = df_dados_faturamentos[df_dados_faturamentos["Serviço ou \nLicença?"].isin(["Licença", "Serviço"])].groupby(['Ano', 'Produto', 'Serviço ou \nLicença?'])['Valor Serviços(R$)'].sum().reset_index()

    fig = receita_por_ano_produto_tipo(df_agg)
    st.pyplot(fig)


    if st.button("Show me the data!", type="primary", key = "cea9ec91-d4c7-4055-8725-189e276c4fd4"):
        st.dataframe(df_dados_faturamentos)


