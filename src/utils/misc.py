from datetime import datetime



def inverter_pontuacao(texto):

	return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formar_valor_monetario(valor):

	return inverter_pontuacao(f'R$ {valor:,.2f}')



def converter_data_para_formato_brasileiro(data_americana: str) -> str:

	data_objeto = datetime.strptime(data_americana, "%Y-%m-%d")

	meses_pt = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

	data_formatada = f"{data_objeto.day} de {meses_pt[data_objeto.month - 1]} de {data_objeto.year}"

	return data_formatada