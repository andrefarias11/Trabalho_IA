from constants import *

class Board(object):
    __slots__ = ['board_as_string_list', 'current_board']

    def __init__(self, cb):
        self.board_as_string_list = cb
        self.current_board = transform_to_matrix(self.board_as_string_list)

    def get_board(self):
        return self.current_board

    def print_board(self):
        for row in self.current_board:
            print(row)

    def manhattan_heuristic(self):
        total_heuristic = 0
        for row in range(0, EDGE_LENGTH):
            for col in range(0, EDGE_LENGTH):
                if self.current_board[row][col] != 0:
                    target_x = (self.current_board[row][col] - 1) / EDGE_LENGTH
                    target_y = (self.current_board[row][col] - 1) % EDGE_LENGTH
                else:
                    target_x = EDGE_LENGTH - 1
                    target_y = EDGE_LENGTH - 1
                total_heuristic += int(abs(row - target_x) + abs(col - target_y))

        return total_heuristic

    def displaced_tiles_heuristic(self):
        total_heuristic = 0
        for row in range(0, EDGE_LENGTH):
            for col in range(0, EDGE_LENGTH):
                if self.current_board[row][col] != 0:
                    target_x = (self.current_board[row][col] - 1) / EDGE_LENGTH
                    target_y = (self.current_board[row][col] - 1) % EDGE_LENGTH
                else:
                    continue
                if row != int(target_x) or col != int(target_y):
                    total_heuristic += 1
        return total_heuristic


def transform_to_matrix(bas):
    cb = list(map(int, bas))
    w, h = EDGE_LENGTH, EDGE_LENGTH
    matrix = [[0 for x in range(w)] for y in range(h)]
    i = 0

    for row in range(0, w):
        for col in range(0, h):
            matrix[row][col] = cb[i]
            i += 1
    return matrix


def transform_to_string_list(matrix):
    tmp = []

    for r in range(0, EDGE_LENGTH):
        for c in range(0, EDGE_LENGTH):
            tmp.append(str(matrix[r][c]))
    return tmp


def find_zero(board):
    for r in range(0, EDGE_LENGTH):
        for c in range(0, EDGE_LENGTH):
            if board[r][c] == 0:
                return r, c
