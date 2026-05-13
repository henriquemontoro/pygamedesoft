# -*- coding: utf-8 -*-

# Dados gerais do jogo
WIDTH = 800  # Largura da tela
HEIGHT = 600  # Altura da tela
FPS = 30  # Frames por segundo
TITULO = 'Fireboy and Watergirl'

# Estados para controle do jogo
INIT = 0
GAME = 1
QUIT = 2

# Cores RGB
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
CINZA = (100, 100, 100)
CINZA_ESCURO = (50, 50, 50)

# Física do jogo
GRAVIDADE = 0.8
VELOCIDADE_PULO = -13
VELOCIDADE_MOVIMENTO = 5

# Tamanhos dos sprites
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 50
PLATFORM_HEIGHT = 20