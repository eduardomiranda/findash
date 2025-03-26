import sys
  
# append the path of the parent directory
sys.path.append(".")

import datetime
import locale
import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

from src.data.dados_saldos import dados_saldos
from src.utils.myplot import barh_chart, pie_chart
from src.utils.login import streamit_login
from src.utils.misc import formar_valor_monetario, converter_data_para_formato_brasileiro


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

streamit_login()

if st.session_state.logged_in:

    if 'dados_saldos' not in st.session_state:
        file_id = st.secrets['dados']['saldos_bancarios_file_id']
        sheet_name = st.secrets['dados']['saldos_bancarios_sheet_name']
        dados_sald = dados_saldos(file_id, sheet_name)
        st.session_state.dados_saldos = dados_sald

    dados_saldos = st.session_state.dados_saldos

    st.markdown(f'⚠️ Os valores apresentados foram obtidos no dia: **{converter_data_para_formato_brasileiro(str(dados_saldos.ultima_data))}**')

    col11, col12 = st.columns(2)
    col21, col22 = st.columns(2)
    col31, col32 = st.columns(2)
    st.divider()
    col41, col42 = st.columns(2)


    with col11:
        st.metric("International Finance Bank (USD)", '${:,.2f}'.format(dados_saldos.ultimo_saldo_ifb), f"{round(dados_saldos.delta_saldo_ifb,2)} %" , border = True)

    with col12:
        st.metric(f"International Finance Bank (PTAX = {formar_valor_monetario(dados_saldos.ultimo_ptax)} )", formar_valor_monetario(dados_saldos.ultimo_saldo_ifb_em_reais), f"{round(dados_saldos.delta_saldo_ifb_em_reais,2)} %" , border = True)


    with col21:
        st.metric("XP Investimentos (na curva)", formar_valor_monetario(dados_saldos.ultimo_saldo_xp_na_curva), f"{round(dados_saldos.delta_saldo_xp_na_curva,2)} %"  , border = True)

    with col22:
        st.metric("XP Investimentos (a mercado)", formar_valor_monetario(dados_saldos.ultimo_saldo_xp_a_mercado), f"{round(dados_saldos.delta_saldo_xp_a_mercado,2)} %" , border = True)


    with col31:
        st.metric("BTG Pactual", formar_valor_monetario(dados_saldos.ultimo_saldo_btg), f"{round(dados_saldos.delta_saldo_btg,2)} %"  , border = True)
    with col32:
        st.metric("Itaú", formar_valor_monetario(dados_saldos.ultimo_saldo_itau), f"{round(dados_saldos.delta_saldo_itau,2)} %" , border = True)


    with col41:
        st.metric("Saldo total (na curva): ", formar_valor_monetario(dados_saldos.ultimo_total_na_curva), f"{round(dados_saldos.delta_total_na_curva,2)} %" , border = True)
    with col42:
        st.metric("Saldo total (a mercado): ", formar_valor_monetario(dados_saldos.ultimo_total_a_mercado), f"{round(dados_saldos.delta_total_a_mercado,2)} %" , border = True)
