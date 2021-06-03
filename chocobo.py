"""Module to represent one chocobo in the race."""
import logging
import random

class Chocobo:
    def __init__(self, game, number):
        self.game = game
        self.x = 0
        self.y = 0
        self.run_frame = 0
        self.chocobo_number = number

    def move(self):
        distance = random.randrange(1, 4)
        self.x = ((self.x + distance) % self.game.screen_width)
        self.run_frame = ((self.run_frame + 1) % 3)

    def draw(self):
        image = self.game.chocobo_sprites.get_sprite(self.chocobo_number, self.run_frame)
        rect = image.get_rect()
        rect.topleft = (self.x, self.y)
        self.game.screen.blit(image, rect)
