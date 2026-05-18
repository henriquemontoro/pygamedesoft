# -*- coding: utf-8 -*-

import pygame
from config import *
from init_screen  import init_screen
from level_screen import level_screen
from game_screen  import game_screen

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Cria a janela do jogo
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITULO)

# Máquina de estados
state = INIT
level = 1

while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == LEVEL_SELECT:
        state, level = level_screen(window)
    elif state == GAME:
        state = game_screen(window, level)
    else:
        state = QUIT

pygame.quit()