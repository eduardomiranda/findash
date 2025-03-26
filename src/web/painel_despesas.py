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
from src.utils.misc import formar_valor_monetario


locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

streamit_login()

if st.session_state.logged_in:

    if 'dados_bancarios' not in st.session_state:

        file_id = st.secrets['dados']['dados_bancarios_file_id']
        dados_banc = dados_bancarios(file_id)
        st.session_state.dados_bancarios = dados_banc

    dados_bancarios = st.session_state.dados_bancarios

    col11, col12 = st.columns(2)
    inicio = col11.date_input("Início", datetime.date(2024, 1, 1))
    fim    = col12.date_input("Fim", datetime.date(2024, 12, 31))

    st.divider()

    options = ('Por Categoria', 'Por Projeto')
    options_icons = ['bar-chart-line', 'gem'] # https://icons.getbootstrap.com/
    option = option_menu(None, options, icons=options_icons, menu_icon="cast", default_index=0, orientation="horizontal")


    if option == options[0] :

        gastos_totais = dados_bancarios.gastos_totais_no_periodo(inicio, fim)
        st.metric("Gastos Totais", formar_valor_monetario(gastos_totais), "", border = True )

        df_categoria_dresult = dados_bancarios.get_gastos_totais_por_categoria(inicio, fim)


        ylabel = df_groupby_column_name = df_categoria_dresult.columns.values[0]
        xlabel = df_column_values_name = df_categoria_dresult.columns.values[1]
        title  = 'Gastos totais'

        chart = barh_chart(df_categoria_dresult, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, True)
        st.pyplot(chart)


        # Combobox para seleção de categoria
        categorias = dados_bancarios.get_categorias(inicio, fim)
        categoria_selecionada = st.selectbox('Selecione a Categoria:', categorias)


        if not dados_bancarios.existem_dados_para_a_categoria(inicio, fim, categoria_selecionada):

            df_dresult = None
            df_groupby_column_name = None
            ylabel = None

            subcategorias = dados_bancarios.get_subcategorias(inicio, fim, categoria_selecionada)

            if 1 < len(subcategorias):
                df_dresult = dados_bancarios.get_gastos_totais_por_categoria_e_subcategoria(inicio, fim, categoria_selecionada)
                ylabel = df_groupby_column_name = 'Subcategoria'

            else:
                df_dresult = dados_bancarios.get_gastos_totais_por_categoria_e_contato(inicio, fim, categoria_selecionada)
                ylabel = df_groupby_column_name = 'Contato'


            xlabel = df_column_values_name = df_dresult.columns.values[2] 
            title  = categoria_selecionada

            chart = barh_chart(df_dresult, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, True)
            st.pyplot(chart)

            if st.button("Show me the data!", type="primary", key = "6915d7f6-effe-4f58-b589-ae599f594316"):
                st.dataframe(df_dresult)

        else:
            st.write("Nenhum dado encontrado para a seleção atual.")


    
        # if 0 < len(subcategorias):
        #     subcategoria_selecionada = st.selectbox('Selecione a Subcategoria:', subcategorias)

        #     # Filtra os dados com base na categoria e subcategoria selecionadas
        #     df_filtrado = dados_bancarios.df[(dados_bancarios.df['Categoria'] == categoria_selecionada) & (dados_bancarios.df['Subcategoria'] == subcategoria_selecionada)]

        #     df_dresult = df_filtrado.groupby(['Subcategoria','Contato'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)

        #     # Cria o gráfico Matplotlib
        #     if not df_filtrado.empty:

        #         df_groupby_column_name = 'Contato'
        #         df_column_values_name = 'Valor efetivo'
        #         xlabel = 'Valor Efetivo (R$)'
        #         ylabel = 'Contato'
        #         title  = subcategoria_selecionada

        #         chart = barh_chart(df_dresult, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title)
        #         st.pyplot(chart)

        #         if st.button("Show me the data!", type="primary", key = "d9aaea47-f06c-4136-ae31-21cb92530906"):
        #             st.dataframe(df_filtrado.sort_values('Valor efetivo', ascending=True))

        #     else:
        #         st.write("Nenhum dado encontrado para a seleção atual.")


    elif option == options[1] :

        df = dados_bancarios.get_gastos_totais_por_projeto(inicio, fim)

        ylabel = df_groupby_column_name = df.columns.values[0]
        xlabel = df_column_values_name = df.columns.values[1]
        title  = 'Gastos totais por projeto'

        chart = barh_chart(df, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, True)
        st.pyplot(chart)

        if st.button("Show me the data!", type="primary", key = "ac31cd5f-e677-4b94-9927-00c5fc1c58e8"):
            st.dataframe(dados_bancarios.get_gastos_de_projetos(inicio, fim))
