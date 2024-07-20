import pygame
from game import IntroScreen, Game

pygame.init()

WIDTH, HEIGHT = 1280, 720

intro = IntroScreen(WIDTH, HEIGHT)
intro.run()

game = Game(WIDTH, HEIGHT)
game.run()

pygame.quit()
