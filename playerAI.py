import sys
from board import Board

sys.setrecursionlimit(100000)
class Tree():
    def __init__(self, board: any):
        self.board = board
        self.children = []

    def genChildren(self, player1Turn: bool):
        # A árvore gerada é extremamente longa. Aplicar o algoritmo de poda antes de tentar construir
        for i in range(self.board.nCols):
            cells = board.simDropChip(i, 'r' if player1Turn else 'y')
            if cells is not None:
                newBoard = Board(cells)
                if not newBoard.checkWinner():
                    newNode = Tree(newBoard)
                    newNode.genChildren(not player1Turn)    # Alterna entre os jogadores red e yellow
                    self.children.append(newNode)

board = Board()
root = Tree(board)
root.genChildren(True)