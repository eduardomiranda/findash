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

    # Campo para seleção do ano
    ano_selecionado = st.selectbox("Selecione o ano", range(2025, 2019, -1))


    # Campos para entrada de valores percentuais
    col11, col12 = st.columns(2)
    with col11:
        margem_servico = st.number_input("Margem sobre 🧠 Serviço (%)", min_value=0.0, max_value=100.0, value=35.0, step=5.0)
    with col12:
        margem_produto = st.number_input("Margem sobre 💻 Produto (%)", min_value=0.0, max_value=100.0, value=20.0, step=5.0)

    # Campos para entrada de valores numéricos que aumentam de 0.1 em 0.1
    col21, col22 = st.columns(2)
    with col21:
        multiplo_servico = st.number_input("Múltiplo para o valuation de 🧠 Serviço", min_value=0.0, value=8.0, step=0.5)
    with col22:
        multiplo_produto = st.number_input("Múltiplo para o valuation de 💻 Produto", min_value=0.0, value=2.0, step=0.5)

    st.divider()

    total_servico_ano_selecionado = df_dados_faturamentos.loc[(df_dados_faturamentos.Ano == ano_selecionado) & (df_dados_faturamentos["Serviço ou \nLicença?"] == "Serviço")]["Valor Serviços(R$)"].sum()
    total_produto_ano_selecionado = df_dados_faturamentos.loc[(df_dados_faturamentos.Ano == ano_selecionado) & (df_dados_faturamentos["Serviço ou \nLicença?"] == "Licença")]["Valor Serviços(R$)"].sum()

    col31, col32 = st.columns(2)
    with col31:
        st.metric(f"Total de 🧠 Serviços em {ano_selecionado}", f'R$ {total_servico_ano_selecionado:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), "" )

    with col32:
        st.metric(f"Total de 💻 Produto em {ano_selecionado}", f'R$ {total_produto_ano_selecionado:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), "" )

    st.divider()

    valuation_servico = total_servico_ano_selecionado * margem_servico / 100 * multiplo_servico
    valuation_produto = total_produto_ano_selecionado * margem_produto / 100 * multiplo_produto
    valor_total = valuation_servico + valuation_produto

    st.title(f"🤑 Valuation da companhia em {ano_selecionado}")
    st.metric("", f'R$ {valor_total:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."), "" )

    st.divider()

    st.subheader("Racional")
    st.text("Valuation do 🧠 Serviço:")
    st.subheader(f"R\$ {total_servico_ano_selecionado:,.2f}  x  {margem_servico:,.1f}%  x  {multiplo_servico} = R\$ {valuation_servico:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.text("Valuation do 💻 Produto:")
    st.subheader(f"R\$ {total_produto_ano_selecionado:,.2f}  x  {margem_produto:,.1f}%  x  {multiplo_produto} = R\$ {valuation_produto:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
