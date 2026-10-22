"""
TAD Árvore Binária — Aula 08 aplicada ao SoundLab (Semana 2)

Árvore binária é uma estrutura não linear onde cada nó possui até
dois filhos: esquerda e direita. Nesta etapa, a árvore serve como
índice para percorrer o acervo de diferentes formas através dos três
percursos clássicos: pré-ordem, em-ordem e pós-ordem.
"""


class NodoArvore:
    def __init__(self, faixa):
        self.faixa = faixa
        self.esquerda = None
        self.direita = None


class ArvoreBinaria:
    def __init__(self):
        self._raiz = None

    def inserir(self, faixa):
        # Insere uma nova faixa na árvore por nível (ordem de chegada)
        novo = NodoArvore(faixa)
        if self._raiz is None:
            self._raiz = novo
            return

        # Procura o primeiro nó com vaga usando uma fila auxiliar
        fila = [self._raiz]
        while fila:
            atual = fila.pop(0)
            if atual.esquerda is None:
                atual.esquerda = novo
                return
            fila.append(atual.esquerda)

            if atual.direita is None:
                atual.direita = novo
                return
            fila.append(atual.direita)

    def pre_ordem(self):
        # Devolve lista em pré-ordem: nó, esquerda, direita
        resultado = []
        self._pre_ordem(self._raiz, resultado)
        return resultado

    def _pre_ordem(self, no, resultado):
        if no is not None:
            resultado.append(no.faixa)
            self._pre_ordem(no.esquerda, resultado)
            self._pre_ordem(no.direita, resultado)

    def em_ordem(self):
        # Devolve lista em em-ordem: esquerda, nó, direita
        resultado = []
        self._em_ordem(self._raiz, resultado)
        return resultado

    def _em_ordem(self, no, resultado):
        if no is not None:
            self._em_ordem(no.esquerda, resultado)
            resultado.append(no.faixa)
            self._em_ordem(no.direita, resultado)

    def pos_ordem(self):
        # Devolve lista em pós-ordem: esquerda, direita, nó
        resultado = []
        self._pos_ordem(self._raiz, resultado)
        return resultado

    def _pos_ordem(self, no, resultado):
        if no is not None:
            self._pos_ordem(no.esquerda, resultado)
            self._pos_ordem(no.direita, resultado)
            resultado.append(no.faixa)
