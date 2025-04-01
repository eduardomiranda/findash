import sys
  
# append the path of the parent directory
sys.path.append(".")

import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt

from pandasai import Agent
from pandasai import SmartDataframe, SmartDatalake
from pandasai.llm.openai import OpenAI

from src.utils.data_loader import get_dados_ifb, get_dados_bancarios

with st.spinner("Obtendo dados...", show_time=True):
	dados_ifb = get_dados_ifb()
	dados_bancarios = get_dados_bancarios()


if 'smart_dl' not in st.session_state:
	api_token = st.secrets['openai']['api_key']
	# openai_model = st.secrets['openai']['openai_model']

	# Creating an instance of the OpenAI class by passing the API token. This instance will be used to interact with OpenAI's language model (LLM).
	llm = OpenAI(api_token=api_token)

	st.session_state.smart_dl = SmartDatalake([dados_ifb.df, dados_bancarios.df], config={"llm": llm})



prompt = st.text_input("Pergunta (Apenas em Inglês por enquanto 😔)", "How much was spent in 2024?")
response = st.session_state.smart_dl.chat(prompt)

if isinstance(response, pd.DataFrame):
	st.dataframe(response)

elif isinstance(response, str) and response.endswith(".png"):
	st.image(response)

else:
	st.markdown(response)