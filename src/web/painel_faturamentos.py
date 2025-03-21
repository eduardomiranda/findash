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
from src.utils.misc import formar_valor_monetario


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

streamit_login()

if st.session_state.logged_in:

    st.text('⚠️ Aqui estão sendo considerados o valor bruto das notas fiscais emitidas e não o valor líquido recebido!')

    if 'dados_faturamentos' not in st.session_state:

        file_id    = st.secrets['dados']['file_id_notas_fiscais_emitidas']
        sheet_name = st.secrets['dados']['sheet_name_notas_fiscais_emitidas']
        dados_fat = dados_faturamentos(file_id, sheet_name) 

        st.session_state.dados_faturamentos = dados_fat
    
    
    a_receber = st.session_state.dados_faturamentos.get_total_pendente_recebimento()

    st.metric("Valores a receber", formar_valor_monetario(a_receber), "" )

    if st.button("Show me the data!", type="primary", key = "4f71f641-6fba-4a11-8a4e-232bee9defc2"):
        st.dataframe(st.session_state.dados_faturamentos.get_notas_pendente_recebimento())


    df_agg = st.session_state.dados_faturamentos.get_receita_bruta_por_produto_e_ano()
    fig = receita_bruta_por_produto_e_ano(df_agg)
    st.pyplot(fig)

    df_agg = st.session_state.dados_faturamentos.get_receita_por_ano_produto_tipo()
    fig = receita_por_ano_produto_tipo(df_agg)
    st.pyplot(fig)


    if st.button("Show me the data!", type="primary", key = "cea9ec91-d4c7-4055-8725-189e276c4fd4"):
        st.dataframe(st.session_state.dados_faturamentos.df)