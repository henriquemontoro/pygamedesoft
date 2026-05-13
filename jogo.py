# -*- coding: utf-8 -*-

import pygame
from config import *
from init_screen import init_screen
from game_screen import game_screen

# Inicialização do Pygame
pygame.init()
pygame.mixer.init()

# Cria a janela do jogo
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITULO)

# Máquina de estados
state = INIT

# Loop principal
while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == GAME:
        state = game_screen(window)
    else:
        state = QUIT

# Finalização do Pygame
pygame.quit()