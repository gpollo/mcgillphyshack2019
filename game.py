from threading import Thread
from time import sleep

import pygame
import pygame.gfxdraw

class Game(object):
    def __init__(self):
        self.__canvas = None
        self.__model = None
        self.__running = False
        self.__surface = pygame.Surface((400, 400), pygame.SRCALPHA, 32)
        self.__thread = Thread(target=self.game_loop)
    
    def get_surface(self):
        return self.__surface

    def resize_surface(self, w, h):
        self.__surface = pygame.Surface((w, h), pygame.SRCALPHA, 32)

    def start(self, canvas):
        if self.__running:
            print("game thread is already running")
            return

        self.__canvas = canvas
        self.__running = True
        self.__thread.start()

    def game_loop(self):
        # TODO: draw something useful
        time = 0
        while self.__running:
            sleep(1/60)
            time += 1/60

#            p = (p + 0.5) % 100
#            (w, h) = self.__surface.get_size()
#            x = int((p/100) * w)
#            y = int((p/100) * h)
#            c = int((p/100) * 255)
#
#            self.__surface.fill((0, 0, 0, 0))
#            pygame.gfxdraw.aacircle(self.__surface, x, y, c, (c, c, c))
#            pygame.gfxdraw.filled_circle(self.__surface, x, y, c, (c, c, c))

            if self.__model is not None:
                self.__model.draw(self.__surface, time)

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
        
    def set_model(self, model):
        self.__model = model
