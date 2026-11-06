"""
TAD Árvore Binária de Busca (ABB) — Aula 09 aplicada ao SoundLab (Semana 3)

Especializa a Árvore Binária da Semana 2 adicionando a regra de ordenação
por título: menores à esquerda, maiores à direita. O percurso em-ordem
herdado de ArvoreBinaria devolve automaticamente o acervo em ordem alfabética.
"""

try:
    from soundlab.arvore import ArvoreBinaria, NodoArvore
except ImportError:
    from arvore import ArvoreBinaria, NodoArvore


class ArvoreBinariaBusca(ArvoreBinaria):
    def inserir(self, faixa):
        # Insere ordenando pelo título (menor vai para esquerda, maior para direita)
        if self._raiz is None:
            self._raiz = NodoArvore(faixa)
        else:
            self._inserir_ordenado(self._raiz, faixa)

    def _inserir_ordenado(self, atual, faixa):
        if faixa.titulo.lower() < atual.faixa.titulo.lower():
            if atual.esquerda is None:
                atual.esquerda = NodoArvore(faixa)
            else:
                self._inserir_ordenado(atual.esquerda, faixa)
        else:
            if atual.direita is None:
                atual.direita = NodoArvore(faixa)
            else:
                self._inserir_ordenado(atual.direita, faixa)

    def buscar(self, titulo):
        # Desce a árvore comparando o título — O(log n) no caso médio
        return self._buscar_no(self._raiz, titulo.lower())

    def _buscar_no(self, atual, titulo_busca):
        if atual is None:
            return None

        titulo_atual = atual.faixa.titulo.lower()
        if titulo_busca == titulo_atual:
            return atual.faixa
        elif titulo_busca < titulo_atual:
            return self._buscar_no(atual.esquerda, titulo_busca)
        else:
            return self._buscar_no(atual.direita, titulo_busca)


ArvoreBusca = ArvoreBinariaBusca
