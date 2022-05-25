from time import sleep
import pygame

class Game:
    rowsNum = 6
    colsNum = 7
    def __init__(self, size):
        self.width, self.height = size
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((255, 255, 255))
        pygame.display.set_caption('Connect 4')

        self.board = []
        thickness = 2
        margin = 20
        for i in range(self.rowsNum):
            x = (((self.width - 2*margin)/ self.rowsNum) * i+1) + margin # Posicao de cada linha
            self.board.append(pygame.Rect(x, 100, thickness, 450))
        self.board.append(pygame.Rect(self.width - margin, 100, thickness, 450)) # Ultima linha
        for rect in self.board:
            self.screen.fill((128,0,0), rect)

jogo = Game((600, 600))
running = True
while running:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False