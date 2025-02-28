import pandas as pd
import streamlit as st

from src.data.data_loader import download_google_spreadsheet
from src.database.mongo_connection import consulta_varios_documentos

class dados_faturamentos():

    def __init__(self, file_id, sheet_name):

        self._df = download_google_spreadsheet(file_id, sheet_name)
        self.condicoes = None

        self.delecao_colunas_desnecessarias()
        self.correcao_tipos_dados()
        self.remocao_ultima_linha()
        self.remocao_notas_emitidas_mas_canceladas()
        self.criacao_coluna_ano()



    @property
    def df(self):
        return self._df



    def delecao_colunas_desnecessarias(self):

        # df.drop('Status', axis=1, inplace=True)
        self._df.drop('Nota', axis=1, inplace=True)
        self._df.drop('Situação', axis=1, inplace=True)
        self._df.drop('ISS devido (R$)', axis=1, inplace=True)
        self._df.drop('Imposto retido na fonte?\nSim • Não', axis=1, inplace=True)



    def  correcao_tipos_dados(self):
        self._df['Valor Serviços(R$)'] = self._df['Valor Serviços(R$)'].fillna('0')

        # Remove "R$ " and replace '.' with '' and ',' with '.'
        self._df['Valor Serviços(R$)'] = self._df['Valor Serviços(R$)'].str.replace('R\$ ', '')
        self._df['Valor Serviços(R$)'] = self._df['Valor Serviços(R$)'].str.replace('R$ ', '')
        self._df['Valor Serviços(R$)'] = self._df['Valor Serviços(R$)'].str.replace(',', '')

        # Convert the resulting string to a float
        self._df['Valor Serviços(R$)'] = self._df['Valor Serviços(R$)'].astype(float)

        self._df['Emissão'] = pd.to_datetime(self._df['Emissão'], dayfirst=True, format="%d/%m/%Y %H:%M:%S")




    def remocao_ultima_linha(self):

        # Remoção da última linha que não possui data e também não tem interferência nos cálculos
        self._df.drop(self._df.tail(1).index,inplace=True) # drop last n rows



    def remocao_notas_emitidas_mas_canceladas(self):

        # Filtrando apenas as notas fiscais pagas e pendentes de pagamento
        self._df = self._df[ self._df['Status\nRecebimento'].isin(['✔️', '🕑']) ]


    def criacao_coluna_ano(self):

        # Criando uma coluna com o ano da emissão da nota fiscal
        self._df['Ano'] = pd.DatetimeIndex(self._df['Emissão']).year



    def get_total_servico(self, ano):
        return self._df.loc[(self._df.Ano == ano) & (self._df["Serviço ou \nLicença?"] == "Serviço")]["Valor Serviços(R$)"].sum()


    def get_total_produto(self, ano):
        return self._df.loc[(self._df.Ano == ano) & (self._df["Serviço ou \nLicença?"] == "Licença")]["Valor Serviços(R$)"].sum()


    def get_receita_bruta_por_produto_e_ano(self):
        return self._df[self._df["Serviço ou \nLicença?"].isin(["Licença", "Serviço"])].groupby(["Ano", "Produto"])["Valor Serviços(R$)"].sum().unstack().fillna(0)

    
    def get_receita_por_ano_produto_tipo(self): 
        # Agrupar os dados por ano, produto e tipo
        return self._df[self._df["Serviço ou \nLicença?"].isin(["Licença", "Serviço"])].groupby(['Ano', 'Produto', 'Serviço ou \nLicença?'])['Valor Serviços(R$)'].sum().reset_index()
