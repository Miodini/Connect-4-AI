from numpy import inf
from board import Board

# Faltam testes
class Tree():
    """Clase representando um nó de uma árvore de busca
    Implementa o algoritmo MINMAX com poda alfa beta.

    Attributes
    ----------
    children : list[object]
        Lista de objetos de Tree representando os filhos de cada nó
    board : object
    playerNumber : int
    _alpha : float
    _beta : float
    """
    def __init__(self, board: object, playerNumber: int, _alpha = -inf, _beta = inf):
        """
        Parameters
        ----------
        board : object
            Objeto da classe Board (importado de board.py) representando o estado atual do tabuleiro no nó.
        playerNumber : int
            Qual jogador (1 ou 2) que está associado a IA
        _alpha : float, optional
            O valor de alfa no algoritmo poda alfa beta. Utilizado para recursão, não deve ser atribuido fora da classe.
        _beta : float, optional
            O valor de beta no algoritmo poda alfa beta. Utilizado para recursão, não deve ser atribuido fora da classe.
        """
        self.children = []
        self.board = board
        self.playerNumber = playerNumber
        self.alpha = _alpha
        self.beta = _beta

    def genChildren(self, player1Turn: bool, minPlayer: bool):
        """Gera recursivamente uma nova instância da classe Tree e adiciona em sua lista de filhos
        Condição de parada é caso algum jogador tenha ganhado no turno

        Parameters
        ----------
        player1Turn : bool
            Se True, é a vez do jogador 1. Se False, é a vez do jogador 2
        minPlayer : bool
            Se True, é a vez do jogador MIN. Se False, é a vez do jogador MAX (algoritmo MINMAX)
        """
        score = None
        for i in range(self.board.nCols):
            cells = self.board.simDropChip(i, 'r' if player1Turn else 'y')

            # Empate (nó terminal)
            if cells is None:
                score = self.getScore(player1Turn, draw = True)
            else:
                newBoard = Board(cells)
                # Nó terminal
                if newBoard.checkWinner():
                    score = self.getScore(player1Turn)
                else:
                    newNode = Tree(newBoard, self.playerNumber)
                    self.children.append(newNode)
                    newScore = newNode.genChildren(not player1Turn, not minPlayer)    # Alterna entre os jogadores red e yellow
                    # MIN (primeira busca do nó) 
                    if score is None and minPlayer:
                        self.beta = score = newScore
                    # MAX (primeira busca do nó)
                    elif score is None and not minPlayer:
                        self.alpha = score = newScore
                    # MIN
                    elif newScore < score and minPlayer:
                        self.beta = score = newScore
                    # MAX
                    elif newScore > score and not minPlayer:
                        self.alfa = score = newScore
                # Poda
                if not minPlayer and self.beta < self.alpha:
                    break
            return score

    def getScore(self, player1Turn: bool, draw: bool = False):
        """Função de utilidade (medida do quão bem a AI foi na partida)
        Parameters
        ----------
        player1Turn : bool
            Se True, é a vez do jogador 1. Se False, é a vez do jogador 2 (para determinar se a IA venceu ou perdeu)

        draw : bool, optional
            Se True, significa que houve empate
        Returns
        -------
        int
            pontuação da função de utilidade (quanto maior, melhor)
        """
        # Se empate
        if draw:
            score = 100     # Pontuação inicial
        # Se a IA ganhou
        elif (self.playerNumber == 1 and player1Turn) or (self.playerNumber == 2 and not player1Turn):
            score = 300
        # Se a IA perdeu
        else:
            score = 0
        score -= self.board.getTotalChips()     # Quanto mais turnos tiver passado, menor a pontuação
        return score
 
board = Board()
root = Tree(board, 1)
root.genChildren(True, False)