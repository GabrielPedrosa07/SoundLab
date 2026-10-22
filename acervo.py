"""
TAD Acervo — a coleção de faixas do SoundLab.

Módulo 1 aplicado. O Acervo é o segundo TAD do projeto:

  Valores    : um conjunto de Faixas, em ordem de cadastro.
  Operações  : adicionar, buscar, remover, quantidade, percorrer.

A lista do Python é a representação interna e fica escondida atrás do
prefixo `_`. Nas Aulas 04 e 05 essa lista será substituída por estruturas
encadeadas — e nenhum código de fora do Acervo precisará mudar.
"""


class Acervo:
    """Coleção de faixas cadastradas no SoundLab."""

    def __init__(self):
        self._faixas = []

    def adicionar(self, faixa):
        """Insere no fim. Custo constante: nada é deslocado."""
        self._faixas.append(faixa)

    def buscar(self, titulo):
        """Devolve a faixa com o título dado, ou None.

        Percorre posição por posição: é a busca linear. No pior caso
        examina o acervo inteiro.
        """
        for faixa in self._faixas:
            if faixa.titulo.lower() == titulo.lower():
                return faixa
        return None

    def remover(self, titulo):
        """Remove e devolve a faixa com o título dado, ou None."""
        for posicao, faixa in enumerate(self._faixas):
            if faixa.titulo.lower() == titulo.lower():
                # pop(posicao) desloca UMA A UMA todas as faixas seguintes
                # para preencher o buraco. Remover do meio custa caro.
                return self._faixas.pop(posicao)
        return None

    def __len__(self):
        """Permite escrever len(acervo)."""
        return len(self._faixas)

    def __iter__(self):
        """Permite escrever `for faixa in acervo` sem expor a lista interna."""
        return iter(self._faixas)
