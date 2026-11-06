"""
TAD Grafo de Recomendação — Aula 10 aplicada ao SoundLab (Semana 4)

Modela as faixas como vértices e a reprodução em sequência como arestas
(coocorrência). Usa Busca em Largura (BFS) com a FilaExecucao da Semana 1
para sugerir faixas a distância 1 ("quem ouviu X também ouviu Y") e
distância 2 ("quem ouviu quem ouviu X").
"""

try:
    from soundlab.fila import FilaExecucao
except ImportError:
    from fila import FilaExecucao


class GrafoRecomendacao:
    """Vértices: títulos de faixas. Arestas: coocorrência
    de reprodução em sequência."""

    def __init__(self):
        self._adjacencia = {}  # titulo -> set de titulos vizinhos

    def registrar_coocorrencia(self, titulo_a, titulo_b):
        if titulo_a.lower() == titulo_b.lower():
            return
        self._adjacencia.setdefault(titulo_a, set()).add(titulo_b)
        self._adjacencia.setdefault(titulo_b, set()).add(titulo_a)

    def recomendar(self, titulo, distancia_maxima=2):
        """Devolve os titulos alcancaveis a partir de 'titulo'
        em até 'distancia_maxima' saltos, usando BFS."""
        origem = None
        for chave in self._adjacencia:
            if chave.lower() == titulo.lower():
                origem = chave
                break

        if origem is None:
            return []

        fila = FilaExecucao()
        visitados = {origem}
        distancia = {origem: 0}
        recomendados = []

        fila.enfileirar(origem)

        while not fila.vazia():
            atual = fila.desenfileirar()
            dist_atual = distancia[atual]

            if dist_atual >= distancia_maxima:
                continue

            for vizinho in self._adjacencia.get(atual, set()):
                if vizinho not in visitados:
                    visitados.add(vizinho)
                    distancia[vizinho] = dist_atual + 1
                    recomendados.append(vizinho)
                    fila.enfileirar(vizinho)

        return recomendados
