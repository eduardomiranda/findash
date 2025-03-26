import pandas as pd
import streamlit as st

from src.data.data_loader import download_google_spreadsheet

class dados_saldos():

    def __init__(self, file_id, sheet_name):

        self._df = download_google_spreadsheet(file_id, sheet_name)

        self.correcao_tipos_dados()
        self.calcula_valores()




    @property
    def df(self):
        return self._df


    @property
    def ultima_data(self):
        return self.__ultima_data

    @property
    def ultimo_saldo_ifb(self):
        return self.__ultimo_saldo_ifb

    @property
    def ultimo_saldo_ifb_em_reais(self):
        return self.__ultimo_saldo_ifb_em_reais

    @property
    def ultimo_ptax(self):
        return self.__ultimo_ptax

    @property
    def ultimo_saldo_btg(self):
        return self.__ultimo_saldo_btg

    @property
    def ultimo_saldo_xp_na_curva(self):
        return self.__ultimo_saldo_xp_na_curva

    @property
    def ultimo_saldo_xp_a_mercado(self):
        return self.__ultimo_saldo_xp_a_mercado

    @property
    def ultimo_saldo_itau(self):
        return self.__ultimo_saldo_itau


    @property
    def ultimo_total_na_curva(self):
        return self.__ultimo_total_na_curva

    @property
    def ultimo_total_a_mercado(self):
        return self.__ultimo_total_a_mercado


    @property
    def delta_saldo_ifb(self):
        return self.__delta_saldo_ifb

    @property
    def delta_saldo_ifb_em_reais(self):
        return self.__delta_saldo_ifb_em_reais

    @property
    def delta_saldo_btg(self):
        return self.__delta_saldo_btg


    @property
    def delta_saldo_xp_na_curva(self):
        return self.__delta_saldo_xp_na_curva

    @property
    def delta_saldo_xp_a_mercado(self):
        return self.__delta_saldo_xp_a_mercado

    @property
    def delta_saldo_itau(self):
        return self.__delta_saldo_itau

    @property
    def delta_total_na_curva(self):
        return self.__delta_total_na_curva

    @property
    def delta_total_a_mercado(self):
        return self.__delta_total_a_mercado




    def correcao_tipos_dados(self):

        columns = ['BTG Pactual', 'XP Investimentos (na curva)', 'XP Investimentos (a mercado)', 'Itaú']

        for column_name in columns:
            # Convert the resulting string to a float
            self._df[column_name] = self._df[column_name].astype(str)

            # Remove "R$ " and replace '.' with '' and ',' with '.'
            self._df[column_name] = self._df[column_name].str.replace('R\$ ', '')
            self._df[column_name] = self._df[column_name].str.replace('.', '')
            self._df[column_name] = self._df[column_name].str.replace(',', '.')

            # Convert the resulting string to a float
            self._df[column_name] = self._df[column_name].astype(float)


        # Convert the string column to datetime with the correct format
        self._df['Data efetiva'] = pd.to_datetime(self._df['Data efetiva'], dayfirst=True, format='%d/%m/%Y')
        self._df['Data efetiva'] = pd.to_datetime(self._df['Data efetiva']).dt.date




    def calcula_valores(self):
        df = self._df.sort_values(by='Data efetiva', ascending=False)

        self.__ultima_data = df['Data efetiva'].iloc[0]
        self.__ultimo_saldo_ifb = df['International Finance Bank'].iloc[0]
        self.__ultimo_ptax = df['PTAX'].iloc[0]
        self.__ultimo_saldo_btg = df['BTG Pactual'].iloc[0]
        self.__ultimo_saldo_xp_na_curva = df['XP Investimentos (na curva)'].iloc[0]
        self.__ultimo_saldo_xp_a_mercado = df['XP Investimentos (a mercado)'].iloc[0]
        self.__ultimo_saldo_itau = df['Itaú'].iloc[0]
        self.__ultimo_saldo_ifb_em_reais = self.__ultimo_saldo_ifb * self.__ultimo_ptax

        self.__penultima_data = df['Data efetiva'].iloc[1]
        self.__penultimo_saldo_ifb = df['International Finance Bank'].iloc[1]
        self.__penultimo_ptax = df['PTAX'].iloc[1]
        self.__penultimo_saldo_btg = df['BTG Pactual'].iloc[1]
        self.__penultimo_saldo_xp_na_curva = df['XP Investimentos (na curva)'].iloc[1]
        self.__penultimo_saldo_xp_a_mercado = df['XP Investimentos (a mercado)'].iloc[1]
        self.__penultimo_saldo_itau = df['Itaú'].iloc[1]
        self.__penultimo_saldo_ifb_em_reais = self.__penultimo_saldo_ifb * self.__penultimo_ptax

        self.__ultimo_total_na_curva = self.__ultimo_saldo_ifb_em_reais + self.__ultimo_saldo_btg + self.__ultimo_saldo_xp_na_curva + self.__ultimo_saldo_itau
        self.__ultimo_total_a_mercado = self.__ultimo_saldo_ifb_em_reais + self.__ultimo_saldo_btg + self.__ultimo_saldo_xp_a_mercado + self.__ultimo_saldo_itau

        self.__penultimo_total_na_curva = self.__penultimo_saldo_ifb_em_reais + self.__penultimo_saldo_btg + self.__penultimo_saldo_xp_na_curva + self.__penultimo_saldo_itau
        self.__penultimo_total_a_mercado = self.__penultimo_saldo_ifb_em_reais + self.__penultimo_saldo_btg + self.__penultimo_saldo_xp_a_mercado + self.__penultimo_saldo_itau

        self.__delta_saldo_ifb = 100 * (self.__ultimo_saldo_ifb - self.__penultimo_saldo_ifb) / self.__penultimo_saldo_ifb
        self.__delta_saldo_ifb_em_reais = 100 * (self.__ultimo_saldo_ifb_em_reais - self.__penultimo_saldo_ifb_em_reais) / self.__penultimo_saldo_ifb_em_reais
        self.__delta_saldo_btg = 100 * (self.__ultimo_saldo_btg - self.__penultimo_saldo_btg) / self.__penultimo_saldo_btg
        self.__delta_saldo_xp_na_curva = 100 * (self.__ultimo_saldo_xp_na_curva - self.__penultimo_saldo_xp_na_curva) / self.__penultimo_saldo_xp_na_curva
        self.__delta_saldo_xp_a_mercado = 100 * (self.__ultimo_saldo_xp_a_mercado - self.__penultimo_saldo_xp_a_mercado) / self.__penultimo_saldo_xp_a_mercado
        self.__delta_saldo_itau = 100 * (self.__ultimo_saldo_itau - self.__penultimo_saldo_itau) / self.__penultimo_saldo_itau
        
        self.__delta_total_na_curva = 100 * (self.__ultimo_total_na_curva - self.__penultimo_total_na_curva) / self.__penultimo_total_na_curva
        self.__delta_total_a_mercado = 100 * (self.__ultimo_total_a_mercado - self.__penultimo_total_a_mercado) / self.__penultimo_total_a_mercado
