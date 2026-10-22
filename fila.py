"""
TAD Fila - Aula 07 aplicada ao SoundLab (Semana 1)

Fila é uma estrutura linear com duas extremidades: entrada pelo fim
e saída pela frente (FIFO - First In, First Out).
O primeiro elemento a entrar é o primeiro a ser atendido/tocado.

No SoundLab a Fila gerencia as faixas "a seguir":
as faixas tocam na ordem em que foram enfileiradas.
Também implementamos a FilaCircular para o modo repetição,
onde a faixa que acabou de tocar volta para o fim da fila.
"""


class No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class FilaExecucao:
    """Fila de reprodução (FIFO): a próxima faixa a tocar
    é sempre a que está há mais tempo esperando."""

    def __init__(self, repeticao=False):
        self._frente = None
        self._tras = None
        self._tamanho = 0
        self.repeticao = repeticao

    def enfileirar(self, faixa):
        # Insere um novo nó no fim da fila (_tras),
        # religando _tras e, se a fila estava vazia, _frente.
        novo = No(faixa)
        if self.vazia():
            self._frente = novo
            self._tras = novo
        else:
            self._tras.proximo = novo
            self._tras = novo
        self._tamanho += 1

    def desenfileirar(self):
        # Remove e devolve o valor do nó na frente da fila;
        # se a fila ficar vazia, religa _tras para None.
        if self.vazia():
            raise IndexError("fila vazia")

        no = self._frente
        self._frente = no.proximo
        if self._frente is None:
            self._tras = None
        self._tamanho -= 1

        # Modo repetição: recicla a faixa colocando-a de volta no fim
        if self.repeticao:
            self.enfileirar(no.valor)

        return no.valor

    def vazia(self):
        return self._tamanho == 0

    def __len__(self):
        return self._tamanho

    def __iter__(self):
        atual = self._frente
        while atual is not None:
            yield atual.valor
            atual = atual.proximo


class FilaCircular(FilaExecucao):
    """Subclasse de FilaExecucao para o modo de repetição:
    ao desenfileirar uma faixa, ela é automaticamente reenfileirada no fim."""

    def __init__(self):
        super().__init__(repeticao=True)

    def desenfileirar(self):
        return super().desenfileirar()
