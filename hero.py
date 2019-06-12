import math
import numpy as np
import pygame
from pygame.locals import *
import pickle

class Hero():
    _sprite = pygame.image.load("cat_trans.png")
    _sprite_move = pygame.image.load("cat2_trans.png")
    _sprite_life = pygame.image.load("head.png")
    _position = (0,0)
    _lives = 9
    _score = 0

    def __init__(self, window, block_size, dungeon, clock):
        self._window = window
        self._block_size = block_size
        self._dungeon = dungeon
        self._clock = clock

        self._wall_sound = pygame.mixer.Sound("swoosh.wav")
        self._levelup_sound = pygame.mixer.Sound("level-up.wav")
        self._loose_sound = pygame.mixer.Sound("loose.wav")
        self._wallcrash_sound = pygame.mixer.Sound("wall-crash.wav")
        self._milk_sound = pygame.mixer.Sound("milk.wav")

        self._position = self._dungeon.randomPosition()

    def reset(self):
        self._position = self._dungeon.randomPosition()

    def render(self, frame):
        # render hero
        if frame == 0:
            image = self._sprite
        else:
            image = self._sprite_move
        self._window.blit(image, (self._position[0]*self._block_size, (self._position[1]+1)*self._block_size))
        # render number of lifes
        for i in range(self._lives):
            self._window.blit(self._sprite_life, (i*self._block_size, 0))
        #
        # write new name
        myfont = pygame.font.SysFont('Arial', 16)
        textsurface = myfont.render('Score: ' + str(self._score), False, (10, 10, 10))
        self._window.blit(textsurface,(20*self._block_size, 0))

    def afterMoving(self):
        # check for healing
        if self._dungeon.map[self._position[0], self._position[1]] == 3:
            self._lives = min(9, self._lives + 2)
            self._score += 1
            self._milk_sound.play()
            self._dungeon.map[self._position[0], self._position[1]] = 1
        # check winning
        if self._dungeon.validateGoal(self._position[0], self._position[1]):
            # move to next next Level
            self._dungeon._counter += 1
            self._score += 5
            self._levelup_sound.play()
            self._lives = min(9, self._lives + 2)
            self._dungeon.reset()
            self.reset()

    def removeLife(self, lost):
        self._lives -= lost
        if (self._lives < 0):
            # loose game
            # update
            self._dungeon._counter = 0
            self._dungeon.reset()
            self._loose_sound.play()
            self.reset()
            self._lives = 9
            score = self._score
            self._score = 0
            return score
        return -1


    def moveHorizontal(self, direction):
        return_value = -1
        if self._dungeon.validatePosition(self._position[0] + direction, self._position[1]):
            self._position[0] += direction
            self.afterMoving()
        elif self._dungeon.validatePosition(self._position[0] + 2*direction, self._position[1]):
            self._wall_sound.play()
            self._position[0] += 2*direction
            return_value = self.removeLife(1)
            self.afterMoving()
        elif self._dungeon.validatePosition(self._position[0] + 3*direction, self._position[1]):
            self._wall_sound.play()
            self._position[0] += 3*direction
            return_value = self.removeLife(3)
            self.afterMoving()
        else:
            self._wallcrash_sound.play()
        return return_value

    def moveVertical(self, direction):
        return_value = -1
        if self._dungeon.validatePosition(self._position[0], self._position[1] + direction):
            self._position[1] += direction
            self.afterMoving()
        elif self._dungeon.validatePosition(self._position[0], self._position[1] + 2*direction):
            self._wall_sound.play()
            self._position[1] += 2*direction
            return_value = self.removeLife(1)
            self.afterMoving()
        elif self._dungeon.validatePosition(self._position[0], self._position[1] + 3*direction):
            self._wall_sound.play()
            self._position[1] += 3*direction
            return_value = self.removeLife(3)
            self.afterMoving()
        else:
            self._wallcrash_sound.play()
        return return_value
