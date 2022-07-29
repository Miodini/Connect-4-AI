from math import inf
from board import Board
import random

MAX_DEPTH = 4
def minimax(board: object, aiChipNum: int):
    """Função minimax com poda alfa e beta para cálculo da melhor jogada. 
    Refere-se a raíz da árvore. Chama _minimaxRecursio() para cálculo do restante dos ramos.
    
    Parameters
    ----------
    board: object
        Um objeto da classe Board representando o estado inicial do tabuleiro.
    aiChipNum: 1|2
        Número da ficha da IA (1 -> vermelho, 2 -> amarelo).
        
    Returns
    -------
    int
        Coluna onde deve ser inserido a ficha para a melhor jogada calculada.
    """
    # Raíz sempre será o jogador MAX
    score = -inf
    alpha = -inf
    beta = inf
    if aiChipNum == 1:
        otherChipNum = 2
    else:
        otherChipNum = 1
    freeCols = board.getFreeColumns()
   
    # Empate -> Interrompe a busca
    if len(freeCols) == 0:
        return board.getScore(True, draw = True)

    bestPlay = random.choice(freeCols)
    for i in freeCols:
        cells = board.simDropChip(i, aiChipNum)
        newBoard = Board(cells)
        newScore = _minimaxRecursion(newBoard, 0, True, alpha, beta, aiChipNum, otherChipNum)    # IA é o player 2
        # MAX
        if newScore > score:
            score = newScore
            bestPlay = i
        alpha = max(alpha, score)
        # Poda
        if beta < alpha:
            break
    return bestPlay

def _minimaxRecursion(board: object, depth: int, isAIsTurn: bool, alpha: float, beta: float, aiChipNum: int, otherChipNum: int):
    """Função recursiva para o cálculo da melhor jogada
    
    Parameters
    ----------
    board: object
        Um objeto da classe Board representando o estado inicial do tabuleiro.
    depth: int
        Profundidade atual da árvore.
    isAIsTurn: bool
        True se o estado atual equivaler à jogada da IA (MAX).
        O valor inverte no meio da função pois a jogada em si só começa após as verificações das condições de parada.
    alpha: float
        Valor de alfa da poda alfa-beta.
    beta: float
        Valor de beta da poda alfa-beta.
    aiChipNum: 1|2
        Número da ficha da IA (1 -> vermelho, 2 -> amarelo).
    otherChipNum: 1|2
        Número da ficha do adversário da IA (1 se aiChipNum == 2, 2 se aiChipNum == 1).
    """
    ## Condições de parada ##########################
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
    #################################################
    isAIsTurn = not isAIsTurn   # Troca de jogador para simular a proxima jogada
    if isAIsTurn:   # MAX
        score = -inf
    else:           # MIN
        score = inf
    for i in freeCols:
        cells = board.simDropChip(i, aiChipNum if isAIsTurn else otherChipNum)
        newBoard = Board(cells)
        newScore = _minimaxRecursion(newBoard, depth + 1, isAIsTurn, alpha, beta, aiChipNum, otherChipNum)    # Alterna entre os jogadores red e yellow
        
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
