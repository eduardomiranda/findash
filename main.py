import streamlit as st
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import gdown

# Function to show the login popup
def show_login_popup():
    with st.form(key='login_form'):
        st.write("Please log in")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            if username == st.secrets['authentication'].get("username", '') and password == st.secrets['authentication'].get("password", ''):  # Replace with your authentication logic
                st.session_state.logged_in = True
                # st.session_state.username = username
                st.success("Logged in successfully!")
            else:
                st.error("Invalid username or password")


# # Tela de login
# st.sidebar.title("Login")
# login = st.sidebar.text_input("Usuário")
# senha = st.sidebar.text_input("Senha", type="password")




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




def renomeacao_campos(df):
    pass




def download_csv_from_google_drive(file_id):
    """
    Downloads a CSV file from Google Drive.

    Args:
        file_id (str): The Google Drive file ID (found in the file's shareable link).
        output_file (str): The name of the output file to save the CSV.

    Returns:
        pd.DataFrame: The downloaded CSV file as a pandas DataFrame.
    """

    output_file = "0c04cf8f-3094-4783-b0fd-f7dd96412290.csv"

    # Construct the download URL
    url = f"https://drive.google.com/uc?id={file_id}"
    
    # Download the file
    gdown.download(url, output_file, quiet=False)
    
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(output_file)
    
    return df





def grafico(df_admin):
        
    df_admin['Valor efetivo'] = df_admin['Valor efetivo'] * -1

    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot horizontal bars
    bars = ax.barh(df_admin['Subcategoria'], df_admin['Valor efetivo'], color='#1f77b4', edgecolor='black', alpha=0.8)

    # Add values at the end of the bars
    for bar, value in zip(bars, df_admin['Valor efetivo']):
        ax.text(bar.get_width() + max(df_admin['Valor efetivo']) * 0.02,  # Position of the text at the end of the bar
                bar.get_y() + bar.get_height()/2,
                f'R$ {value:,.2f}',
                va='center', ha='left', fontsize=10, color='black')

    # Customize the plot
    ax.set_xlabel('Valor Efetivo (R$)', fontsize=12, labelpad=10)
    ax.set_ylabel('Subcategoria', fontsize=12, labelpad=10)
    ax.set_title('Despesas Administrativas', fontsize=16, pad=20, fontweight='bold')

    # Improve grid and ticks
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)  # Place gridlines below bars
    ax.tick_params(axis='both', which='major', labelsize=10)

    # Remove spines (borders) for a cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)

    # Add a light background color
    ax.set_facecolor('#f7f7f7')
    fig.patch.set_facecolor('#ffffff')

    return fig

    # # Adjust layout for better spacing
    # plt.tight_layout()

    # # Show the plot
    # plt.show()



if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login_popup()

else:
    # df = pd.read_csv('Meu_Dinheiro_20250205142457.csv')

    df = None

    if 'df' not in st.session_state:
        st.session_state.df = download_csv_from_google_drive(st.secrets['dados']['file_id'])
        df = st.session_state.df

        delecao_colunas_desnecessarias(df)
        correcao_tipos_dados(df)
        renomeacao_campos(df)

    else:
        df = st.session_state.df


    # Título do aplicativo
    st.title('Análise de Despesas')

    df = df[ df['Tipo'] == 'Despesa']

    # Combobox para seleção de categoria
    categorias = df['Categoria'].unique()
    categoria_selecionada = st.selectbox('Selecione a Categoria:', categorias)

    # # Filtra as subcategorias com base na categoria selecionada
    # subcategorias = df[df['Categoria'] == categoria_selecionada]['Subcategoria'].unique()
    # subcategoria_selecionada = st.selectbox('Selecione a Subcategoria:', subcategorias)

    # Filtra os dados com base na categoria e subcategoria selecionadas
    df_filtrado = df[df['Categoria'] == categoria_selecionada]

    df_dresult = df_filtrado.groupby(['Categoria','Subcategoria'])['Valor efetivo'].sum().reset_index().sort_values('Valor efetivo', ascending=False)


    # Cria o gráfico Matplotlib
    if not df_filtrado.empty:
        st.pyplot(grafico(df_dresult))
        st.dataframe(df_filtrado.sort_values('Valor efetivo', ascending=True))

    else:
        st.write("Nenhum dado encontrado para a seleção atual.")
