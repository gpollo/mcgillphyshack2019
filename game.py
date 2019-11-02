from threading import Thread
from time import sleep

import pygame
import pygame.gfxdraw

# TODO: find some way update surface size

class Game(object):
    def __init__(self):
        self.__canvas = None
        self.__running = False
        self.__surface = pygame.Surface((400, 400), pygame.SRCALPHA, 32)
        self.__thread = Thread(target=self.game_loop)
    
    def get_surface(self):
        return self.__surface

    def start(self, canvas):
        if self.__running:
            print("game thread is already running")
            return

        self.__canvas = canvas
        self.__running = True
        self.__thread.start()

    def game_loop(self):
        # TODO: draw something useful
        c = 0
        while self.__running:
            sleep(1/60)
            c = (c + 1) % 255
            self.__surface.fill((0, 0, 0, 0))
            pygame.gfxdraw.aacircle(self.__surface, c, c, c//10, (c, c, c))
            pygame.gfxdraw.filled_circle(self.__surface, c, c, c//10, (c, c, c))
            self.__canvas.update()

            if self.__canvas is None:
                print("missing canvas to update")
            else:
                self.__canvas.update()

    def stop(self):
        if not self.__running:
            print("game thread is not running")
            return

        self.__running = False
        self.__thread.join()
        
