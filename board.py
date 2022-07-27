import numpy as np

# Player 1 = Red
# Player 2 = Yellow

class Board:
    def __init__(self, cells = None, nRows: int = 6, nCols: int = 7):
        """
        Parameters
        ----------
        cells : list[list[str]], optional
            Valor inicial das células do tabuleirio. Se não fornecida, será criado um tabuleiro vazio
        """
        self.nRows = nRows 
        self.nCols = nCols  
        if cells is None:
            self.cells = np.zeros((nRows, nCols), dtype=np.int8)
        else:
            self.cells = cells
        
    def dropChip(self, column, currentPlayer):
        """Procura a primeira posição livre (de baixo pra cima) na coluna 'column'.
        Altera o atributo 'cells' para constar que a posição encontrada está ocupada pelo jogador 'currentPlayer'.

        Returns
        -------
        int | None
            Índice da posição ou None caso a coluna esteja cheia.
        """
        # Coluna cheia
        if self.cells[0][column] != 0:
            return None
        for i in range(-1, -self.nRows - 1, -1):    # Itera de baixo pra cima
            if self.cells[i][column] == 0:
                self.cells[i][column] = currentPlayer
                return self.nRows + 1 + i

    def simDropChip(self, column: int, currentPlayer: str):
        """Procura a primeira posição livre (de baixo pra cima) na coluna 'column'.
        
        Returns
        -------
        tuple | None
            Retorna uma cópia de Board.cells (sem alterá-la) após a inserção da ficha ou None caso a coluna esteja cheia.
        """
        for i in range(-1, -self.nRows - 1, -1):    # Itera de baixo pra cima
            if self.cells[i][column] == 0:
                # Realiza uma deep copy de self.cells
                tempList = []
                for row in self.cells:
                    newRow = [e for e in row]
                    tempList.append(newRow)
                tempList[i][column] = currentPlayer
                
                return tuple(tempList)
        return None

    def checkWinner(self):
        """Procura se há algum ganhador. 
        
        Returns
        -------
        bool
            True se houve algum ganhador, False se não.
        """
        # 4 elementos na horizontal
        for i in range(self.nRows):
            for j in range(self.nCols - 3):
                if self.cells[i][j] == self.cells[i][j+1] == self.cells[i][j+2] == self.cells[i][j+3] and self.cells[i][j] != 0:
                    return True
        # 4 elementos na vertical
        for i in range(self.nRows - 3):
            for j in range(self.nCols):
                if self.cells[i][j] == self.cells[i+1][j] == self.cells[i+2][j] == self.cells[i+3][j] and self.cells[i][j] != 0:
                    return True
        # 4 elementos na diagonal
        for i in range(self.nRows - 3):
            for j in range(self.nCols - 3):
                if self.cells[i][j] == self.cells[i+1][j+1] == self.cells[i+2][j+2] == self.cells[i+3][j+3] and self.cells[i][j] != 0:
                    return True
        for i in range(3, self.nRows):
            for j in range(self.nCols - 3):
                if self.cells[i][j] == self.cells[i-1][j+1] == self.cells[i-2][j+2] == self.cells[i-3][j+3] and self.cells[i][j] != 0:
                    return True
        return False

    def getTotalChips(self):
        """
        Returns
        -------
        int
            Quantidade de fichas presentes no tabuleiro.
        """
        total = 0
        for row in self.cells:
            for cell in row:
                if cell != 0:
                    total += 1
        return total

    def checkAlmostWin(self, chipNum):
        # Calcula os pontos em situação de quase vitória
        # 3 elementos na horizontal
        score = 0
        for i in range(self.nRows):
            chips = 0
            for j in range(self.nCols - 3):
                if self.cells[i][j] == chipNum:
                    chips += 1
                if self.cells[i][j+1] == chipNum:
                    chips += 1
                if self.cells[i][j+2] == chipNum:
                    chips += 1
                if self.cells[i][j+3] == chipNum:
                    chips += 1
                if chips == 3:
                   # Analizando jogada da IA
                    if chipNum == 2:
                        score += 30
                    # Analizando jogada do humano
                    else:
                        score -= 30

        # 3 elementos na vertical
        for i in range(self.nRows - 3):
            chips = 0
            for j in range(self.nCols):
                if self.cells[i][j] == chipNum:
                    chips += 1
                if self.cells[i+1][j] == chipNum:
                    chips += 1
                if self.cells[i+2][j] == chipNum:
                    chips += 1
                if self.cells[i+3][j] == chipNum:
                    chips += 1
                if chips == 3:
                   # Analizando jogada da IA
                    if chipNum == 2:
                        score += 30
                    # Analizando jogada do humano
                    else:
                        score -= 30

        # 3 elementos na diagonal
        for i in range(self.nRows - 3):
            chips = 0
            for j in range(self.nCols - 3):
                if self.cells[i][j] == chipNum:
                    chips += 1
                if self.cells[i+1][j+1] == chipNum:
                    chips += 1
                if self.cells[i+2][j+2] == chipNum:
                    chips += 1
                if self.cells[i+3][j+3] == chipNum:
                    chips += 1
                if chips == 3:
                   # Analizando jogada da IA
                    if chipNum == 2:
                        score += 30
                    # Analizando jogada do humano
                    else:
                        score -= 30

        for i in range(3, self.nRows):
            chips = 0
            for j in range(self.nCols - 3):
                if self.cells[i][j] == chipNum:
                    chips += 1
                if self.cells[i-1][j+1] == chipNum:
                    chips += 1
                if self.cells[i-2][j+2] == chipNum:
                    chips += 1
                if self.cells[i-3][j+3] == chipNum:
                    chips += 1
                if chips == 3:
                   # Analizando jogada da IA
                    if chipNum == 2:
                        score += 30
                    # Analizando jogada do humano
                    else:
                        score -= 30              
        return score

    def getFreeColumns(self):
        indexes = []
        # Itera sobre as colunas
        for i, col in enumerate(list(np.transpose(self.cells))):
            if 0 in col:
                indexes.append(i)
        return indexes

    def getScore(self, isAIsTurn: bool, *, draw: bool = False, win: bool = False):
        """Função de utilidade (medida do quão bem a AI foi na partida)
        Parameters
        ----------
        isAIsTurn : bool
            Se True, é a vez do jogador 1. Se False, é a vez do jogador 2 (para determinar se a IA venceu ou perdeu)

        draw : bool, optional
            Se True, significa que houve empate
        Returns
        -------
        int
            pontuação da função de utilidade (quanto maior, melhor)
        """
        score = 0
        # Se empate
        if draw:
            score += 100
        # Se a IA ganhou
        elif isAIsTurn and win:
            score += 1000
        # Se a IA perdeu
        elif not isAIsTurn and win:
            score -= 1000
        else:
            score += self.checkAlmostWin(2 if isAIsTurn else 1)
        
        score -= self.getTotalChips()     # Quanto mais turnos tiver passado, menor a pontuação
        return score