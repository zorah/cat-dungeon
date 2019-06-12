import math
import shelve

import pygame
from pygame.locals import *

import cevent
from dungeon import *
from hero import *


# change CApp into
class CApp(cevent.CEvent):
    _block_size = 20
    _game_size = 30
    _clock = pygame.time.Clock()

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._final_score = -1
        self._show_score = False
        self._scoreStart = 0
        self._update_score = False

    def on_init(self):
        pygame.init()
        #pygame.font.init() # does not have to be called after pygame.init()?

        self._window = pygame.display.set_mode((self._game_size*self._block_size, (self._game_size+1)*self._block_size), pygame.HWSURFACE)
        self._running = True

        pygame.mixer.music.load("squirrel.xm")
        pygame.mixer.music.play(-1,0.0)

        self._dungeon = Dungeon(self._window, self._block_size, self._game_size)
        self._dungeon.drawDungeon()

        self._hero = Hero(self._window, self._block_size, self._dungeon, self._clock)

    def on_event(self, event):
        if event.type == QUIT:
            self.on_exit()

        elif event.type >= USEREVENT:
            self.on_user(event)

        elif event.type == VIDEOEXPOSE:
            self.on_expose()

        elif event.type == VIDEORESIZE:
            self.on_resize(event)

        elif event.type == KEYUP:
            self.on_key_up(event)

        elif event.type == KEYDOWN:
            self.on_key_down(event)

        elif event.type == MOUSEMOTION:
            self.on_mouse_move(event)

        elif event.type == MOUSEBUTTONUP:
            if event.button == 0:
                self.on_lbutton_up(event)
            elif event.button == 1:
                self.on_mbutton_up(event)
            elif event.button == 2:
                self.on_rbutton_up(event)

        elif event.type == MOUSEBUTTONDOWN:
            self.on_lbutton_down(event)
            if event.button == 0:
                self.on_lbutton_down(event)
            elif event.button == 1:
                self.on_mbutton_down(event)
            elif event.button == 2:
                self.on_rbutton_down(event)

        elif event.type == ACTIVEEVENT:
            if event.state == 1:
                if event.gain:
                    self.on_mouse_focus()
                else:
                    self.on_mouse_blur()
            elif event.state == 2:
                if event.gain:
                    self.on_input_focus()
                else:
                    self.on_input_blur()
            elif event.state == 4:
                if event.gain:
                    self.on_restore()
                else:
                    self.on_minimize()
    def on_loop(self):
        pass
    def on_render(self):
        frame = math.floor(pygame.time.get_ticks() / 400) % 2
        pygame.draw.rect(self._window, (200, 200, 200), pygame.Rect(0,0,self._game_size*self._block_size,self._block_size))
        self._dungeon.drawDungeon()
        self._hero.render(frame)
        if self._final_score >= 0 and not self._show_score:
            self._show_score = True
            self._scoreStart = pygame.time.get_ticks()

        if self._show_score:
            # test if there was a new high Score# load the previous score if it exists
            try:
                d = shelve.open('score')
                score = d['highscore']
            except:
                score = 0

            # print final score
            rect = pygame.Rect(2*self._block_size, 2*self._block_size,400,100)
            pygame.draw.rect(self._window, (230, 230, 230), rect)
            myfont = pygame.font.SysFont('Arial', 16)
            textsurface = myfont.render('Your final score was ' + str(self._final_score) + '!', False, (10, 10, 10))
            self._window.blit(textsurface,(3*self._block_size, 3*self._block_size))

            if score < self._final_score: # new high score
                textsurface2 = myfont.render('Concats! You beat the previous high score of  ' + str(score) + '!!', False, (10, 10, 10))
                self._window.blit(textsurface2,(3*self._block_size, 5*self._block_size))
                # save the score
                self._update_score = True
            else:
                textsurface2 = myfont.render('The previous high score was ' + str(score) + '.', False, (10, 10, 10))
                self._window.blit(textsurface2,(3*self._block_size, 5*self._block_size))
                self._update_score = False

        pygame.display.flip()

        if self._show_score and (self._scoreStart <= (pygame.time.get_ticks() - 5000)):
            if score < self._final_score:
                d = shelve.open('score') # here you will save the score variable
                d['highscore'] = self._final_score # thats all, now it is saved on disk.
                d.close()
            self._final_score = -1
            self._show_score = False

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def on_exit(self):
        self._running = False

    def on_key_down(self, event):
        if not self._show_score:
            if event.key == pygame.K_LEFT:
                self._final_score = self._hero.moveHorizontal(-1)
            if event.key == pygame.K_RIGHT:
                self._final_score = self._hero.moveHorizontal(1)
            if event.key == pygame.K_DOWN:
                self._final_score = self._hero.moveVertical(1)
            if event.key == pygame.K_UP:
                self._final_score = self._hero.moveVertical(-1)
        if event.key == pygame.K_ESCAPE:
            self._running = False
        if event.key == pygame.K_TAB:
            self.reset()

    def reset(self):
        self._dungeon.reset()
        self._dungeon._counter = 0
        self._hero._score = 0
        self._hero._lives = 9
        self._hero.reset()

if __name__ == "__main__" :
    theApp = CApp()
    theApp.on_execute()
