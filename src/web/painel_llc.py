import sys
  
# append the path of the parent directory
sys.path.append(".")


import datetime
import locale
import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

from src.utils.data_loader import get_dados_ifb
from src.utils.myplot import barh_chart, pie_chart
from src.utils.login import streamit_login
from src.utils.misc import formar_valor_monetario


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

streamit_login()

if st.session_state.logged_in:

    with st.spinner("Obtendo dados...", show_time=True):
        dados_ifb = get_dados_ifb()


    df_result = dados_ifb.agrupa_por_descricao()

    ylabel = df_groupby_column_name = df_result.columns.values[0]
    xlabel = df_column_values_name = df_result.columns.values[1]
    title  = 'Century Data LLC'

    chart = barh_chart(df_result, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, simbolo_moeda = '$')
    st.pyplot(chart)

    if st.button("Show me the data!", type="primary", key="04067110-0e6f-4506-8bb3-be45ac465ec4" ):
        st.dataframe(dados_ifb.df)
