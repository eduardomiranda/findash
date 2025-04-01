
import streamlit as st

from src.data.dados_faturamentos import dados_faturamentos
from src.data.dados_bancarios import dados_bancarios
from src.data.dados_saldos import dados_saldos
from src.data.dados_ifb import dados_ifb


def get_dados_ifb():

	if 'dados_ifb' not in st.session_state:
	    file_id = st.secrets['dados']['ifb_file_id']
	    sheet_name = st.secrets['dados']['ifb_sheet_name']

	    dados = dados_ifb(file_id, sheet_name)
	    st.session_state.dados_ifb = dados

	return st.session_state.dados_ifb




def get_dados_bancarios():

	if 'dados_bancarios' not in st.session_state:

		file_id = st.secrets['dados']['dados_bancarios_file_id']
		dados = dados_bancarios(file_id)
		st.session_state.dados_bancarios = dados

	return st.session_state.dados_bancarios



def get_dados_faturamentos(): 

    if 'dados_faturamentos' not in st.session_state:

        file_id    = st.secrets['dados']['notas_fiscais_emitidas_file_id']
        sheet_name = st.secrets['dados']['notas_fiscais_emitidas_sheet_name']
        dados_fat = dados_faturamentos(file_id, sheet_name) 

        st.session_state.dados_faturamentos = dados_fat

    return st.session_state.dados_faturamentos



def get_dados_saldos():

    if 'dados_saldos' not in st.session_state:
        file_id = st.secrets['dados']['saldos_bancarios_file_id']
        sheet_name = st.secrets['dados']['saldos_bancarios_sheet_name']
        dados_sald = dados_saldos(file_id, sheet_name)
        st.session_state.dados_saldos = dados_sald

    return st.session_state.dados_saldos
