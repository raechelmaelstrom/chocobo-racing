#!/usr/bin/env python
import asyncio
from enum import Enum
import logging
import time
import sys

import pygame
import pygame.freetype

from pygame.locals import *

from twitchio import Channel, User, Client

import creds
from chocobo import Chocobo
from chocobosprites import ChocoboSprites, CHOCOBO_HEIGHT

class GameState(Enum):
    IDLE = 1
    STARTING = 2
    RACING = 3
    WINNER = 4

class Game:
    def __init__(self, twitch):
        self.screen_width = 1920
        self.screen_height = CHOCOBO_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.chocobo_sprites = ChocoboSprites()
        self.font = pygame.freetype.Font("ff6.ttf", 72)
        self.twitch = twitch
        self.twitch_user = None
        self.reset()

    def reset(self):
        self.state = GameState.IDLE
        self.wait_time = 300
        self.current_lap = 0
        self.winner = None
        self.prediction = None

        self.chocobos = [
                Chocobo(self, 0),
                Chocobo(self, 2),
        ]

    def draw_idle(self):
        self.wait_time -= 1

        if self.wait_time <= 0:
            self.wait_time = 300
            self.state = GameState.STARTING

    async def draw_starting(self):
        self.wait_time -= 1
        text_surface, rect = self.font.render(f"Starting race in: {self.wait_time / 10}", (255, 255, 255))
        self.screen.blit(text_surface, dest=(700, 15))

        if self.twitch_user == None:
            self.twitch_user = (await self.twitch.fetch_users(names=[creds.username]))[0]

        if self.prediction == None:
            self.prediction = await self.twitch_user.create_prediction(creds.token, 'Chocobo Race Results', 'yellow', 'red', 30)

        if self.wait_time <= 0:
            self.wait_time = 300
            self.state = GameState.RACING

    def draw_race(self):
        for c in self.chocobos:
            c.draw()

            if c.lap > self.current_lap:
                self.current_lap = c.lap
                self.lap_height = -50

                if self.current_lap > 4:
                    if not self.winner:
                        self.winner = c
                    else:
                        # It's a tie, run another lap
                        self.winner = None

        self.lap_height += 2
        text_surface, rect = self.font.render(f"Lap {self.current_lap}", (255, 255, 255))
        self.screen.blit(text_surface, dest=(1400, self.lap_height))

        if self.winner:
            self.state = GameState.WINNER

    async def draw_winner(self):
        text_surface, rect = self.font.render(f"A Winner is You", (255, 255, 255))
        self.screen.blit(text_surface, dest=(700, 15))

        if self.prediction:
            winning_index = self.chocobos.index(self.winner)
            winning_outcome = self.prediction.outcomes[winning_index].outcome_id
            await self.twitch_user.end_prediction(creds.token, self.prediction.prediction_id, "RESOLVED", winning_outcome)
            self.prediction = None

        if self.wait_time <= 0:
            self.reset()
        elif self.wait_time == 300:
            self.winner.x = 1100
        else:
            self.winner.move()
            self.winner.draw()

        self.wait_time -= 1

    async def run_game(self):
        while True:
            self.screen.fill((255,0, 255)) # Magenta BG

            await asyncio.sleep(.1)

            if self.state == GameState.IDLE:
                self.draw_idle()
            if self.state == GameState.STARTING:
                await self.draw_starting()
            elif self.state == GameState.RACING:
                for c in self.chocobos:
                    c.move()

                self.draw_race()
            elif self.state == GameState.WINNER:
                await self.draw_winner()

            pygame.display.flip()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.debug("Initializing game")

    pygame.init()
    pygame.display.set_caption("Chocobo Racing")

    loop = asyncio.get_event_loop()

    twitch = Client(token=creds.token,
                    initial_channels=[f'#{creds.username}'],
                    client_secret=creds.client_secret,
                    loop=loop)
    game = Game(twitch)

    game_task = loop.create_task(game.run_game())
    twitch_task = loop.create_task(twitch.run())
    logging.debug("initialized")

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        twitch_task.cancel()
        game_task.cancel()

    pygame.quit()
