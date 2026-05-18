# -*- coding: utf-8 -*-

import pygame
import math
from config import *


def _draw_btn_rect(window, text, rect, font, mx, my):
    hov  = rect.collidepoint(mx, my)
    bg   = (70, 65, 105) if hov else (40, 36, 65)
    bord = (230, 220, 255) if hov else (140, 130, 180)
    pygame.draw.rect(window, bg,   rect, border_radius=10)
    pygame.draw.rect(window, bord, rect, 2, border_radius=10)
    txt = font.render(text, True, BRANCO)
    window.blit(txt, txt.get_rect(center=rect.center))


def init_screen(window):
    clock   = pygame.time.Clock()
    state   = INIT
    tick    = 0

    font_title = pygame.font.SysFont(None, 80)
    font_sub   = pygame.font.SysFont(None, 34)
    font_info  = pygame.font.SysFont(None, 26)
    font_btn   = pygame.font.SysFont(None, 36)

    # Posições fixas dos botões — calculadas uma vez antes do loop
    btn_jogar = pygame.Rect(WIDTH // 2 - 100, 395, 200, 50)
    btn_sair  = pygame.Rect(WIDTH // 2 - 100, 459, 200, 50)

    while state == INIT:
        clock.tick(FPS)
        tick += 1
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_jogar.collidepoint(mx, my):
                    state = LEVEL_SELECT
                if btn_sair.collidepoint(mx, my):
                    state = QUIT

        # ── Fundo gradiente escuro ─────────────────────────────────────
        for y in range(HEIGHT):
            t = y / HEIGHT
            r = int(8  + t * 18)
            g = int(6  + t * 12)
            b = int(22 + t * 28)
            pygame.draw.line(window, (r, g, b), (0, y), (WIDTH, y))

        # Estrelas animadas
        for sx, sy, sr in [(60, 40, 1), (180, 70, 2), (320, 25, 1),
                           (480, 55, 2), (610, 38, 1), (740, 68, 2),
                           (110, 130, 1), (400, 90, 1), (570, 110, 2),
                           (700, 140, 1), (250, 115, 2)]:
            bright = int(130 + 80 * math.sin(tick * 0.04 + sx * 0.05))
            pygame.draw.circle(window, (bright, bright, bright), (sx, sy), sr)

        # ── Título ────────────────────────────────────────────────────
        pulse = int(4 * math.sin(tick * 0.06))
        title_font = pygame.font.SysFont(None, 80 + pulse)
        title = title_font.render('FIREBOY & WATERGIRL', True, AMARELO)
        window.blit(title, title.get_rect(center=(WIDTH // 2, 110)))

        # Linha decorativa
        pygame.draw.line(window, (100, 80, 180),
                         (WIDTH // 2 - 280, 145), (WIDTH // 2 + 280, 145), 2)

        # ── Descrição dos controles ────────────────────────────────────
        cy_ctrl = 195
        for text, color in [
            ('Fireboy  (vermelho)  —  WASD', (220, 80, 60)),
            ('Watergirl  (azul)  —  Setas', (60, 100, 220)),
        ]:
            surf = font_sub.render(text, True, color)
            window.blit(surf, surf.get_rect(center=(WIDTH // 2, cy_ctrl)))
            cy_ctrl += 38

        # ── Regras ────────────────────────────────────────────────────
        regras = [
            'Trabalhem juntos para resolver os puzzles!',
            'Fireboy não pode tocar água   •   Watergirl não pode tocar lava',
            'Piscina verde é ácido — mata os dois!',
        ]
        cy_reg = 295
        for linha in regras:
            surf = font_info.render(linha, True, (190, 185, 220))
            window.blit(surf, surf.get_rect(center=(WIDTH // 2, cy_reg)))
            cy_reg += 28

        # ── Botões ────────────────────────────────────────────────────
        _draw_btn_rect(window, 'JOGAR', btn_jogar, font_btn, mx, my)
        _draw_btn_rect(window, 'SAIR',  btn_sair,  font_btn, mx, my)

        pygame.display.flip()

    return state