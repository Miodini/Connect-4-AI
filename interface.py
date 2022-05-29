import os
from tokenize import String
import pygame as pg

class Game:
    player1Turn = True
    _margin = 5         # Tamanho da margem entre o tabuleiro e a borda da janela
    _cellSize = 84      # Tamanho de cada célula. O tabuleiro é dividido em 7 células horizontais e 6 verticais.
    _sArrowHeight = 22  # Altura do arquivo de imagem da seta pequena
    _lArrowHeight = 25  # Altura do arquivo de imagem da seta grande

    def __init__(self, size):
        self.width, self.height = size
        pg.init()
        pg.display.set_caption('Connect 4')
        self.screen = pg.display.set_mode(size)
        self.screen.fill((255, 255, 255))

        board = pg.image.load(os.path.join('img', 'board.png')).convert_alpha()
        self.screen.blit(board, (self._margin, 140))

        self.arrowsPos = []
        self.smallArrowImg = pg.image.load(os.path.join('img', 'arrow_s.png')).convert_alpha()
        self.bigArrowImg = pg.image.load(os.path.join('img', 'arrow_l.png')).convert_alpha()
        for i in range(7):      # 7 colunas
            self.arrowsPos.append((i*self._cellSize + self._margin, 110))
            self.drawArrow(i, 'small')        

    def drawArrow(self, i, arrowType):
        xPos = self.arrowsPos[i][0]
        yPos = self.arrowsPos[i][1]
        blankRect = pg.Rect(xPos, yPos, self._cellSize, self._lArrowHeight)
        pg.draw.rect(self.screen, (255, 255, 255), blankRect)   # Limpa a flecha antiga
        if arrowType == 'small':
            self.screen.blit(self.smallArrowImg, (xPos + 10, yPos)) # Cada flecha pequena é 10px menor que cada célula em cada lado
        elif arrowType == 'big':
            self.screen.blit(self.bigArrowImg, (xPos, yPos)) # Cada flecha pequena é 10px menor que cada célula em cada lado

    def waitInput(self):
        pass

    def checkMouseCollision(self):
        arrowsDownRightPos = list(map(lambda t: (t[0] + self._cellSize, t[1] + self._sArrowHeight), self.arrowsPos)) # Calcula a posição inferior direita de cada flecha
    
        mousePos = pg.mouse.get_pos()
        hovering = False    # Para determinar se o cursor deve mudar ou não
        for i in range(len(self.arrowsPos)):
            if mousePos[0] > self.arrowsPos[i][0] and mousePos[1] > self.arrowsPos[i][1] and mousePos[0] < arrowsDownRightPos[i][0] and mousePos[1] < arrowsDownRightPos[i][1]:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                hovering = True
                self.drawArrow(i, 'big')
            else:
                self.drawArrow(i, 'small')
        if hovering == False: 
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

    def start(self):
        running = True
        while running:
            self.checkMouseCollision()
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

jogo = Game((600, 700))
jogo.start()