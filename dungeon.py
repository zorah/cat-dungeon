import math
import numpy as np
import pygame
from pygame.locals import *

class Dungeon():

    _goal = pygame.image.load("fish.png")
    _heal = pygame.image.load("milk.png")
    _counter = 0

    def __init__(self, window, block_size, game_size):
        self._window = window
        self._block_size = block_size
        self._game_size = game_size
        self.reset()

    def reset(self):
        self.map = np.random.randint(2, size=(self._game_size, self._game_size))
        # set goal
        self._finish = self.randomPosition()
        self.map[self._finish[0], self._finish[1]] = 2
        for i in range(2):
            milk = self.randomPosition()
            self.map[milk[0], milk[1]] = 3

    def drawDungeon(self):
        # draw map
        for y in range(self._game_size):
            for x in range(self._game_size):
                if self.map[x,y] == 0:
                    color = (50, 50, 50)
                else:
                    color = (200, 200, 200)
                rect = pygame.Rect(x*(self._block_size), (y+1)*(self._block_size), self._block_size, self._block_size)
                pygame.draw.rect(self._window, color, rect)
                if self.map[x,y] == 3:
                    self._window.blit(self._heal, (x*self._block_size, (y + 1)*self._block_size))
        # draw goal
        self._window.blit(self._goal, (self._finish[0]*self._block_size, (self._finish[1] + 1)*self._block_size))
        # write text
        # write new name
        myfont = pygame.font.SysFont('Arial', 16)
        textsurface = myfont.render('Dungeon ' + str(self._counter), False, (10, 10, 10))
        self._window.blit(textsurface,(10*self._block_size, 0))

    def validatePosition(self, posX, posY):
        if posX >= 0 and posX < self._game_size and posY >= 0 and posY < self._game_size:
            if not (self.map[posX, posY] == 0):
                return True
        return False

    def validateGoal(self, posX, posY):
        if posX >= 0 and posX < self._game_size and posY >= 0 and posY < self._game_size:
            if (self.map[posX, posY] == 2):
                return True
        return False

    def randomPosition(self):
        found = False
        while not found:
            position = np.random.randint(self._game_size, size=2)
            if self.map[position[0],position[1]] == 1:
                found = True
        return position
