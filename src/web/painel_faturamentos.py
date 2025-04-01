import sys
  
# append the path of the parent directory
sys.path.append(".")


import datetime
import locale
import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

from src.utils.data_loader import get_dados_faturamentos
from src.utils.myplot import receita_bruta_por_produto_e_ano, receita_por_ano_produto_tipo
from src.utils.login import streamit_login
from src.utils.misc import formar_valor_monetario


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

streamit_login()

if st.session_state.logged_in:

    with st.spinner("Obtendo dados...", show_time=True):
        dados_faturamentos = get_dados_faturamentos()

    st.text('⚠️ Aqui estão sendo considerados o valor bruto das notas fiscais emitidas e não o valor líquido recebido!')

    
    a_receber = dados_faturamentos.get_total_pendente_recebimento()

    st.metric("Valores a receber", formar_valor_monetario(a_receber), "" , border = True)

    if st.button("Show me the data!", type="primary", key = "4f71f641-6fba-4a11-8a4e-232bee9defc2"):
        st.dataframe(dados_faturamentos.get_notas_pendente_recebimento())


    df_agg = dados_faturamentos.get_receita_bruta_por_produto_e_ano()
    fig = receita_bruta_por_produto_e_ano(df_agg)
    st.pyplot(fig)

    df_agg = dados_faturamentos.get_receita_por_ano_produto_tipo()
    fig = receita_por_ano_produto_tipo(df_agg)
    st.pyplot(fig)


    if st.button("Show me the data!", type="primary", key = "cea9ec91-d4c7-4055-8725-189e276c4fd4"):
        st.dataframe(dados_faturamentos.df)