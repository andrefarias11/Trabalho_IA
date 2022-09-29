from copy import copy, deepcopy
from sys import getsizeof
from tabuleiro import *
import globals
import psutil
import time
import os
from heapq import *


def move_up(valor_hp, quadro_pai, at_quadro, pontoVazio, pq, visitado):
  
    """
    :param pq: fila prioritária utilizada para anexar novos estados (se necessário)
    :param valor_hp: Tem o valor heurístico dos pais
    :param quadro_pai: Mantém o quadro de pais
    :param at_quadro: Mantém o quadro atual do filho a ser avaliado
    :param pontoVazio: Mantém as coordenadas de onde se encontra a posição vazia
    :return:
    """
    if pontoVazio[0] - 1 >= 0:

        tmp = at_quadro[pontoVazio[0] - 1][pontoVazio[1]]
        at_quadro[pontoVazio[0] - 1][pontoVazio[1]] = at_quadro[pontoVazio[0]][pontoVazio[1]]
        at_quadro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(at_quadro)

        check_hm(tabuleiro(cb_as_list),
                 ' '.join(str(num) for linha in quadro_pai for num in linha),
                 valor_hp, pq, visitado)


def move_down(valor_hp, quadro_pai, at_quadro, pontoVazio, pq, visitado):

    if pontoVazio[0] + 1 < EDGE_LENGTH:
        tmp = at_quadro[pontoVazio[0] + 1][pontoVazio[1]]
        at_quadro[pontoVazio[0] + 1][pontoVazio[1]] = at_quadro[pontoVazio[0]][pontoVazio[1]]
        at_quadro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(at_quadro)

        check_hm(tabuleiro(cb_as_list),
                 ' '.join(str(num) for linha in quadro_pai for num in linha),
                 valor_hp, pq, visitado)


def move_left(valor_hp, quadro_pai, at_quadro, pontoVazio, pq, visitado):

    if pontoVazio[1] - 1 >= 0:

        tmp = at_quadro[pontoVazio[0]][pontoVazio[1] - 1]
        at_quadro[pontoVazio[0]][pontoVazio[1] - 1] = at_quadro[pontoVazio[0]][pontoVazio[1]]
        at_quadro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(at_quadro)

        check_hm(tabuleiro(cb_as_list),
                 ' '.join(str(num) for linha in quadro_pai for num in linha),
                 valor_hp, pq, visitado)


def move_right(valor_hp, quadro_pai, at_quadro, pontoVazio, pq, visitado):

    if pontoVazio[1] + 1 < EDGE_LENGTH:

        tmp = at_quadro[pontoVazio[0]][pontoVazio[1] + 1]
        at_quadro[pontoVazio[0]][pontoVazio[1] + 1] = at_quadro[pontoVazio[0]][pontoVazio[1]]
        at_quadro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(at_quadro)

        check_hm(tabuleiro(cb_as_list),
                 ' '.join(str(num) for linha in quadro_pai for num in linha),
                 valor_hp, pq, visitado)


def check_hm(b, parent, ph, pq, visitado):
    """
    Verifica se o novo quadro (depois de subir, descer, esquerda, ou direita) já foi visitado.
    Se não foi, acrescenta à fila de prioridade.
    """

    h = 0
    filho = ' '.join(str(e) for e in b.tabuleiro_as_string_list)

    if filho not in visitado.keys():
        pq.append((h, b.tabuleiro_as_string_list))
        visitado[filho] = [h, h + ph, parent]


def get_path(tabuleiro, visitado):

    if tabuleiro == 'NULL':
        return
    else:
        get_path(visitado[tabuleiro][2], visitado)
        b = tabuleiro(tabuleiro.split(' '))
        b.print_tabuleiro()
        print('')


def bfs(start_tabuleiro):
    """
    o quadro de partida contém o quadro actual
    Retorna verdadeiro ou falso (se uma solução foi encontrada em 15 segundos
    """
    pq = []
    visitado = {}

    b = tabuleiro(start_tabuleiro)
    h = 0

    cb_as_list = b.tabuleiro_as_string_list
    visitado[' '.join(str(e) for e in cb_as_list)] = [h, h, 'NULL']

    pq.append((h, cb_as_list))

    curr_max = 0

    curr_time = time.time()

    while len(pq) != 0:

        if (time.time() - curr_time) * 1000 > 30000:
            print('Não foi encontrado uma solução em 15 segundos para o quadro inicial')
            break
        no = pq.pop(0)
        if getsizeof(pq) > curr_max:
            curr_max = getsizeof(pq)

        # no[0] == 0 or (use for next project, put that or cond in if cond
        if no[1] == GOAL_STATE_15_AS_ILIST or no[1] == GOAL_STATE_15_AS_SLIST:
            get_path(GOAL_STATE_15, visitado)
            print('*** Solução encontrada usando BFS!                       ***')
            print('*** O Caminho da Solução foi impresso. ***')

            process = psutil.Process(os.getpid())
            memory = process.memory_info().rss
            memory_bfs = memory / 1000000

            globals.memory_bfs = memory_bfs
            print('BFS Árvore de tamanho atingida ', curr_max / 1048576)
            visitado.clear()
            return True

        # pega o tabuleiro como MATRIX
        at_quadro = transform_to_matrix(no[1])

        # procura o ponto vazio
        pontoVazio = find_zero(at_quadro)

        # no[0] pega o valor da heuristica,
        # at_quadro é o tabuleiro actual,
        # deepcopy(at_quadro) é o tabuleiro actual.
        # pontoVazio é a posição do ponto vazio
        move_up(no[0], at_quadro, deepcopy(at_quadro), pontoVazio, pq, visitado)
        move_down(no[0], at_quadro, deepcopy(at_quadro), pontoVazio, pq, visitado)
        move_left(no[0], at_quadro, deepcopy(at_quadro), pontoVazio, pq, visitado)
        move_right(no[0], at_quadro, deepcopy(at_quadro), pontoVazio, pq, visitado)

    return False
