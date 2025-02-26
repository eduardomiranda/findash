import gdown
import pandas as pd
import streamlit as st

from src.database.mongo_connection import consulta_varios_documentos
from src.data.data_prep import data_prep


def download_csv_from_google_driveas_dataframe(file_id):
    """
    Downloads a CSV file from Google Drive.

    Args:
        file_id (str): The Google Drive file ID (found in the file's shareable link).
        output_file (str): The name of the output file to save the CSV.

    Returns:
        pd.DataFrame: The downloaded CSV file as a pandas DataFrame.
    """

    # Download em Relatórios > Lançamentos de caixa

    output_file = "0c04cf8f-3094-4783-b0fd-f7dd96412290.csv"

    # Construct the download URL
    url = f"https://drive.google.com/uc?id={file_id}"
    
    # Download the file
    gdown.download(url, output_file, quiet=False)
    
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(output_file)
    
    return df




def get_data(file_id):

	df = download_csv_from_google_driveas_dataframe(file_id)
	
	mongodb_uri     = st.secrets['mongodb'].get("mongodb_uri", '')
	db_name         = st.secrets['mongodb'].get("mongodb_db", '')
	collection_name = st.secrets['mongodb'].get("mongodb_collection_data_prep", '')
	query = {}

	condicoes = consulta_varios_documentos( mongodb_uri, db_name, collection_name, query )
	data_prep(df, condicoes)

	return df