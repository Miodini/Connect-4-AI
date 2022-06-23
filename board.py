from numpy import transpose
import copy

class Board:
    def __init__(self, cells: list[list[str]] = None):
        self.nRows = 6      # Apenas para informação externa...
        self.nCols = 7      # ...não são usados internamente pela classe 
        if cells is None:
            self.cells = [
                ['0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0'],
                ['0', '0', '0', '0', '0', '0', '0']
            ]
        else:
            self.cells = cells
        
    def dropChip(self, column: int, currentPlayer: str):
        """
        Procura a primeira posição livre (de baixo pra cima) na coluna 'column'.
        Altera o atributo 'cells' para constar que a posição encontrada está ocupada pelo jogador 'currentPlayer'.
        Retorna o índice da posição ou None caso a coluna esteja cheia.
        """
        for i in range(-1, -len(self.cells[0]), -1):    # Itera de baixo pra cima
            if self.cells[i][column] == '0':
                self.cells[i][column] = currentPlayer
                return len(self.cells[0]) + i
        return None

    def simDropChip(self, column: int, currentPlayer: str):
        """
        Procura a primeira posição livre (de baixo pra cima) na coluna 'column'.
        Retorna o uma cópia de Board.cells (sem alterá-la) após a inserção da ficha
        ou None caso a coluna esteja cheia.
        """
        for i in range(-1, -len(self.cells[0]), -1):    # Itera de baixo pra cima
            if self.cells[i][column] == '0':
                newCell = copy.deepcopy(self.cells)
                newCell[i][column] = currentPlayer
                return newCell
        return None

    def checkWinner(self):
        """Procura se há algum ganhador. Retorna True se sim, False se não."""
        # 4 elementos na horizontal
        for row in self.cells[:]:
            s = ''.join(e for e in row)    # Converte a lista em string
            if 'vvvv' in s or 'yyyy' in s:
                return True
        # 4 elementos na vertical
        for col in list(transpose(self.cells[:])):
            s = ''.join(e for e in col)    # Converte a lista em string
            if 'vvvv' in s or 'yyyy' in s:
                return True
        # 4 elementos na diagonal
        diagIndexes = (
            # Direção nordeste-sudoeste
            ((0,3), (1,2), (2,1), (3,0)),
            ((0,4), (1,3), (2,2), (3,1), (4,0)),
            ((0,5), (1,4), (2,3), (3,2), (4,1), (5,0)),
            ((0,6), (1,5), (2,4), (3,3), (4,2), (5,1)),
            ((1,6), (2,5), (3,4), (4,3), (5,2)),
            ((2,6), (3,5), (4,4), (5,3)),
            # Direção noroeste-sudeste
            ((2,0), (3,1), (4,2), (5,3)),
            ((1,0), (2,1), (3,2), (4,3), (5,4)),
            ((0,0), (1,1), (2,2), (3,3), (4,4), (5,5)),
            ((0,1), (1,2), (2,3), (3,4), (4,5), (5,6)),
            ((0,2), (1,3), (2,4), (3,5), (4,6)),
            ((0,3), (1,4), (2,5), (3,6))
        )
        for quads in diagIndexes:
            s = ''.join(self.cells[e[0]][e[1]] for e in quads)     # Converte a lista em string
            if 'vvvv' in s or 'yyyy' in s:
                return True
        return False