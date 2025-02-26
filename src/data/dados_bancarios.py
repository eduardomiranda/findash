import pandas as pd
import streamlit as st

from src.data.data_loader import download_csv_from_google_drive
from src.database.mongo_connection import consulta_varios_documentos

class dados_bancarios():

    def __init__(self, file_id):

        self._df = download_csv_from_google_drive(file_id)
        self.condicoes = self.get_conditions_dados_bancarios()

        self.delecao_colunas_desnecessarias()
        self.correcao_tipos_dados()
        self.remover_registros_investimentos()
        self.remover_registros_transferencias()
        self.remover_registros_cartao_credito()
        self.rename()


    @property
    def df(self):
        return self._df



    def get_conditions_dados_bancarios(self):
        
        mongodb_uri     = st.secrets['mongodb'].get("mongodb_uri", '')
        db_name         = st.secrets['mongodb'].get("mongodb_db", '')
        collection_name = st.secrets['mongodb'].get("mongodb_collection_data_prep", '')
        query = {}

        condicoes = consulta_varios_documentos( mongodb_uri, db_name, collection_name, query )
        return condicoes



    def delecao_colunas_desnecessarias(self):

        # df.drop('Status', axis=1, inplace=True)
        self._df.drop('Data prevista', axis=1, inplace=True)
        self._df.drop('Venc. Fatura', axis=1, inplace=True)
        self._df.drop('Valor previsto', axis=1, inplace=True)
        self._df.drop('Forma', axis=1, inplace=True)
        self._df.drop('ID Único', axis=1, inplace=True)
        self._df.drop('Tags', axis=1, inplace=True)
        self._df.drop('Cartão', axis=1, inplace=True)
        self._df.drop('Meta de Economia', axis=1, inplace=True)
        self._df.drop('Repetição', axis=1, inplace=True)
        self._df.drop('Razão social', axis=1, inplace=True)
        self._df.drop('N. Documento', axis=1, inplace=True)
        self._df.drop('Data competência', axis=1, inplace=True)

        self._df.drop('Status', axis=1, inplace=True)
        self._df.drop('Conta', axis=1, inplace=True)
        self._df.drop('Conta transferência', axis=1, inplace=True)
        self._df.drop('CPF/CNPJ', axis=1, inplace=True)


    def  correcao_tipos_dados(self):
        self._df['Valor efetivo'] = self._df['Valor efetivo'].fillna('0')

        # Remove "R$ " and replace '.' with '' and ',' with '.'
        self._df['Valor efetivo'] = self._df['Valor efetivo'].str.replace('R\$ ', '')
        self._df['Valor efetivo'] = self._df['Valor efetivo'].str.replace('.', '')
        self._df['Valor efetivo'] = self._df['Valor efetivo'].str.replace(',', '.')

        # Convert the resulting string to a float
        self._df['Valor efetivo'] = self._df['Valor efetivo'].astype(float)

        # Convert the string column to datetime with the correct format
        self._df['Data efetiva'] = pd.to_datetime(self._df['Data efetiva'], dayfirst=True, format='%d/%m/%Y')




    def rename(self):

        for condicao in self.condicoes:
            dataframe_column_name = condicao.get("dataframe_column_name", None)

            if dataframe_column_name:
                old_value = condicao.get("old_value", None)
                new_value = condicao.get("new_value", None)

                self._df[dataframe_column_name] = self._df[dataframe_column_name].replace(old_value, new_value)




    def remover_registros_investimentos(self):

        index_investimentos = self._df[ self._df['Categoria'] == 'Investimentos' ].index
        self._df.drop(index_investimentos, inplace=True)



    def remover_registros_transferencias(self):

        index_transferencias = self._df[ self._df['Categoria'] == 'Transferência' ].index
        self._df.drop(index_transferencias, inplace=True)



    def remover_registros_cartao_credito(self):

        index_cartao_credito = self._df[ self._df['Subcategoria'] == 'Cartão de créditos' ].index
        self._df.drop(index_cartao_credito, inplace=True)
