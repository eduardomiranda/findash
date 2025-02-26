import sys
  
# append the path of the parent directory
sys.path.append(".")


import datetime
import locale
import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

from src.data.data_prep import data_prep
from src.utils.google_drive import download_csv_from_google_drive
from src.utils.myplot import barh_chart, pie_chart
from src.web.painel_login import show_login_popup
from src.database.mongo_connection import consulta_varios_documentos



locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


if st.secrets['environment'].get("location", '') == "local":
    st.session_state.logged_in = True
else:
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        show_login_popup()


if st.session_state.logged_in:

    df = None

    if 'df' not in st.session_state:
        st.session_state.df = download_csv_from_google_drive(st.secrets['dados']['file_id'])
        df = st.session_state.df

        mongodb_uri     = st.secrets['mongodb'].get("mongodb_uri", '')
        db_name         = st.secrets['mongodb'].get("mongodb_db", '')
        collection_name = st.secrets['mongodb'].get("mongodb_collection_data_prep", '')
        query = {}
        condicoes = consulta_varios_documentos( mongodb_uri, db_name, collection_name, query )
        data_prep(df, condicoes)
    else:
        df = st.session_state.df


    # Título do aplicativo
    # st.title('💸 Análise de Despesas')

    col11, col12 = st.columns(2)
    inicio = col11.date_input("Início", datetime.date(2024, 1, 1))
    fim    = col12.date_input("Fim", datetime.date(2024, 12, 31))

    st.divider()

    options = ('Por Categoria', 'Por Projeto')
    options_icons = ['bar-chart-line', 'gem'] # https://icons.getbootstrap.com/
    option = option_menu(None, options, icons=options_icons, menu_icon="cast", default_index=0, orientation="horizontal")


    if option == options[0] :

        df["Data efetiva"] = pd.to_datetime(df["Data efetiva"]).dt.date
        df =  df.loc[(df['Data efetiva'] >= inicio) & (df['Data efetiva'] <= fim)]


        df = df[ df['Tipo'] == 'Despesa']

        gastos_totais = locale.currency(df['Valor efetivo'].sum() , grouping=True)
        st.metric("Gastos Totais", gastos_totais, "" )


        df_categoria_dresult = df.groupby(['Categoria'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)
        # st.pyplot(grafico(df_categoria_dresult))

        df_groupby_column_name = 'Categoria'
        df_column_values_name = 'Valor efetivo'
        xlabel = 'Valor Efetivo (R$)'
        ylabel = 'Categoria'
        title  = 'Gastos totais'

        chart = barh_chart(df_categoria_dresult, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, True)
        st.pyplot(chart)



        # Combobox para seleção de categoria
        categorias = df['Categoria'].unique()
        categoria_selecionada = st.selectbox('Selecione a Categoria:', categorias)

        # Filtra as subcategorias com base na categoria selecionada
        subcategorias = df[df['Categoria'] == categoria_selecionada]['Subcategoria'].unique()


        df_filtrado = df[df['Categoria'] == categoria_selecionada]

        # Cria o gráfico Matplotlib
        if not df_filtrado.empty:

            df_dresult = None
            df_groupby_column_name = None
            ylabel = None

            if 1 < len(subcategorias):
                df_dresult = df_filtrado.groupby(['Categoria','Subcategoria'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)
                df_groupby_column_name = 'Subcategoria'
                ylabel = 'Subcategoria'
            else:
                df_dresult = df_filtrado.groupby(['Categoria','Contato'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)
                df_groupby_column_name = 'Contato'
                ylabel = 'Contato'


            df_column_values_name = 'Valor efetivo'
            xlabel = 'Valor Efetivo (R$)'
            title  = categoria_selecionada

            chart = barh_chart(df_dresult, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, True)
            st.pyplot(chart)

            st.dataframe(df_filtrado.sort_values('Valor efetivo', ascending=True))

        else:
            st.write("Nenhum dado encontrado para a seleção atual.")



        
        if 0 < len(subcategorias):
            subcategoria_selecionada = st.selectbox('Selecione a Subcategoria:', subcategorias)

            # Filtra os dados com base na categoria e subcategoria selecionadas
            df_filtrado = df[(df['Categoria'] == categoria_selecionada) & (df['Subcategoria'] == subcategoria_selecionada)]

            df_dresult = df_filtrado.groupby(['Subcategoria','Contato'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)

            # Cria o gráfico Matplotlib
            if not df_filtrado.empty:

                df_groupby_column_name = 'Contato'
                df_column_values_name = 'Valor efetivo'
                xlabel = 'Valor Efetivo (R$)'
                ylabel = 'Contato'
                title  = subcategoria_selecionada

                chart = barh_chart(df_dresult, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title)
                st.pyplot(chart)

                st.dataframe(df_filtrado.sort_values('Valor efetivo', ascending=True))

            else:
                st.write("Nenhum dado encontrado para a seleção atual.")


    elif option == options[1] :

        df["Data efetiva"] = pd.to_datetime(df["Data efetiva"]).dt.date
        df =  df.loc[(df['Data efetiva'] > inicio) & (df['Data efetiva'] <= fim)]


        df = df[ df['Projeto'] != 'Sem projeto']

        df_projeto_result = df.groupby(['Projeto'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)

        df_groupby_column_name = 'Projeto'
        df_column_values_name = 'Valor efetivo'
        xlabel = 'Valor Efetivo (R$)'
        ylabel = 'Projeto'
        title  = 'Gastos totais por projeto'

        chart = barh_chart(df_projeto_result, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, True)
        st.pyplot(chart)

        st.dataframe(df.sort_values('Valor efetivo', ascending=True))
