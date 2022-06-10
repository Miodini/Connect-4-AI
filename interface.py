import os
import pygame as pg
from numpy import transpose

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY =  (190, 190, 190)
RED = (145, 17, 17)
YELLOW = (200, 209, 23)

class Board:
    def __init__(self):
        self.cells = [
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

class Game:
    _xMargin = 5        # Tamanho da margem entre o tabuleiro e a borda da janela (eixo X)
    _topMargin = 140    # Tamanho da margem entre o tabuleiro e a borda da janela (eixo Y, cima)
    _botMargin = 84     # Tamanho da margem entre o tabuleiro e a borda da janela (eixo Y, baixo)
    _cellSize = 84      # Tamanho de cada célula. O tabuleiro é dividido em 7 células horizontais e 6 verticais.
    player1Turn = True  # Player 1 == True: vermelho. Player 1 == False: amarelo
    gameOver = False
    board = Board()     # Objeto contendo as informações e métodos do tabuleiro

    def __init__(self, size: tuple[int]):
        pg.init()
        pg.display.set_caption('Connect 4')
        self.screen = pg.display.set_mode(size)
        self.screen.fill(WHITE)

        self.width, self.height = size
        self.turns = 0
        self.imgs = {
            'board': pg.image.load(os.path.join('img', 'board.png')).convert_alpha(),       # Tabuleiro
            'sArrow': pg.image.load(os.path.join('img', 'arrow_s.png')).convert_alpha(),    # Seta pequenoa
            'lArrow': pg.image.load(os.path.join('img', 'arrow_l.png')).convert_alpha(),    # Seta grande
            'yChip': pg.image.load(os.path.join('img', 'chip_y.png')).convert_alpha(),      # Ficha amarela
            'rChip': pg.image.load(os.path.join('img', 'chip_r.png')).convert_alpha()       # Ficha vermelha
        }
        self.rects = {
            'sArrows': [],   # Pequeno
            'lArrows': [],    # Grande
            'rstButtom': None
        }

        self.screen.blit(self.imgs['board'], (self._xMargin, self._topMargin))
        for i in range(7):      # 7 colunas
            self.rects['sArrows'].append(pg.Rect(i*self._cellSize + self._xMargin + 10, 110, self.imgs['sArrow'].get_width(), self.imgs['sArrow'].get_height()))
            self.rects['lArrows'].append(pg.Rect(i*self._cellSize + self._xMargin, 110, self.imgs['lArrow'].get_width(), self.imgs['lArrow'].get_height()))
            self.drawArrow(i, 'small')        

    def drawArrow(self, column: int, arrowType: str):
        """
        Desenha a uma flecha na coluna 'column'.
        'arrowType' deve ser "small" ou "big" para uma flecha pequena ou grande
        """
        # Diferença das dimensões das flechas grandes e pequenas nas duas dimensões
        pg.draw.rect(self.screen, WHITE, self.rects['lArrows'][column])   # Limpa a flecha antiga
        if arrowType == 'small':
            self.screen.blit(self.imgs['sArrow'], self.rects['sArrows'][column]) 
        elif arrowType == 'big':
            self.screen.blit(self.imgs['lArrow'], self.rects['lArrows'][column])

    def checkMouseCollision(self):
        """ 
        Verifica se o mouse está sobreposto a caixa de colisão de alguma das setas de inserção de ficha.
        Se sim, redesenha a seta sobreposta para uma maior, muda o cursor para "mão" e retorna a coluna da seta (começando em 0).
        Se não, muda o cursor para flecha e retorna None.
        """
        mousePos = pg.mouse.get_pos()
        hovering = {'arrow': None, 'reset': False}    # Para determinar se o cursor deve mudar ou não
        # Setas
        for [i, arrow] in enumerate(self.rects['sArrows']):
            if arrow.collidepoint(mousePos):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                hovering['arrow'] = i
                self.drawArrow(i, 'big')
            else:
                self.drawArrow(i, 'small')
        # Botão de reset
        if self.gameOver:
            if self.rects['rstButtom'].collidepoint(mousePos):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
                hovering['reset'] = True

        if hovering['arrow'] == None and not hovering['reset']: 
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
            self.turns += 1
            self.screen.blit(
                self.imgs['rChip'] if self.player1Turn else self.imgs['yChip'],
                (self._xMargin + (self._cellSize * column), self._topMargin + (self._cellSize * positionInserted) - self._botMargin)
            )
            if self.board.checkWinner():
                mode = 'win'
                self.gameOver = True
            elif self.turns >= 42:
                mode = 'draw'
                self.gameOver = True
            else:
                mode = 'turn'    
                self.player1Turn = not self.player1Turn     # Troca o jogador atual
            self.genText(mode)
            

    def genText(self, mode: str):
        """
        Limpa a parte superior da tela e escreve o texto informativo na tela
        'mode' = "turn" | "win" | "draw"
        Para os modos win e draw, também gera um botão de reiniciar jogo
        """
        font = pg.font.Font(None, 48)
        blankRect = pg.Rect(0, 0, self.width, self._topMargin)
        pg.draw.rect(self.screen, WHITE, blankRect)
        if self.player1Turn:
            playerName = 'vermelho'
            color = RED
        else:
            playerName = 'amarelo'
            color = YELLOW
        
        if mode == 'turn':
            text = f'Vez do jogador {playerName}.'
            textSize = font.size(f'Vez do jogador {playerName}.')
        else:
            # Botão de reset
            rstFont = pg.font.Font(None, 36)
            rstText = 'Reiniciar'
            rstTextSize = rstFont.size('Reiniciar')
            rstTextBox = rstFont.render(rstText, True, BLACK, LIGHT_GRAY)
            self.rects['rstButtom'] = pg.Rect(
                self.width/2 - rstTextSize[0]/2,
                self._topMargin/2 - rstTextSize[1] + 25,
                rstTextSize[0],
                rstTextSize[1]
            )
            if mode == 'win': 
                text = f'Vitória do jogador {playerName}!'
                textSize = font.size(f'Vitória do jogador {playerName}!')
            elif mode == 'draw':
                text = 'Empate!'
                textSize = font.size('Empate!')
                color = BLACK
            self.screen.blit(rstTextBox, self.rects['rstButtom'])

        textBox = font.render(text, True, color, WHITE)
        self.screen.blit(textBox, (self.width/2 - textSize[0]/2, self._topMargin/2 - textSize[1]))

    def start(self):
        """Inicia a rotina de jogo e mantém o controle dos eventos"""
        running = True
        self.genText('turn')
        while running:
            hovering = self.checkMouseCollision()
            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.MOUSEBUTTONUP and hovering['arrow'] != None and not self.gameOver:
                    self.dropChip(hovering['arrow'])
                if event.type == pg.MOUSEBUTTONUP and hovering['reset']:
                    self.restart()
    
    def restart(self):
        """Retorna o jogo ao estado inicial"""
        self.gameOver = False
        self.player1Turn = True
        self.turns = 0
        self.board = Board()    # Limpar o tabuleiro == criar outro
        self.screen.fill(WHITE)
        self.screen.blit(self.imgs['board'], (self._xMargin, self._topMargin))
        self.genText('turn')

jogo = Game((600, 700))
jogo.start()