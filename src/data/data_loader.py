import gdown
import pandas as pd
import streamlit as st

from src.database.mongo_connection import consulta_varios_documentos


def download_csv_from_google_drive(file_id):
    """
    Downloads a CSV file from Google Drive.

    Args:
        file_id (str): The Google Drive file ID (found in the file's shareable link).

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




def download_google_spreadsheet(file_id, sheet_name):

    """
    Downloads a Google Spreadsheet from Google Drive.

    Args:
        file_id (str): The Google Drive file ID (found in the file's shareable link).

    Returns:
        pd.DataFrame: The downloaded Google Spreadsheet as a pandas DataFrame.
    """

    url = f"https://docs.google.com/spreadsheets/d/{file_id}/gviz/tq?tqx=out:csv&sheet={{{sheet_name}}}"
    return pd.read_csv(url)

