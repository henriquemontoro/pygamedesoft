# -*- coding: utf-8 -*-

import pygame
from config import *
from init_screen  import init_screen
from level_screen import level_screen
from game_screen  import game_screen
import sounds

# Inicialização do Pygame
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
sounds.init()

# Cria a janela do jogo
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITULO)

# Máquina de estados
state            = INIT
level            = 1
levels_unlocked  = 1   # começa só com fase 1 disponível

while state != QUIT:
    if state == INIT:
        state = init_screen(window)
    elif state == LEVEL_SELECT:
        state, level = level_screen(window, levels_unlocked)
    elif state == GAME:
        state, won = game_screen(window, level)
        if won:
            levels_unlocked = min(levels_unlocked + 1, 3) if level >= levels_unlocked else levels_unlocked
    else:
        state = QUIT

pygame.quit()