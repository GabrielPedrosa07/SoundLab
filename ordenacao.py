"""
TAD Ordenação — Aula 12 aplicada ao SoundLab (Semana 6)

Implementa manualmente a ordenação por inserção (Insertion Sort), com custo
O(n²) no pior caso, recebendo uma função 'chave' para extrair o critério
de comparação (ex: duração em segundos ou número de execuções).
"""


def ordenar_por_insercao(lista, chave, decrescente=False):
    """Ordena e devolve uma nova lista usando Insertion Sort,
    comparando os elementos através da função 'chave'."""
    dados = list(lista)
    for i in range(1, len(dados)):
        atual = dados[i]
        valor_atual = chave(atual)
        j = i - 1

        if decrescente:
            while j >= 0 and chave(dados[j]) < valor_atual:
                dados[j + 1] = dados[j]
                j -= 1
        else:
            while j >= 0 and chave(dados[j]) > valor_atual:
                dados[j + 1] = dados[j]
                j -= 1

        dados[j + 1] = atual

    return dados
