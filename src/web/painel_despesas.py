import sys
  
# append the path of the parent directory
sys.path.append(".")

import datetime
import locale
import streamlit as st
import pandas as pd

from streamlit_option_menu import option_menu

from src.data.dados_bancarios import dados_bancarios
from src.utils.myplot import barh_chart, pie_chart
from src.utils.login import streamit_login


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

streamit_login()

if st.session_state.logged_in:

    df_dados_bancarios = None
    if 'df_dados_bancarios' not in st.session_state:
        dados_banc = dados_bancarios(st.secrets['dados']['file_id_dados_bancarios'])
        st.session_state.df_dados_bancarios = dados_banc.df

    df_dados_bancarios = st.session_state.df_dados_bancarios


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

        df_dados_bancarios["Data efetiva"] = pd.to_datetime(df_dados_bancarios["Data efetiva"]).dt.date
        df_dados_bancarios =  df_dados_bancarios.loc[(df_dados_bancarios['Data efetiva'] >= inicio) & (df_dados_bancarios['Data efetiva'] <= fim)]


        df_dados_bancarios = df_dados_bancarios[ df_dados_bancarios['Tipo'] == 'Despesa']

        gastos_totais = locale.currency(df_dados_bancarios['Valor efetivo'].sum() , grouping=True)
        st.metric("Gastos Totais", gastos_totais, "" )


        df_categoria_dresult = df_dados_bancarios.groupby(['Categoria'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)
        # st.pyplot(grafico(df_categoria_dresult))

        df_groupby_column_name = 'Categoria'
        df_column_values_name = 'Valor efetivo'
        xlabel = 'Valor Efetivo (R$)'
        ylabel = 'Categoria'
        title  = 'Gastos totais'

        chart = barh_chart(df_categoria_dresult, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, True)
        st.pyplot(chart)



        # Combobox para seleção de categoria
        categorias = df_dados_bancarios['Categoria'].unique()
        categoria_selecionada = st.selectbox('Selecione a Categoria:', categorias)

        # Filtra as subcategorias com base na categoria selecionada
        subcategorias = df_dados_bancarios[df_dados_bancarios['Categoria'] == categoria_selecionada]['Subcategoria'].unique()


        df_filtrado = df_dados_bancarios[df_dados_bancarios['Categoria'] == categoria_selecionada]

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

            if st.button("Show me the data!", type="primary", key = "6915d7f6-effe-4f58-b589-ae599f594316"):
                st.dataframe(df_filtrado.sort_values('Valor efetivo', ascending=True))

        else:
            st.write("Nenhum dado encontrado para a seleção atual.")



        
        if 0 < len(subcategorias):
            subcategoria_selecionada = st.selectbox('Selecione a Subcategoria:', subcategorias)

            # Filtra os dados com base na categoria e subcategoria selecionadas
            df_filtrado = df_dados_bancarios[(df_dados_bancarios['Categoria'] == categoria_selecionada) & (df_dados_bancarios['Subcategoria'] == subcategoria_selecionada)]

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

                if st.button("Show me the data!", type="primary", key = "d9aaea47-f06c-4136-ae31-21cb92530906"):
                    st.dataframe(df_filtrado.sort_values('Valor efetivo', ascending=True))

            else:
                st.write("Nenhum dado encontrado para a seleção atual.")


    elif option == options[1] :

        df_dados_bancarios["Data efetiva"] = pd.to_datetime(df_dados_bancarios["Data efetiva"]).dt.date
        df_dados_bancarios =  df_dados_bancarios.loc[(df_dados_bancarios['Data efetiva'] > inicio) & (df_dados_bancarios['Data efetiva'] <= fim)]


        df_dados_bancarios = df_dados_bancarios[ df_dados_bancarios['Projeto'] != 'Sem projeto']

        df_projeto_result = df_dados_bancarios.groupby(['Projeto'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)

        df_groupby_column_name = 'Projeto'
        df_column_values_name = 'Valor efetivo'
        xlabel = 'Valor Efetivo (R$)'
        ylabel = 'Projeto'
        title  = 'Gastos totais por projeto'

        chart = barh_chart(df_projeto_result, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, True)
        st.pyplot(chart)

        if st.button("Show me the data!", type="primary", key = "ac31cd5f-e677-4b94-9927-00c5fc1c58e8"):
            st.dataframe(df_dados_bancarios.sort_values('Valor efetivo', ascending=True))
