"""
TAD Faixa — a menor unidade de informação do SoundLab.

Módulo 1 aplicado. O TAD declara:

  Valores    : título, artista, duração em segundos, número de execuções.
  Operações  : tocar(), duracao_formatada().

Quem usa a Faixa não precisa saber que a duração é guardada em segundos.
Essa é a ideia central de tipo abstrato de dados: o contrato é público,
a representação é detalhe interno.
"""


class Faixa:
    """Uma música do acervo."""

    def __init__(self, titulo, artista, duracao_seg):
        self.titulo = titulo
        self.artista = artista
        self.duracao_seg = duracao_seg
        self.execucoes = 0

    def tocar(self):
        """Registra mais uma execução. Na Aula 12 este número vira critério
        de ordenação do ranking."""
        self.execucoes += 1

    def duracao_formatada(self):
        """Converte a representação interna (segundos) para o formato que o
        usuário entende (minutos:segundos)."""
        minutos = self.duracao_seg // 60
        segundos = self.duracao_seg % 60
        return f"{minutos}:{segundos:02d}"

    def __str__(self):
        return f"{self.titulo} - {self.artista} ({self.duracao_formatada()})"
