"""Module to represent loading different chocobo sprites"""
import logging

from spritesheet import SpriteSheet

CHOCOBO_WIDTH = 73
CHOCOBO_HEIGHT = 72

class ChocoboSprites:
    def __init__(self):
        self.spritesheet = SpriteSheet("chocobo.png")

    def get_sprite(self, chocobo_number, run_frame):
        if run_frame > 3:
            raise Exception("Uhoh, invalid run_frame")

        left = CHOCOBO_WIDTH * chocobo_number * 3 + run_frame * CHOCOBO_WIDTH

        # First or second row?
        top = CHOCOBO_HEIGHT * 2
        if chocobo_number > 3:
            top = top * 2

        return self.spritesheet.image_at((left, top, CHOCOBO_WIDTH, CHOCOBO_HEIGHT))
