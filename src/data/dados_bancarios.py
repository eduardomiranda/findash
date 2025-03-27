import pandas as pd
import streamlit as st
from datetime import datetime, date

from src.data.data_loader import download_csv_from_google_drive, download_google_spreadsheet

class dados_bancarios():

    def __init__(self, file_id):

        self._df = download_csv_from_google_drive(file_id)

        self.delecao_colunas_desnecessarias()
        self.correcao_tipos_dados()
        self.remover_registros_investimentos()
        self.remover_registros_transferencias()
        self.remover_registros_cartao_credito()
        self.anonimizacao_dados_salario()
        self.anonimizacao_dados_bonus()
        self.data_prep()


    @property
    def df(self):
        return self._df



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
        self._df['Data efetiva'] = pd.to_datetime(self._df['Data efetiva']).dt.date



    def anonimizacao_dados(self, categoria, subcategoria, tipo):

        df_aux = self._df

        # Converta a coluna 'Data efetiva' em objetos de data e hora, caso ainda não o tenha feito
        df_aux['Data efetiva AUX'] = pd.to_datetime(df_aux['Data efetiva'])

        # Extraia o mês e o ano da coluna 'Data efetiva'
        df_aux['Ano-Mês'] = df_aux['Data efetiva AUX'].dt.to_period('M')

        # Agrupar por mês e somar os salários
        monthly_salary_expenses = df_aux[(df_aux.Categoria == categoria) & (df_aux.Subcategoria == subcategoria)].groupby('Ano-Mês')['Valor efetivo'].sum().reset_index()

        # Ajusta a coluna Data efetiva com o último dia de cada mês. Ou seja, na coluna Ano-Mês temos 2023-01, então na coluna Data efetiva teremos 2023-01-31 
        monthly_salary_expenses['Data efetiva'] = monthly_salary_expenses['Ano-Mês'].dt.to_timestamp(how='end')

        # Adição de colunas importantes para as demais análises
        monthly_salary_expenses['Categoria'] = categoria
        monthly_salary_expenses['Subcategoria'] = subcategoria
        monthly_salary_expenses['Tipo'] = tipo

        # Remova as linhas de salário originais para privacidade
        df_aux = df_aux[~((df_aux.Categoria == categoria) & (df_aux.Subcategoria == subcategoria))]

        # Mesclar as despesas mensais de salário de volta ao DataFrame original
        self._df = pd.concat([df_aux, monthly_salary_expenses])

        # Faz a conversão da coluna 'Data efetiva' para o formato de data 
        self._df['Data efetiva'] = pd.to_datetime(self._df['Data efetiva']).dt.date




    def anonimizacao_dados_salario(self):
        categoria = 'Pessoal'
        subcategoria = 'Salários'
        tipo = 'Despesa'

        self.anonimizacao_dados(categoria, subcategoria, tipo)



    def anonimizacao_dados_bonus(self):
        categoria = 'Pessoal'
        subcategoria = 'Bônus'
        tipo = 'Despesa'

        self.anonimizacao_dados(categoria, subcategoria, tipo)



    def __get_conditions_column_value_replace(self):

        file_id = st.secrets['dados']['dados_bancarios_data_prep_file_id']
        sheet_name = 'column_value_replace'

        return download_google_spreadsheet(file_id, sheet_name)



    def __get_conditions_categoria_subcategoria_replace(self):

        file_id = st.secrets['dados']['dados_bancarios_data_prep_file_id']
        sheet_name = 'categoria_subcategoria_replace'

        return download_google_spreadsheet(file_id, sheet_name)



    def data_prep(self):

        column_value_replace_df = self.__get_conditions_column_value_replace()

        for index, row in column_value_replace_df.iterrows():
            column_name = row['column_name']

            if column_name:
                old_value = row['old_value']
                new_value = row['new_value']

                self._df[column_name] = self._df[column_name].replace(old_value, new_value)


        categoria_subcategoria_replace_df = self.__get_conditions_categoria_subcategoria_replace()

        for index, row in categoria_subcategoria_replace_df.iterrows():

            old_category    = row['old_category']
            old_subcategory = row['old_subcategory']
            new_category    = row['new_category']
            new_subcategory = row['new_subcategory']

            # Define conditions
            condition1 = self._df['Categoria'] == old_category
            condition2 = self._df['Subcategoria'] == old_subcategory

            # Combine conditions (both must be True)
            mask = condition1 & condition2

            # Replace values in columns C and D where the mask is True
            self._df.loc[mask, ['Categoria', 'Subcategoria']] = [new_category, new_subcategory]




    def remover_registros_investimentos(self):

        index_investimentos = self._df[ self._df['Categoria'] == 'Investimentos' ].index
        self._df.drop(index_investimentos, inplace=True)



    def remover_registros_transferencias(self):

        index_transferencias = self._df[ self._df['Categoria'] == 'Transferência' ].index
        self._df.drop(index_transferencias, inplace=True)



    def remover_registros_cartao_credito(self):

        index_cartao_credito = self._df[ self._df['Subcategoria'] == 'Cartão de créditos' ].index
        self._df.drop(index_cartao_credito, inplace=True)


    def filtrar_dados_por_periodo(self, inicio, fim):

        return self._df.loc[(self._df['Data efetiva'] >= inicio) & (self._df['Data efetiva'] <= fim)]



    def filtrar_receita_por_periodo(self, inicio, fim):

        df = self.filtrar_dados_por_periodo(inicio, fim)
        return df[ (df['Tipo'] == 'Receita') & (~df['Categoria'].isin(['Remunera+', 'Resgate', 'Devolução'])) ]


    def receitas_totais_no_periodo(self, inicio, fim):

        df = self.filtrar_receita_por_periodo(inicio, fim)
        receitas_totais = df['Valor efetivo'].sum()
        return receitas_totais


    def get_vendas_por_contato(self, inicio, fim):

        df = self.filtrar_receita_por_periodo(inicio, fim)
        return df[df['Categoria'] == 'Vendas'].groupby(['Contato'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=True)



    def filtrar_despesas_por_periodo(self, inicio, fim):

        df = self.filtrar_dados_por_periodo(inicio, fim)
        return df[ df['Tipo'] == 'Despesa']


    def gastos_totais_no_periodo(self, inicio, fim):

        df = self.filtrar_despesas_por_periodo(inicio, fim)
        gastos_totais = df['Valor efetivo'].sum()
        return gastos_totais


    def get_gastos_totais_por_categoria(self, inicio, fim):

        df = self.filtrar_despesas_por_periodo(inicio, fim)
        return df.groupby(['Categoria'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)


    def get_categorias(self, inicio, fim):

        df = self.filtrar_despesas_por_periodo(inicio, fim)
        return df['Categoria'].unique()


    def get_dados_por_categoria(self, inicio, fim, categoria):

        df = self.filtrar_despesas_por_periodo(inicio, fim)
        return df[df['Categoria'] == categoria].sort_values('Valor efetivo', ascending=True)


    def get_subcategorias(self, inicio, fim, categoria):

        df = self.filtrar_despesas_por_periodo(inicio, fim)
        return df[df['Categoria'] == categoria]['Subcategoria'].unique()


    def existem_dados_para_a_categoria(self, inicio, fim, categoria):

        df = self.filtrar_despesas_por_periodo(inicio, fim)
        return df[df['Categoria'] == categoria].empty


    def get_gastos_totais_por_categoria_e_subcategoria(self, inicio, fim, categoria):

        df = self.get_dados_por_categoria(inicio, fim, categoria)
        return df.groupby(['Categoria','Subcategoria'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)


    def get_gastos_totais_por_categoria_e_contato(self, inicio, fim, categoria):

        df = self.get_dados_por_categoria(inicio, fim, categoria)
        return df.groupby(['Categoria','Contato'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)


    def get_gastos_de_projetos(self, inicio, fim):

        df = self.filtrar_despesas_por_periodo(inicio, fim)
        return df[ df['Projeto'] != 'Sem projeto']


    def get_gastos_totais_por_projeto(self, inicio, fim):

        df = self.get_gastos_de_projetos(inicio, fim)
        return df.groupby(['Projeto'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)
