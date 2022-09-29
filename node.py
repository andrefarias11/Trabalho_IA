
class Node:

    __slots__ = ['current_board', 'parent_board', 'heuristic_value', 'total_cost']

    def __init__(self, cb, pb, hv, tc):
        """
        :param cb: atual tabuleiro
        :param pb: tabuleiro pai
        :param hv: valor heurístico
        :param tc: custo total
        """
        self.current_board = cb
        self.parent_board = pb
        self.heuristic_value = hv
        self.total_cost = tc
