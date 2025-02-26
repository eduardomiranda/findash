import pandas as pd


def delecao_colunas_desnecessarias(df):
    # df.drop('Status', axis=1, inplace=True)
    df.drop('Data prevista', axis=1, inplace=True)
    df.drop('Venc. Fatura', axis=1, inplace=True)
    df.drop('Valor previsto', axis=1, inplace=True)
    df.drop('Forma', axis=1, inplace=True)
    df.drop('ID Único', axis=1, inplace=True)
    df.drop('Tags', axis=1, inplace=True)
    df.drop('Cartão', axis=1, inplace=True)
    df.drop('Meta de Economia', axis=1, inplace=True)
    df.drop('Repetição', axis=1, inplace=True)
    df.drop('Razão social', axis=1, inplace=True)
    df.drop('N. Documento', axis=1, inplace=True)
    df.drop('Data competência', axis=1, inplace=True)

    df.drop('Status', axis=1, inplace=True)
    df.drop('Conta', axis=1, inplace=True)
    df.drop('Conta transferência', axis=1, inplace=True)
    df.drop('CPF/CNPJ', axis=1, inplace=True)


def  correcao_tipos_dados(df):
    df['Valor efetivo'] = df['Valor efetivo'].fillna('0')

    # Remove "R$ " and replace '.' with '' and ',' with '.'
    df['Valor efetivo'] = df['Valor efetivo'].str.replace('R\$ ', '')
    df['Valor efetivo'] = df['Valor efetivo'].str.replace('.', '')
    df['Valor efetivo'] = df['Valor efetivo'].str.replace(',', '.')

    # Convert the resulting string to a float
    df['Valor efetivo'] = df['Valor efetivo'].astype(float)

    # Convert the string column to datetime with the correct format
    df['Data efetiva'] = pd.to_datetime(df['Data efetiva'], dayfirst=True, format='%d/%m/%Y')




def rename(df, condicoes):

    for condicao in condicoes:
        dataframe_column_name = condicao.get("dataframe_column_name", None)

        if dataframe_column_name:
            old_value = condicao.get("old_value", None)
            new_value = condicao.get("new_value", None)

            df[dataframe_column_name] = df[dataframe_column_name].replace(old_value, new_value)




def remover_registros_investimentos(df):

    index_investimentos = df[ df['Categoria'] == 'Investimentos' ].index
    df.drop(index_investimentos, inplace=True)



def remover_registros_transferencias(df):

    index_transferencias = df[ df['Categoria'] == 'Transferência' ].index
    df.drop(index_transferencias, inplace=True)



def remover_registros_cartao_credito(df):

    index_cartao_credito = df[ df['Subcategoria'] == 'Cartão de créditos' ].index
    df.drop(index_cartao_credito, inplace=True)



def data_prep(df, condicoes=[]):
    delecao_colunas_desnecessarias(df)
    correcao_tipos_dados(df)
    remover_registros_investimentos(df)
    remover_registros_transferencias(df)
    remover_registros_cartao_credito(df)
    rename(df, condicoes)



