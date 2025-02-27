# import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import numpy as np


# Formatando o eixo X para exibir valores em reais
def formato_reais(x, pos):
    return f'R$ {x:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".")



def barh_chart(df, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, flip_sign=False):
        
    if flip_sign:
        df['Valor efetivo'] = df['Valor efetivo'] * -1
        
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot horizontal bars
    bars = ax.barh(df[df_groupby_column_name], df[df_column_values_name], color='#1f77b4', edgecolor='black', alpha=0.8)

    total_width = sum([bar.get_width() for bar in bars])

    # Add values at the end of the bars
    for bar, value in zip(bars, df['Valor efetivo']):

        percentual = bar.get_width() / total_width * 100
        ax.text(10000,
                bar.get_y() + bar.get_height()/2,
                f'{percentual:,.2f}%',
                va='center', ha='left', fontsize=10, fontweight='bold', color='white')

        ax.text(bar.get_width() + max(df['Valor efetivo']) * 0.02,  # Position of the text at the end of the bar
                bar.get_y() + bar.get_height()/2,
                f'R$ {value:,.2f}',
                va='center', ha='left', fontsize=10, color='black')


    # Customize the plot
    ax.set_xlabel(xlabel, fontsize=12, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=12, labelpad=10)
    ax.set_title(title, fontsize=16, pad=20, fontweight='bold')

    # Improve grid and ticks
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    ax.set_axisbelow(True)  # Place gridlines below bars
    ax.tick_params(axis='both', which='major', labelsize=10)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(formato_reais))


    # Remove spines (borders) for a cleaner look
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(True)

    # Add a light background color
    ax.set_facecolor('#f7f7f7')
    fig.patch.set_facecolor('#ffffff')

    return fig



def pie_chart(df, df_groupby_column_name, df_column_values_name, title, flip_sign=False):

    if flip_sign:
        df['Valor efetivo'] = df['Valor efetivo'] * -1

    # Create the plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Define colors (using the same blue color and a consistent palette)
    colors = ['#03045e', '#023e8a', '#0077b6', '#0096c7', '#00b4d8', '#48cae4', '#90e0ef', '#ade8f4', '#caf0f8']
    # colors = ['#3366cc','#dc3912','#ff9900','#109618','#990099','#0099c6','#dd4477','#66aa00','#b82e2e','#316395','#994499','#22aa99','#aaaa11','#6633cc','#e67300','#8b0707','#651067','#329262','#5574a6','#3b3eac','#b77322','#16d620','#b91383','#f4359e','#9c5935','#a9c413','#2a778d','#668d1c','#bea413','#0c5922','#743411']

    # Plot the pie chart
    wedges, texts, autotexts = ax.pie(df[df_column_values_name], 
                                      labels=df[df_groupby_column_name], 
                                      autopct='%1.1f%%', 
                                      startangle=90, 
                                      colors=colors, 
                                      textprops={'fontsize': 12, 'color': 'black'}, 
                                      wedgeprops={'edgecolor': 'black', 'linewidth': 0.5})

    # Customize the plot
    ax.set_title(title, fontsize=16, pad=20, fontweight='bold')

    # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.axis('equal')

    # Add a light background color
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#f7f7f7')

    # Remove spines (borders) for a cleaner look
    for spine in ax.spines.values():
        spine.set_visible(False)

    return fig




def receita_bruta_por_produto_e_ano(df_agg):

    # Definindo cores personalizadas para cada produto
    # cores = ['#F1A104', '#00743F', '#25B396', '#70CED0', '#1E65A7', '#192E53', ] # https://br.pinterest.com/pin/variety-of-orange-green-blue-color-scheme-blue-schemecolorcom--619315386258482814/
    # cores = ['#BDD1BD', '#85B093', '#568F7C', '#326D6C', '#173C4C', '#07142B', '#000009'] # https://br.pinterest.com/pin/216665432067725843/
    # cores = ['#32AAB5', '#E7D39A', '#F1AA60', '#F27B68', '#E54787', '#BF219A', '#8E0F9C', '#4B1D91'] # https://br.pinterest.com/pin/6122149487251309/
    # cores = ['#001236', '#7C66BB', '#FF4F7B', '#FF6E77', '#FF8C73', '#FFBD80', '#FFFDC2', '#BAFAFF', '#00A2C7', '#43B171'] # https://br.pinterest.com/pin/58757970135987348/
    cores = ['#FF8C73', '#001236', '#43B171', '#EEEEEF', '#00A2C7', '#4B1D91', '#FFBD80' ]

    # Configurando o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    df_agg.plot(kind='barh', stacked=True, ax=ax, color=cores)

    ax.set_xlabel("Receita Bruta (R$)")
    ax.set_ylabel("Ano")
    ax.set_title("Receita Bruta por Produto e Ano")
    ax.legend(title="Produto", bbox_to_anchor=(1.05, 1), loc='upper left')

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(formato_reais))

    # Adicionando os valores totais ao final de cada barra
    for i, total in enumerate(df_agg.sum(axis=1)):
        ax.text(total * 1.02, i, f'R$ {total:,.2f}'.replace(",", "X").replace(".", ",").replace("X", "."),
                va='center', ha='left', fontsize=9, color='black')


    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()

    return fig






def receita_por_ano_produto_tipo(df_agg):        
    # Supondo que o DataFrame tenha as colunas 'Ano', 'Produto', 'Tipo' e 'Valor Serviços(R$)'

    df_agg.rename(columns={'Serviço ou \nLicença?': 'Legenda'}, inplace=True)


    # Obter os anos únicos
    anos = df_agg['Ano'].unique()

    # Criar uma paleta de cores consistente para os produtos
    produtos = df_agg['Produto'].unique()
    paleta_cores = sns.color_palette("husl", len(produtos))  # Ou use outra paleta de sua preferência
    cores_por_produto = dict(zip(produtos, paleta_cores))

    # Criar subplots para cada ano
    fig, axes = plt.subplots(len(anos), 1, figsize=(12, 6 * len(anos)))

    # Se houver apenas um ano, 'axes' não será um array, então precisamos tratar esse caso
    if len(anos) == 1:
        axes = [axes]

    # Loop através de cada ano e criar um gráfico de barras empilhadas
    for i, ano in enumerate(anos[::-1]):
        # Filtrar os dados para o ano atual
        data_ano = df_agg[df_agg['Ano'] == ano]

        # Criar uma tabela pivô para separar Produto e Serviço
        pivot_data = data_ano.pivot_table(index='Produto', columns='Legenda', values='Valor Serviços(R$)', aggfunc='sum', fill_value=0)


        # Ordenar os produtos para garantir consistência visual
        pivot_data = pivot_data.reindex(produtos, fill_value=0)

        # Criar o gráfico de barras empilhadas
        pivot_data.plot(kind='barh', stacked=True, ax=axes[i], color=['#4B1D91', '#43B171'])  # Cores para Produto e Serviço

        axes[i].set_xlabel('Receita Bruta (R$)')
        axes[i].set_ylabel('Produto')
        axes[i].set_title(f'Receita Bruta por Produto e Tipo no Ano {ano}')

        axes[i].xaxis.set_major_formatter(ticker.FuncFormatter(formato_reais))


        # Adicionar os valores nas barras
        for container in axes[i].containers:
            axes[i].bar_label(container, fontsize=8, padding=3, labels=[f'R$ {val:,.2f}'.replace(",", "X").replace(".", ",").replace("X", ".") if val != 0 else '' for val in container.datavalues])


    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.tight_layout()

    return fig

