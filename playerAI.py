from math import inf
from board import Board
import random

MAX_DEPTH = 4
def minimax(board: object):
    # Raíz sempre será o jogador MAX
    score = -inf
    alpha = -inf
    beta = inf
    bestPlay = 0
    freeCols = board.getFreeColumns()
    # Empate -> Interrompe a busca
    if len(freeCols) == 0:
        return board.getScore(True, draw = True)

    bestPlay = random.choice(freeCols)
    for i in freeCols:
        cells = board.simDropChip(i, 1)
        newBoard = Board(cells)
        newScore = _minimaxRecursion(newBoard, 0, True, alpha, beta)    # IA é o player 2
        # MAX
        if newScore > score:
            score = newScore
            bestPlay = i
        alpha = max(alpha, score)
        # Poda
        if beta < alpha:
            break
    return bestPlay

def _minimaxRecursion(board: object, depth: int, isAIsTurn: bool, alpha: float, beta: float):
    ## Condições de parada
    # Vitória de alguém -> Interrompe a busca
    if board.checkWinner():
        return board.getScore(isAIsTurn, win = True)

    freeCols = board.getFreeColumns()
    # Empate -> Interrompe a busca
    if len(freeCols) == 0:
        return board.getScore(isAIsTurn, draw = True)
    # Nível máximo de recursão atingido
    if depth == MAX_DEPTH:
        return board.getScore(isAIsTurn)

    score = -inf
    for i in freeCols:
        cells = board.simDropChip(i, 1 if isAIsTurn else 2)
        newBoard = Board(cells)
        newScore = _minimaxRecursion(newBoard, depth + 1, not isAIsTurn, alpha, beta)    # Alterna entre os jogadores red e yellow
        
        # Jogador MAX
        if isAIsTurn: 
            if newScore > score:
                score = newScore
            alpha = max(alpha, score)
        # Jogador MIN
        else:
            if newScore < score:
                score = newScore
            beta = min(beta, score)
        # Poda
        if beta < alpha:
            break

    return score