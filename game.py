#!/usr/bin/env python
import logging
import sys

import pygame
from pygame.locals import *

logging.basicConfig(level=logging.DEBUG)
logging.debug("hello world")

pygame.init()

logging.debug("initialized")

screen = pygame.display.set_mode((1920, 480))

while True:
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            logging.debug("Exiting...")
            sys.exit()
