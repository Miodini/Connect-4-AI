import os
import pygame as pg

class Board:
    cells = [
        ['0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0'],
        ['0', '0', '0', '0', '0', '0', '0']
    ]

    def targetRow(self, column: int, currentPlayer: str):
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
                
class Game:
    player1Turn = True  # Player 1 == True: vermelho. Player 1 == False: amarelo
    _xMargin = 5        # Tamanho da margem entre o tabuleiro e a borda da janela (eixo X)
    _topMargin = 140    # Tamanho da margem entre o tabuleiro e a borda da janela (eixo Y, cima)
    _botMargin = 84     # Tamanho da margem entre o tabuleiro e a borda da janela (eixo Y, baixo)
    _cellSize = 84      # Tamanho de cada célula. O tabuleiro é dividido em 7 células horizontais e 6 verticais.
    _sArrowHeight = 22  # Altura do arquivo de imagem da seta pequena
    _lArrowHeight = 25  # Altura do arquivo de imagem da seta grande
    board = Board()     # Objeto contendo as informações e métodos do tabuleiro

    def __init__(self, size: tuple[int]):
        self.width, self.height = size
        pg.init()
        pg.display.set_caption('Connect 4')
        self.screen = pg.display.set_mode(size)
        self.screen.fill((255, 255, 255))

        boardImg = pg.image.load(os.path.join('img', 'board.png')).convert_alpha()
        self.screen.blit(boardImg, (self._xMargin, self._topMargin))

        self.arrowsPos = []
        self.yellowChipImg = pg.image.load(os.path.join('img', 'chip_y.png')).convert_alpha()
        self.redChipImg = pg.image.load(os.path.join('img', 'chip_r.png')).convert_alpha()
        self.smallArrowImg = pg.image.load(os.path.join('img', 'arrow_s.png')).convert_alpha()
        self.bigArrowImg = pg.image.load(os.path.join('img', 'arrow_l.png')).convert_alpha()
        for i in range(7):      # 7 colunas
            self.arrowsPos.append((i*self._cellSize + self._xMargin, 110))
            self.drawArrow(i, 'small')        

    def drawArrow(self, column: int, arrowType: str):
        """
        Desenha a uma flecha na coluna 'column'.
        'arrowType' deve ser "small" ou "big" para uma flecha pequena ou grande
        """
        xPos = self.arrowsPos[column][0]
        yPos = self.arrowsPos[column][1]
        blankRect = pg.Rect(xPos, yPos, self._cellSize, self._lArrowHeight)
        pg.draw.rect(self.screen, (255, 255, 255), blankRect)   # Limpa a flecha antiga
        if arrowType == 'small':
            self.screen.blit(self.smallArrowImg, (xPos + 10, yPos)) # Cada flecha pequena é 10px menor que cada célula em cada lado
        elif arrowType == 'big':
            self.screen.blit(self.bigArrowImg, (xPos, yPos)) # Cada flecha pequena é 10px menor que cada célula em cada lado

    def checkMouseCollision(self):
        """ 
        Verifica se o mouse está sobreposto a caixa de colisão de alguma das setas de inserção de ficha.
        Se sim, redesenha a seta sobreposta para uma maior, muda o cursor para "mão" e retorna a coluna da seta (começando em 0).
        Se não, muda o cursor para flecha e retorna None.
        """
        arrowsDownRightPos = list(map(lambda t: (t[0] + self._cellSize, t[1] + self._sArrowHeight), self.arrowsPos)) # Calcula a posição inferior direita de cada flecha
    
        mousePos = pg.mouse.get_pos()
        hovering = None    # Para determinar se o cursor deve mudar ou não
        for i in range(len(self.arrowsPos)):
            if mousePos[0] > self.arrowsPos[i][0] and mousePos[1] > self.arrowsPos[i][1] and mousePos[0] < arrowsDownRightPos[i][0] and mousePos[1] < arrowsDownRightPos[i][1]:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                hovering = i
                self.drawArrow(i, 'big')
            else:
                self.drawArrow(i, 'small')
        if hovering == None: 
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)
        return hovering

    def dropChip(self, column):
        """
        Insere uma ficha na coluna 'column' na linha vazia mais a baixo.
        Não faz nada se não tiver espaço vazio na coluna.
        Muda o jogador atual e chama o método de reescrever o texto.
        """
        positionInserted = self.board.targetRow(column, 'v' if self.player1Turn else 'y')
        if positionInserted != None:
            self.screen.blit(
                self.redChipImg if self.player1Turn else self.yellowChipImg,
                (self._xMargin + (self._cellSize * column), self._topMargin + (self._cellSize * positionInserted) - self._botMargin)
            )
            self.player1Turn = not self.player1Turn     # Troca o jogador atual
            self.genText()

    def genText(self):
        """Limpa a parte superior da tela e escreve o texto de jogador da vez"""
        font = pg.font.Font(None, 48)
        blankRect = pg.Rect(0, 0, self.width, self._topMargin)
        pg.draw.rect(self.screen, (255, 255, 255), blankRect)
        if self.player1Turn:
            playerName = 'vermelho'
            color = (145, 17, 17)
        else:
            playerName = 'amarelo'
            color = (200, 209, 23)

        text = f'Vez do jogador {playerName}.'
        textBox = font.render(text, True, color, (255, 255, 255))
        textSize = font.size(f'Vez do jogador {playerName}.')
        self.screen.blit(textBox, (self.width/2 - textSize[0]/2, self._topMargin/2 - textSize[1]))

    def start(self):
        """Inicia a rotina de jogo e mantém o controle dos eventos"""
        running = True
        self.genText()
        while running:
            hoveredArrow = self.checkMouseCollision()
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if hoveredArrow != None and event.type == pg.MOUSEBUTTONUP:
                    self.dropChip(hoveredArrow)

jogo = Game((600, 700))
jogo.start()