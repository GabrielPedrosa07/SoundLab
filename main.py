"""
SoundLab — versão 11 (Aula 11 / Semana 5).

O SoundLab agora compara na prática o número de comparações da Busca Linear
O(n) contra a Busca Binária O(log n) aplicada sobre a lista ordenada obtida
pelo percurso em-ordem da ABB (Semana 3).

    python main.py
"""

try:
    from soundlab.acervo import Acervo
    from soundlab.faixa import Faixa
    from soundlab.fila import FilaExecucao
    from soundlab.pilha import Pilha
    from soundlab.playlist import Playlist
    from soundlab.arvore import ArvoreBinaria
    from soundlab.arvore_busca import ArvoreBinariaBusca
    from soundlab.grafo import GrafoRecomendacao
    from soundlab.busca import busca_linear_contada, busca_binaria_contada
except ImportError:
    from acervo import Acervo
    from faixa import Faixa
    from fila import FilaExecucao
    from pilha import Pilha
    from playlist import Playlist
    from arvore import ArvoreBinaria
    from arvore_busca import ArvoreBinariaBusca
    from grafo import GrafoRecomendacao
    from busca import busca_linear_contada, busca_binaria_contada

OPCOES = """
+------------------- SoundLab -------------------+
 1  Listar acervo           7  Inserir na playlist (posicao)
 2  Cadastrar faixa         8  Tirar da playlist (posicao)
 3  Buscar por titulo       9  Comecar reproducao (playlist)
 4  Remover do acervo      10  Proxima faixa da playlist (>>)
 5  Ver playlist           11  Faixa anterior da playlist (<<)
 6  Acrescentar a playlist
                           12  Tocar faixa do acervo (historico)
                           13  Desfazer reproducao (historico)

                           14  Adicionar a fila (a seguir)
                           15  Tocar proxima da fila
                           16  Alternar modo repeticao
                           17  Ver fila a seguir

                           18  Ver percursos da arvore
                           19  Buscar por titulo (ABB)
                           20  Listar ordem alfabetica (ABB)
                           21  Recomendar a partir de faixa
                           22  Comparar buscas (Linear vs Binaria)
 0  Sair
+------------------------------------------------+"""


def carregar_acervo():
    acervo = Acervo()
    acervo.adicionar(Faixa("Aquarela do Brasil", "Ary Barroso", 245))
    acervo.adicionar(Faixa("Construcao", "Chico Buarque", 382))
    acervo.adicionar(Faixa("Ponta de Areia", "Milton Nascimento", 194))
    acervo.adicionar(Faixa("Baiao", "Luiz Gonzaga", 168))
    acervo.adicionar(Faixa("Trem das Onze", "Adoniran Barbosa", 175))
    acervo.adicionar(Faixa("Garota de Ipanema", "Tom Jobim", 210))
    return acervo


def registrar_sequencia(faixa, grafo, estado):
    anterior = estado["ultima"]
    if anterior is not None and anterior.titulo != faixa.titulo:
        grafo.registrar_coocorrencia(anterior.titulo, faixa.titulo)
    estado["ultima"] = faixa


def listar(acervo):
    if len(acervo) == 0:
        print("  acervo vazio")
    for posicao, faixa in enumerate(acervo):
        print(f"  [{posicao}] {faixa}")


def cadastrar(acervo):
    titulo = input("  titulo...: ").strip()
    artista = input("  artista..: ").strip()
    acervo.adicionar(Faixa(titulo, artista, int(input("  duracao (s): "))))
    print(f"  cadastrada. o acervo tem {len(acervo)} faixas.")


def buscar(acervo):
    faixa = acervo.buscar(input("  titulo: ").strip())
    print(f"  {faixa}" if faixa else "  nao encontrada")


def remover(acervo):
    faixa = acervo.remover(input("  titulo: ").strip())
    print(f"  removida: {faixa}" if faixa else "  nao encontrada")


def ver_playlist(playlist):
    print(f"  playlist '{playlist.nome}' ({len(playlist)} faixas)")
    for posicao, faixa in enumerate(playlist):
        print(f"    {posicao}. {faixa}")


def acrescentar(acervo, playlist):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    playlist.adicionar(faixa)
    print(f"  '{faixa.titulo}' entrou no fim da playlist")


def inserir(acervo, playlist):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    posicao = int(input(f"  posicao (0 a {len(playlist)}): "))
    playlist.inserir_em(posicao, faixa)
    print(f"  '{faixa.titulo}' inserida na posicao {posicao}")


def tirar(playlist):
    posicao = int(input(f"  posicao (0 a {len(playlist) - 1}): "))
    print(f"  saiu: {playlist.remover_em(posicao)}")


def comecar(playlist, grafo=None, estado=None):
    faixa = playlist.comecar_reproducao()
    faixa.tocar()
    if grafo is not None and estado is not None:
        registrar_sequencia(faixa, grafo, estado)
    print(f"  tocando: {faixa}")


def proxima(playlist, grafo=None, estado=None):
    faixa = playlist.proxima()
    faixa.tocar()
    if grafo is not None and estado is not None:
        registrar_sequencia(faixa, grafo, estado)
    print(f"  tocando: {faixa}")


def anterior(playlist, grafo=None, estado=None):
    faixa = playlist.anterior()
    faixa.tocar()
    if grafo is not None and estado is not None:
        registrar_sequencia(faixa, grafo, estado)
    print(f"  tocando: {faixa}")


def tocar_agora(acervo, historico, grafo=None, estado=None):
    """Toca uma faixa direto do acervo, fora da ordem da playlist.

    Cada chamada empilha uma faixa nova: o topo do historico passa a
    ser "o que esta tocando agora".
    """
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    faixa.tocar()
    historico.empilhar(faixa)
    if grafo is not None and estado is not None:
        registrar_sequencia(faixa, grafo, estado)
    print(f"  tocando agora: {faixa}")


def desfazer_reproducao(historico):
    """Desempilha a faixa atual e revela a que tocava antes dela —
    exatamente o oposto de tocar_agora."""
    if historico.vazia():
        print("  nada no historico")
        return
    atual = historico.desempilhar()
    print(f"  saindo de: {atual}")
    if historico.vazia():
        print("  historico vazio - nada tocando")
    else:
        print(f"  voltando a tocar: {historico.topo()}")


def enfileirar_faixa(acervo, fila):
    faixa = acervo.buscar(input("  titulo: ").strip())
    if faixa is None:
        print("  nao esta no acervo")
        return
    fila.enfileirar(faixa)
    print(f"  '{faixa.titulo}' entrou na fila a seguir")


def tocar_proxima_fila(fila, grafo=None, estado=None):
    faixa = fila.desenfileirar()
    faixa.tocar()
    if grafo is not None and estado is not None:
        registrar_sequencia(faixa, grafo, estado)
    print(f"  tocando da fila: {faixa}")


def alternar_repeticao(fila):
    fila.repeticao = not fila.repeticao
    status = "ativado" if fila.repeticao else "desativado"
    print(f"  modo repeticao {status}")


def ver_fila(fila):
    status = "ativado" if fila.repeticao else "desativado"
    print(f"  fila a seguir ({len(fila)} faixas) [repeticao: {status}]")
    if fila.vazia():
        print("    fila vazia")
        return
    for posicao, faixa in enumerate(fila):
        print(f"    {posicao}. {faixa}")


def ver_percursos_arvore(acervo):
    if len(acervo) == 0:
        print("  acervo vazio")
        return

    arvore = ArvoreBinaria()
    for faixa in acervo:
        arvore.inserir(faixa)

    pre = [f.titulo for f in arvore.pre_ordem()]
    em = [f.titulo for f in arvore.em_ordem()]
    pos = [f.titulo for f in arvore.pos_ordem()]

    print("\n  Percursos da Arvore Binaria (Indice do Acervo):")
    print(f"  {'PRE-ORDEM':<26} | {'EM-ORDEM':<26} | {'POS-ORDEM':<26}")
    print("  " + "-" * 82)

    total = max(len(pre), len(em), len(pos))
    for i in range(total):
        p = pre[i] if i < len(pre) else ""
        e = em[i] if i < len(em) else ""
        po = pos[i] if i < len(pos) else ""
        print(f"  {p:<26} | {e:<26} | {po:<26}")
    print("  " + "-" * 82)


def montar_abb(acervo):
    abb = ArvoreBinariaBusca()
    for faixa in acervo:
        abb.inserir(faixa)
    return abb


def buscar_abb(acervo):
    abb = montar_abb(acervo)
    titulo = input("  titulo: ").strip()
    faixa = abb.buscar(titulo)
    print(f"  {faixa}" if faixa else "  nao encontrada")


def listar_alfabetica_abb(acervo):
    if len(acervo) == 0:
        print("  acervo vazio")
        return
    abb = montar_abb(acervo)
    ordenadas = abb.em_ordem()
    print("  acervo em ordem alfabetica (ABB em-ordem):")
    for posicao, faixa in enumerate(ordenadas, start=1):
        print(f"    {posicao}. {faixa}")


def recomendar_faixas(acervo, grafo):
    titulo = input("  titulo: ").strip()
    faixa = acervo.buscar(titulo)
    if faixa is None:
        print("  nao esta no acervo")
        return
    sugestoes = grafo.recomendar(faixa.titulo)
    if not sugestoes:
        print(f"  nenhuma recomendacao para '{faixa.titulo}' ainda")
        return
    print(f"  quem ouviu '{faixa.titulo}' tambem ouviu:")
    for pos, sugerida in enumerate(sugestoes, start=1):
        print(f"    {pos}. {sugerida}")


def comparar_buscas(acervo):
    if len(acervo) == 0:
        print("  acervo vazio")
        return

    lista_linear = list(acervo)
    # Lista ordenada obtida a partir do em_ordem() da ABB da Semana 3
    abb = montar_abb(acervo)
    lista_ordenada = abb.em_ordem()

    # Seleciona pelo menos 5 titulos variados (inicio, meio, fim e um inexistente)
    titulos_teste = [f.titulo for f in lista_linear]
    titulos_teste.append("Faixa Inexistente")

    print(f"\n  Comparacao de Buscas no Acervo ({len(lista_linear)} faixas):")
    print(f"  {'TITULO BUSCADO':<26} | {'ACHADO':<8} | {'LINEAR O(n)':<13} | {'BINARIA O(log n)':<16}")
    print("  " + "-" * 72)

    for titulo in titulos_teste:
        faixa_lin, comp_lin = busca_linear_contada(lista_linear, titulo)
        faixa_bin, comp_bin = busca_binaria_contada(lista_ordenada, titulo)
        achado = "Sim" if faixa_bin is not None else "Nao"
        print(f"  {titulo:<26} | {achado:<8} | {comp_lin:<13} | {comp_bin:<16}")

    print("  " + "-" * 72)
    print("  Interpretacao:")
    print("  - A busca linear O(n) percorre faixa por faixa, chegando a examinar o acervo")
    print("    inteiro nos elementos do fim ou quando o titulo nao existe.")
    print("  - A busca binaria O(log n), aplicada sobre a lista ordenada do em_ordem() da ABB,")
    print("    descarta metade das faixas a cada passo, exigindo no maximo 3 comparacoes.")
    print("  - Em um acervo pequeno a diferenca absoluta e pequena, mas conforme o acervo")
    print("    cresce (ex: 100 ou 1000 faixas), o ganho de O(log n) sobre O(n) se torna enorme.")


def main():
    acervo = carregar_acervo()
    playlist = Playlist("Favoritas")
    historico = Pilha()
    fila = FilaExecucao()
    grafo = GrafoRecomendacao()
    estado = {"ultima": None}

    while True:
        print(OPCOES)
        opcao = input(" opcao: ").strip()
        try:
            if opcao == "0":
                print(" ate a proxima.")
                break
            elif opcao == "1": listar(acervo)
            elif opcao == "2": cadastrar(acervo)
            elif opcao == "3": buscar(acervo)
            elif opcao == "4": remover(acervo)
            elif opcao == "5": ver_playlist(playlist)
            elif opcao == "6": acrescentar(acervo, playlist)
            elif opcao == "7": inserir(acervo, playlist)
            elif opcao == "8": tirar(playlist)
            elif opcao == "9": comecar(playlist, grafo, estado)
            elif opcao == "10": proxima(playlist, grafo, estado)
            elif opcao == "11": anterior(playlist, grafo, estado)
            elif opcao == "12": tocar_agora(acervo, historico, grafo, estado)
            elif opcao == "13": desfazer_reproducao(historico)
            elif opcao == "14": enfileirar_faixa(acervo, fila)
            elif opcao == "15": tocar_proxima_fila(fila, grafo, estado)
            elif opcao == "16": alternar_repeticao(fila)
            elif opcao == "17": ver_fila(fila)
            elif opcao == "18": ver_percursos_arvore(acervo)
            elif opcao == "19": buscar_abb(acervo)
            elif opcao == "20": listar_alfabetica_abb(acervo)
            elif opcao == "21": recomendar_faixas(acervo, grafo)
            elif opcao == "22": comparar_buscas(acervo)
            else: print("  opcao invalida")
        except (ValueError, IndexError) as erro:
            print(f"  {erro}")


if __name__ == "__main__":
    main()
