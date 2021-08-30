#!/usr/bin/env python
import logging
import time
import sys

import pygame
from pygame.locals import *

from chocobo import Chocobo
from chocobosprites import ChocoboSprites, CHOCOBO_HEIGHT

class Game:
    def __init__(self):
        self.screen_width = 1920
        self.screen_height = CHOCOBO_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.chocobo_sprites = ChocoboSprites()
        self.chocobos = [
                Chocobo(self, 0),
                Chocobo(self, 2),
                #Chocobo(self, 3),
                #Chocobo(self, 4),
        ]

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                logging.debug("exiting...")
                sys.exit()

        self.screen.fill((255,0, 255)) # Magenta BG

        for c in self.chocobos:
            c.draw()

        pygame.display.flip()

    def run(self):
        while True:
            time.sleep(.1)

            for c in self.chocobos:
                c.move()

            self.draw()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Initializing game")

    pygame.init()
    pygame.display.set_caption("Chocobo Racing")

    logging.debug("initialized")
    game = Game()
    game.run()
