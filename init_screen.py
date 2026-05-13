# -*- coding: utf-8 -*-

import pygame
from config import *

def init_screen(window):
    """
    Tela inicial do jogo.
    
    Argumentos:
        window: janela do pygame onde a tela será desenhada
        
    Retorno:
        state: próximo estado do jogo
    """
    
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()
    
    # Estado inicial
    state = INIT
    
    # Loop da tela inicial
    while state == INIT:
        # Ajusta a velocidade
        clock.tick(FPS)
        
        # Processa os eventos
        for event in pygame.event.get():
            # Fecha a janela
            if event.type == pygame.QUIT:
                state = QUIT
            
            # Eventos de teclado
            if event.type == pygame.KEYDOWN:
                # ESPAÇO ou ENTER para começar
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    state = GAME
                # ESC para sair
                elif event.key == pygame.K_ESCAPE:
                    state = QUIT
        
        # Desenha fundo
        window.fill(PRETO)
        
        # Título
        font_titulo = pygame.font.SysFont(None, 72)
        text_titulo = font_titulo.render('FIREBOY & WATERGIRL', True, AMARELO)
        rect_titulo = text_titulo.get_rect()
        rect_titulo.centerx = WIDTH // 2
        rect_titulo.centery = HEIGHT // 3
        window.blit(text_titulo, rect_titulo)
        
        # Descrição dos personagens
        font_desc = pygame.font.SysFont(None, 36)
        
        text_fire = font_desc.render('FIREBOY (vermelho) - WASD', True, VERMELHO)
        rect_fire = text_fire.get_rect()
        rect_fire.centerx = WIDTH // 2
        rect_fire.centery = HEIGHT // 2
        window.blit(text_fire, rect_fire)
        
        text_water = font_desc.render('WATERGIRL (azul) - Setas', True, AZUL)
        rect_water = text_water.get_rect()
        rect_water.centerx = WIDTH // 2
        rect_water.centery = HEIGHT // 2 + 50
        window.blit(text_water, rect_water)
        
        # Instruções
        font_inst = pygame.font.SysFont(None, 28)
        
        text_inst1 = font_inst.render('Trabalhem juntos para resolver os puzzles!', True, BRANCO)
        rect_inst1 = text_inst1.get_rect()
        rect_inst1.centerx = WIDTH // 2
        rect_inst1.centery = HEIGHT // 2 + 120
        window.blit(text_inst1, rect_inst1)
        
        text_inst2 = font_inst.render('Fireboy nao pode tocar agua', True, BRANCO)
        rect_inst2 = text_inst2.get_rect()
        rect_inst2.centerx = WIDTH // 2
        rect_inst2.centery = HEIGHT // 2 + 150
        window.blit(text_inst2, rect_inst2)
        
        text_inst3 = font_inst.render('Watergirl nao pode tocar lava', True, BRANCO)
        rect_inst3 = text_inst3.get_rect()
        rect_inst3.centerx = WIDTH // 2
        rect_inst3.centery = HEIGHT // 2 + 180
        window.blit(text_inst3, rect_inst3)
        
        # Prompt para começar
        font_start = pygame.font.SysFont(None, 32)
        text_start = font_start.render('Pressione ESPACO para comecar', True, VERDE)
        rect_start = text_start.get_rect()
        rect_start.centerx = WIDTH // 2
        rect_start.centery = HEIGHT - 80
        window.blit(text_start, rect_start)
        
        # Atualiza tela
        pygame.display.flip()
    
    return state