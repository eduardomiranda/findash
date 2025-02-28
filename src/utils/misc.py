


def inverter_pontuacao(texto):

	return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formar_valor_monetario(valor):

	return inverter_pontuacao(f'R$ {valor:,.2f}')