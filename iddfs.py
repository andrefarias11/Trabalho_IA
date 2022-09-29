"""
Busca em Profundidade.
"""


import os
import time
import psutil
import globals
from tabuleiro import *
from copy import deepcopy


def move_tabuleiro(direction, node, visitado):
    """
    :param direction: direcao para onde o vazio vai se mover
    :param node: no atual
    :param visitado: listas de nos visitados
    :return: novo no 
    """

    cb_as_list = node[0]
    parent_tabuleiro = node[1]
    pontoVazio = node[2]
    curr_tabuleiro = deepcopy(parent_tabuleiro)
    passed = False

    if direction == "UP" and pontoVazio[0] - 1 >= 0:
        passed = True
        tmp = curr_tabuleiro[pontoVazio[0] - 1][pontoVazio[1]]
        curr_tabuleiro[pontoVazio[0] - 1][pontoVazio[1]] = curr_tabuleiro[pontoVazio[0]][pontoVazio[1]]
        curr_tabuleiro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(curr_tabuleiro)

    elif direction == "DOWN" and pontoVazio[0] + 1 < EDGE_LENGTH:
        passed = True
        tmp = curr_tabuleiro[pontoVazio[0] + 1][pontoVazio[1]]
        curr_tabuleiro[pontoVazio[0] + 1][pontoVazio[1]] = curr_tabuleiro[pontoVazio[0]][pontoVazio[1]]
        curr_tabuleiro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(curr_tabuleiro)

    elif direction == "LEFT" and pontoVazio[1] - 1 >= 0:
        passed = True
        tmp = curr_tabuleiro[pontoVazio[0]][pontoVazio[1] - 1]
        curr_tabuleiro[pontoVazio[0]][pontoVazio[1] - 1] = curr_tabuleiro[pontoVazio[0]][pontoVazio[1]]
        curr_tabuleiro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(curr_tabuleiro)

    elif direction == "RIGHT" and pontoVazio[1] + 1 < EDGE_LENGTH:
        passed = True
        tmp = curr_tabuleiro[pontoVazio[0]][pontoVazio[1] + 1]
        curr_tabuleiro[pontoVazio[0]][pontoVazio[1] + 1] = curr_tabuleiro[pontoVazio[0]][pontoVazio[1]]
        curr_tabuleiro[pontoVazio[0]][pontoVazio[1]] = tmp
        cb_as_list = transform_to_string_list(curr_tabuleiro)

    del curr_tabuleiro[:]
    del curr_tabuleiro

    #Se passou por uma das condições do if-elif, verificar se o quadro foi visitado.
    #Se não foi visitado, adicionar à lista de visitados e retornar o novo quadro.
    #Se foi visitado, retornar None.
    #Se não passou por nenhuma das condições do if-elif, retornar None.
    if passed:
        result = check_hm(tabuleiro(cb_as_list), ' '.join(str(num) for row in parent_tabuleiro for num in row), visitado)
    else:
        return 'NULL'

    if result:
        return cb_as_list
    else:
        return 'NULL'


def check_hm(b, parent, visitado):
    """
    :param b: tabuleiro

    :param parent: tabuleiro pai
    :param visitado: lista de nos visitados
    :return: True se o tabuleiro não foi visitado
    """

    child = ' '.join(str(e) for e in b.tabuleiro_as_string_list)
    if child not in visitado.keys():
        visitado[child] = parent
        return True
    return False


def get_path(tabuleiro, visitado):
    """
    :param tabuleiro: tabuleiro
    :param visitado: lista de nos visitados
    :return:caminho do tabuleiro inicial ao tabuleiro final
    """

    if tabuleiro == 'NULL':
        return
    else:
        get_path(visitado[tabuleiro], visitado)
        b = tabuleiro(tabuleiro.split(' '))
        b.print_tabuleiro()
        print('')


def iddfs(start_tabuleiro):
    """
    :param start_tabuleiro: tabuleiro inicial
    :return:caminho do tabuleiro inicial ao tabuleiro final
    """

    visitado = {}
    curr_time = time.time()
    depth = 0

    while True:

        if (time.time() - curr_time) * 1000 > 15000:
            print('Desculpe... Não foi encontrado uma solução em 15 segundos usando IDDFS... Terminando o programa.')
            break

        b = tabuleiro(start_tabuleiro)
        cb_as_list = b.tabuleiro_as_string_list
        visitado[' '.join(str(e) for e in cb_as_list)] = 'NULL'

        if dls(start_tabuleiro, depth, visitado):
            get_path(GOAL_STATE_15, visitado)
            print('*** Solução usando Busca em Profundidade                     ***')
            return True

        depth += 1
        visitado.clear()

    return False


def dls(atual_tabuleiro, depth, visitado):
    """
    :param atual_tabuleiro: tabuleiro atual
    :param depth:   profundidade
    :param visitado: lista de nos visitados
    :return:True se o tabuleiro final foi encontrado
    """

    b = tabuleiro(atual_tabuleiro)

    cb_as_list = b.tabuleiro_as_string_list

    if cb_as_list == GOAL_STATE_15_AS_ILIST or cb_as_list == GOAL_STATE_15_AS_SLIST:
        return True

    if depth <= 0:
        return False

    # pega e trasnforma o tabuleiro atual em matriz
    curr_tabuleiro = transform_to_matrix(cb_as_list)

    # busca o ponto vazio
    pontoVazio = find_zero(curr_tabuleiro)

    up_result = move_tabuleiro("Cima", [cb_as_list, curr_tabuleiro, pontoVazio], visitado)
    down_result = move_tabuleiro("Baixo", [cb_as_list, curr_tabuleiro, pontoVazio], visitado)
    left_result = move_tabuleiro("Esquerda", [cb_as_list, curr_tabuleiro, pontoVazio], visitado)
    right_result = move_tabuleiro("Direita", [cb_as_list, curr_tabuleiro, pontoVazio], visitado)

    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss
    memory_iddfs = memory / 1000000
    globals.memory_iddfs = memory_iddfs

    if up_result != "NULL":
        if dls(up_result, depth - 1, visitado):
            return True
    if down_result != "NULL":
        if dls(down_result, depth - 1, visitado):
            return True
    if left_result != 'NULL':
        if dls(left_result, depth - 1, visitado):
            return True
    if right_result != 'NULL':
        if dls(right_result, depth - 1, visitado):
            return True

    return False
