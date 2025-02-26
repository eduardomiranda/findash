import streamlit as st

from src.database.mongo_connection import consulta_varios_documentos
from src.data.data_loader import download_csv_from_google_drive, download_google_spreadsheet
from src.data.data_prep import data_prep


def get_dados_bancarios(file_id):

	df = download_csv_from_google_drive(file_id)
	
	mongodb_uri     = st.secrets['mongodb'].get("mongodb_uri", '')
	db_name         = st.secrets['mongodb'].get("mongodb_db", '')
	collection_name = st.secrets['mongodb'].get("mongodb_collection_data_prep", '')
	query = {}

	condicoes = consulta_varios_documentos( mongodb_uri, db_name, collection_name, query )
	data_prep(df, condicoes)

	return df




def get_dados_notas_fiscais_emitidas(file_id, sheet_name):

	df = download_google_spreadsheet(file_id, sheet_name)

	return df