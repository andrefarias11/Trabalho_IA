
from __future__ import print_function
from iddfs import iddfs, nr_iddfs
from random import shuffle
from board import *
from bfs import bfs
from a_star import a_star
import globals
import psutil
import time
import gc
import os


def intro():
    print('use : 1 2 3 4 5 6 7 8 13 9 12 15 0 11 10 14\n')
    print('copie a linha de cima e cole aqui')
    return input("por favor insira o tabuleiro inicial: ")


def check_input(user_input):
    """
    :param user_input: Determinado pelo usuario
    """

    if user_input == 'r' or user_input == 'R':
        return True

    check_against = GOAL_STATE_15_AS_SLIST
    user_input = user_input.split(" ")

    if len(user_input) != 16:
        return False
    for num in check_against:
        if num not in user_input:
            return False
    return True


def randomize_board ():
    """
    :return: é o quadro utilizado para iniciar o programa, shuffles board é o utilizador pressiona 'r'
    """

    users_board = GOAL_STATE_15_AS_SLIST
    return shuffle(users_board)


def print_board(users_board):
    board = ""
    count = 0
    for num in users_board:
        if count % EDGE_LENGTH == 0 and count != 0:
            board += '\n'
        if len(num) == 1:
            if num == '0':
                board += '   '
            else:
                board += num + '  '
        else:
            board += num + ' '
        count += 1
    print(board)


def main():
    """
    Principal é a função utilizada para executar/ dirigir o programa.
    :return:
    """

    user_input = intro()
    users_board = -999
    is_valid = check_input(user_input)
    if is_valid:
        if user_input == 'r' or user_input == 'R':
            users_board = randomize_board()
        else:
            users_board = user_input.split(' ')
        print('Entrada de dados bem sucedida. Resolução do tabuleiro..')
        print('Seu tabuleiro: ')
        print_board(users_board)
    else:
        print('entrada de dados inválida')
        exit(0)

    print('Tempo para resolver usando bfs.\n\n')

    process = psutil.Process(os.getpid())
    memory = process.memory_info().rss
    memory_main = memory / 1000000

    globals.memory_main = memory_main

    # bfs tempo
    bfs_start_time = time.time()
    bfs(users_board)
    bfs_time = time.time() - bfs_start_time
    gc.collect()

    # iddfs tempo
    iddfs_start_time = time.time()
    iddfs(users_board)
    iddfs_time = time.time() - iddfs_start_time
    gc.collect()

    nr_iddfs_start_time = time.time()
    nr_iddfs(users_board)
    nr_iddfs_time = time.time() - nr_iddfs_start_time
    gc.collect()

    # Heuristic usando A*
    manhattan_astar_start_time = time.time()
    a_star(users_board, 'M')
    manhattan_astar_time = time.time() - manhattan_astar_start_time
    gc.collect()

    # quadrados deslocados Heurísticos utilizados com A*
    displaced_astar_start_time = time.time()
    a_star(users_board, 'D')
    displaced_astar_time = time.time() - displaced_astar_start_time
    gc.collect()

    # 1 2 3 4 5 6 7 8 13 9 12 15 0 11 10 14
    # 1 2 3 4 5 6 7 8 0 9 10 15 13 14 12 11

    print('Tempo para resolver usando bfs: ' + str(bfs_time) + ' segundos')
    print('Tempo para resolver usando iddfs: ' + str(iddfs_time) + ' segundos')
    print('Tempo para resolver usando nr_iddfs: ' + str(nr_iddfs_time) + ' segundos')
    print('Tempo para resolver usando A*: ' + str(a_star_time) + ' segundos') 



if __name__ == "__main__":
    main()
