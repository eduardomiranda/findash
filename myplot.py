# import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def barh_chart(df, df_groupby_column_name, df_column_values_name, xlabel, ylabel, title, flip_sign=False):
        
    if flip_sign:
        df['Valor efetivo'] = df['Valor efetivo'] * -1
        
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 8))

    # Plot horizontal bars
    bars = ax.barh(df[df_groupby_column_name], df[df_column_values_name], color='#1f77b4', edgecolor='black', alpha=0.8)

    # Add values at the end of the bars
    for bar, value in zip(bars, df['Valor efetivo']):
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