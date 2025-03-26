import pandas as pd
import streamlit as st

from src.data.data_loader import download_google_spreadsheet

class dados_ifb():

    def __init__(self, file_id, sheet_name):

        self._df = download_google_spreadsheet(file_id, sheet_name)
        self.delecao_colunas_desnecessarias()
        self.correcao_tipos_dados()
        self.condicoes = self.get_conditions_dados_bancarios()
        self.rename()



    @property
    def df(self):
        return self._df


    def get_conditions_dados_bancarios(self):

        file_id = st.secrets['dados']['ifb_data_prep_file_id']
        sheet_name = 'column_rename'

        return download_google_spreadsheet(file_id, sheet_name)



    def delecao_colunas_desnecessarias(self):

        # df.drop('Status', axis=1, inplace=True)
        self._df.drop('Debits', axis=1, inplace=True)
        self._df.drop('Credits', axis=1, inplace=True)


    def  correcao_tipos_dados(self):
        self._df['Valor efetivo'] = self._df['Valor efetivo'].fillna('0')

        # Remove "R$ " and replace '.' with '' and ',' with '.'
        self._df['Valor efetivo'] = self._df['Valor efetivo'].str.replace('$', '')
        self._df['Valor efetivo'] = self._df['Valor efetivo'].str.replace(',', '')

        # Convert the resulting string to a float
        self._df['Valor efetivo'] = self._df['Valor efetivo'].astype(float)

        # Convert the string column to datetime with the correct format
        self._df['Date'] = pd.to_datetime(self._df['Date']).dt.date
        self._df['Date'] = pd.to_datetime(self._df['Date'], dayfirst=True, format='%m/%d/%Y')


    def rename(self):

        for index, row in self.condicoes.iterrows():
            column_name = row['column_name']

            if column_name:
                old_value = row['old_value']
                new_value = row['new_value']

                self._df[column_name] = self._df[column_name].replace(old_value, new_value)



    def agrupa_por_descricao(self): 
        # Agrupar os dados por ano, produto e tipo
        return self._df.groupby(['Description'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=True)
