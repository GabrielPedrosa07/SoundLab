def busca_linear_contada(lista, titulo):
    """Busca linear instrumentada: devolve (faixa_ou_None,
    numero_de_comparacoes feitas até achar ou esgotar a lista)."""
    comparacoes = 0
    for faixa in lista:
        comparacoes += 1
        if faixa.titulo.lower() == titulo.lower():
            return faixa, comparacoes
    return None, comparacoes


def busca_binaria_contada(lista_ordenada, titulo):
    """Busca binaria instrumentada sobre uma lista JA ORDENADA
    por titulo. Devolve (faixa_ou_None, numero_de_comparacoes)."""
    inicio, fim, comparacoes = 0, len(lista_ordenada) - 1, 0
    while inicio <= fim:
        comparacoes += 1
        meio = (inicio + fim) // 2
        if lista_ordenada[meio].titulo.lower() == titulo.lower():
            return lista_ordenada[meio], comparacoes
        elif lista_ordenada[meio].titulo.lower() < titulo.lower():
            inicio = meio + 1
        else:
            fim = meio - 1
    return None, comparacoes
