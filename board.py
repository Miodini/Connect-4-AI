import numpy as np

# Player 1 = Red
# Player 2 = Yellow

class Board:
    """Representa o tabuleiro e seus métodos de modificação/verificação."""
    def __init__(self, cells = None, nRows = 6, nCols = 7):
        """
        Parameters
        ----------
        cells: numpy.2darray, optional
            Valor inicial das células do tabuleirio. Se não fornecida, será criado um tabuleiro vazio.
            Deve ter as dimensões nRows x nCols.
        nRows: int, default 6
            Número de linhas do tabuleiro.
        nCols: int, default 7
            Número de colunas do tabuleiro.
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
        Caso a coluna esteja cheia, não altera o tabuleiro.
        
        Parameters
        ----------
        column: int
            Índice da coluna onde será inserido a ficha.
        currentPlayer: int
            Número representando o jogador atual (1 -> vermelho, 2 -> amarelo).
            
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

    def simDropChip(self, column, currentPlayer):
        """Procura a primeira posição livre (de baixo pra cima) na coluna 'column'.
        Retorna uma cópia de 'cells' com a posição encontrada ocupada pelo jogador 'currentPlayer'.
       
       Parameters
        ----------
        column: int
            Índice da coluna onde será inserido a ficha.
        currentPlayer: int
            Número representando o jogador atual (1 -> vermelho, 2 -> amarelo).
            
        Returns
        -------
        numpy.2darray | None
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
        """Procura se há algum ganhador no jogo. 
        
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
        """Calcula o total de fichas presentes no tabuleiro.
        
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

    def checkAlmostWin(self, aiChipNum):
        """Calcula os pontos em situação de quase vitória.
        Uma condição de quase vitória ocorre caso haja 3 fichas de mesmo cor em um grupo de 4 células na horizontal/vertical/horizontal.
        Quase vitórias para o jogador atual resultam em pontos positivos. Para o jogador adversário, resultam em pontos negativos.
        Caso haja mais de uma condição de quase vitória, a pontuação total é acumulada.
        
        Parameters
        ----------
        aiChipNum: int
            Número da ficha do jogador atual.
            
        Returns
        -------
        int
            Pontuação do jogador na rodada.
        """
        # 3 elementos na horizontal
        score = 0
        for i in range(self.nRows):
            aiChips = foeChips = 0
            for j in range(self.nCols - 3):
                if self.cells[i][j] != 0:
                    if self.cells[i][j] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i][j+1] != 0:
                    if self.cells[i][j+1] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i][j+2] != 0:
                    if self.cells[i][j+2] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i][j+3] != 0:
                    if self.cells[i][j+3] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if aiChips == 3:
                    score += 30
                elif foeChips == 3:
                    score -= 30

        # 3 elementos na vertical
        for i in range(self.nRows - 3):
            aiChips = foeChips = 0
            for j in range(self.nCols):
                if self.cells[i][j] != 0:
                    if self.cells[i][j] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i+1][j] != 0:
                    if self.cells[i+1][j] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i+2][j] != 0:
                    if self.cells[i+2][j] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i+3][j] != 0:
                    if self.cells[i+3][j] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if aiChips == 3:
                    score += 30
                elif foeChips == 3:
                    score -= 30


        # 3 elementos na diagonal
        for i in range(self.nRows - 3):
            aiChips = 0
            for j in range(self.nCols - 3):
                if self.cells[i][j] != 0:
                    if self.cells[i][j] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i+1][j+1] != 0:
                    if self.cells[i+1][j+1] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i+2][j+2] != 0:
                    if self.cells[i+2][j+2] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i+3][j+3] != 0:
                    if self.cells[i+3][j+3] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if aiChips == 3:
                    score += 30
                elif foeChips == 3:
                    score -= 30

        for i in range(3, self.nRows):
            aiChips = 0
            for j in range(self.nCols - 3):
                if self.cells[i][j] != 0:
                    if self.cells[i][j] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i-1][j+1] != 0:
                    if self.cells[i-1][j+1] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i-2][j+2] != 0:
                    if self.cells[i-2][j+2] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if self.cells[i-3][j+3] != 0:
                    if self.cells[i-3][j+3] == aiChipNum:
                        aiChips += 1
                    else:
                        foeChips += 1
                if aiChips == 3:
                    score += 30
                elif foeChips == 3:
                    score -= 30              
        return score

    def getFreeColumns(self):
        """Retorna as colunas que não estão cheias.
        
        Returns
        -------
        list[int]
        """
        indexes = []
        # Itera sobre as colunas
        for i, col in enumerate(list(np.transpose(self.cells))):
            if 0 in col:
                indexes.append(i)
        return indexes

    def getScore(self, isAIsTurn, aiChipNum, *, draw = False, win = False):
        """Função de utilidade (medida do quão bem a AI foi na partida)
        Parameters
        ----------
        isAIsTurn : bool
            Se True, é a vez do jogador 1. Se False, é a vez do jogador 2 (para determinar se a IA venceu ou perdeu)
        aiChipNum: int
            Número da ficha do jogador atual.
        draw: bool, optional
            Se True, significa que houve empate na rodada.
        win: bool, optional
            Se True, significa que houve vitória na rodada.
        Returns
        -------
        int
            Pontuação da função de utilidade (quanto maior, melhor)
        """
        score = 0
        # Se empate
        if draw:
            score += 0
        # Se a IA ganhou
        elif isAIsTurn and win:
            score += 1000
        # Se a IA perdeu
        elif not isAIsTurn and win:
            score -= 1000
        else:
            score += self.checkAlmostWin(aiChipNum)
        
        score -= self.getTotalChips()     # Quanto mais turnos tiver passado, menor a pontuação
        return score
