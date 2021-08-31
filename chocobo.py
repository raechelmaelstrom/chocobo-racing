"""Module to represent one chocobo in the race."""
import logging
import random

class Chocobo:
    def __init__(self, game, number):
        self.game = game
        self.x = -80
        self.y = 0
        self.lap = 1
        self.run_frame = 0
        self.double_rolls = 0
        self.chocobo_number = number

    def move(self):
        roll = random.randint(1,7)
        if roll == 6:
            self.double_rolls += 5

        if self.double_rolls:
            roll *= 2
            self.double_rolls -= 1

        self.x += roll
        if self.x > self.game.screen_width:
            self.lap += 1
            self.x -= self.game.screen_width + 80

        self.run_frame = ((self.run_frame + 1) % 3)

    def draw(self):
        image = self.game.chocobo_sprites.get_sprite(self.chocobo_number, self.run_frame)
        rect = image.get_rect()
        rect.topleft = (self.x, self.y)
        self.game.screen.blit(image, rect)
