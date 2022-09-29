from copy import deepcopy
from sys import getsizeof
from board import transform_to_string_list
from constants import EDGE_LENGTH, GOAL_STATE_15_AS_ILIST
from quadro import *
import globals
import psutil
import time
import os
from heapq import *


def moverCima(valor_hp, quadro_pai, at_quadro, pontoVazio, pq, visitado):
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

        check_hm(quadro(cb_as_list),
                 ' '.join(str(num) for row in quadro_pai for num in row),
                 valor_hp, pq, visitado)


def moverBaixo(valor_hp, quadro_pai, at_quadro, pontoVazio, pq, visitado):
    if pontoVazio[0] + 1 < EDGE_LENGTH:
        tmp = at_quadro[pontoVazio[0] + 1][pontoVazio[1]]
        at_quadro[pontoVazio[0] + 1][pontoVazio[1]] = at_quadro[pontoVazio[0]][pontoVazio[1]]
        at_quadro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(at_quadro)

        check_hm(quadro(cb_as_list),
                 ' '.join(str(num) for row in quadro_pai for num in row),
                 valor_hp, pq, visitado)


def moverEsquerda(valor_hp, quadro_pai, at_quadro, pontoVazio, pq, visitado):
    if pontoVazio[1] - 1 >= 0:

        tmp = at_quadro[pontoVazio[0]][pontoVazio[1] - 1]
        at_quadro[pontoVazio[0]][pontoVazio[1] - 1] = at_quadro[pontoVazio[0]][pontoVazio[1]]
        at_quadro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(at_quadro)

        check_hm(quadro(cb_as_list),
                 ' '.join(str(num) for row in quadro_pai for num in row),
                 valor_hp, pq, visitado)


def moverDireita(valor_hp, quadro_pai, at_quadro, pontoVazio, pq, visitado):
    if pontoVazio[1] + 1 < EDGE_LENGTH:

        tmp = at_quadro[pontoVazio[0]][pontoVazio[1] + 1]
        at_quadro[pontoVazio[0]][pontoVazio[1] + 1] = at_quadro[pontoVazio[0]][pontoVazio[1]]
        at_quadro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(at_quadro)

        check_hm(quadro(cb_as_list),
                 ' '.join(str(num) for row in quadro_pai for num in row),
                 valor_hp, pq, visitado)


def check_hm(b, parent, ph, pq, visitado):

    if HEURISTIC == 'H':
        h = b.heuristica()
    else:
        h = b.peca_deslocada()
    filho = ' '.join(str(e) for e in b.quadro_as_string_list)

    if filho not in visitado.keys():
        heappush(pq, (h, b.quadro_as_string_list))
        visitado[filho] = [h, h + ph, parent]
    elif filho in visitado:
        if h + visitado[parent][1] < visitado[filho][1]:
            visitado[filho][1] = h + visitado[parent][1]
            heappush(pq, (h, b.quadro_as_string_list))


def get_path(quadro, visitado):

    if quadro == 'NULL':
        return
    else:
        get_path(visitado[quadro][2], visitado)
        b = quadro(quadro.split(' '))
        b.print_quadro()
        print('')
        if HEURISTIC == 'H':
            heur = str(b.heuristica())
        else:
            heur = str(b.peca_deslocada())
        print('Heuristic Valor: ' + heur + '\n')


def a_star(quadro_init, heuristic):
    """
    :param quadro_init: O quadro inicial contém o quadro atual
    :param heuristic: mostrar se é  heurística ou nao
    :return: Retorna verdadeiro ou falso   
    """
    pq = []
    visitado = {}
    global HEURISTIC

    HEURISTIC = heuristic
    b = quadro(quadro_init)

    if HEURISTIC == 'H':
        h = b.heuristica()
    else:
        h = b.peca_deslocada()

    cb_as_list = b.quadro_as_string_list
    visitado[' '.join(str(e) for e in cb_as_list)] = [h, h, 'NULL']

    heappush(pq, (h, cb_as_list))
    curr_max = 0

    curr_time = time.time()

    while len(pq) != 0:

        if (time.time() - curr_time) * 1000 > 30000:
            print('Não foi encontrado uma solução em 15 segundos para o quadro inicial') 
            break
        no = heappop(pq)

        if getsizeof(pq) > curr_max:
            curr_max = getsizeof(pq)

        if no[1] == GOAL_STATE_15_AS_ILIST or no[1] == GOAL_STATE_15_AS_SLIST:
            get_path(GOAL_STATE_15, visitado)

            if HEURISTIC == 'H':
                heur = 'Heuristic'
            else:
                heur = 'Heurística de Quadrado Deslocados'

            print('*** Solução encontrada usando  ', heur, ' A*!     ***')

            process = psutil.Process(os.getpid())
            memory = process.memory_info().rss
            memory_bfs = memory / 1000000
            globals.memory_bfs = memory_bfs

            print('*** Os valores heurísticos são impressos para cada estado   ***'
                  '\n*** Heurística utilizada: ', heur, '              ***'
                  '\n*** Algoritmo de busca Utilizado: Primeira busca da amplitude      ***')
            print('Arvore atingida ', curr_max / 1048576, 'MB')
            visitado.clear()
            return True

        # transformar a lista em uma matrix
        at_quadro = transform_to_matrix(no[1])

        # buscar o ponto vazio
        pontoVazio = find_zero(at_quadro)

        # no[0] holds the parent's heuristic, 
        # at_quadro contém o quadro numa matriz
        # deepcopy(at_quadro)
        # pontoVazio é a posição do ponto vazio
        moverCima(no[0], at_quadro, deepcopy(at_quadro), pontoVazio, pq, visitado)
        moverBaixo(no[0], at_quadro, deepcopy(at_quadro), pontoVazio, pq, visitado)
        moverEsquerda(no[0], at_quadro, deepcopy(at_quadro), pontoVazio, pq, visitado)
        moverDireita(no[0], at_quadro, deepcopy(at_quadro), pontoVazio, pq, visitado)

    print('Não foi encontrado uma solução para o quadro inicial');

    return False
