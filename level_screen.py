# -*- coding: utf-8 -*-

import pygame
import math
from config import *


def level_screen(window):
    """Tela de seleção de fase. Retorna (state, level_num)."""
    clock  = pygame.time.Clock()
    tick   = 0
    result = None

    font_title = pygame.font.SysFont(None, 56)
    font_num   = pygame.font.SysFont(None, 80)
    font_name  = pygame.font.SysFont(None, 32)
    font_small = pygame.font.SysFont(None, 22)

    card_data = [
        ('1', 'FLORESTA', (45, 90, 45),  1, 'Fácil'),
        ('2', 'CAVERNA',  (35, 28, 65),  2, 'Médio'),
        ('3', 'VULCÃO',   (100, 32, 12), 3, 'Difícil'),
    ]

    def draw_stars(surf, n_filled, cx, cy, size=8):
        """Desenha 3 estrelas de 5 pontas; n_filled delas preenchidas."""
        import math as _m
        spacing = size * 2 + 4
        start_x = cx - spacing
        for i in range(3):
            sx = start_x + i * spacing
            filled = i < n_filled
            pts_outer, pts_inner = [], []
            for k in range(5):
                ang_o = _m.radians(-90 + k * 72)
                ang_i = _m.radians(-90 + k * 72 + 36)
                pts_outer.append((sx + size   * _m.cos(ang_o),
                                  cy + size   * _m.sin(ang_o)))
                pts_inner.append((sx + size/2 * _m.cos(ang_i),
                                  cy + size/2 * _m.sin(ang_i)))
            pts = []
            for o, inn in zip(pts_outer, pts_inner):
                pts.append(o); pts.append(inn)
            if filled:
                pygame.draw.polygon(surf, AMARELO, pts)
                pygame.draw.polygon(surf, (200, 160, 0), pts, 1)
            else:
                pygame.draw.polygon(surf, (80, 80, 60), pts)
                pygame.draw.polygon(surf, (140, 130, 80), pts, 1)

    # Posição dos cards centrada horizontalmente
    CW, CH  = 195, 210
    card_xs = [133, 400, 667]
    card_y  = HEIGHT // 2 + 20
    card_rects = [
        pygame.Rect(cx - CW // 2, card_y - CH // 2, CW, CH)
        for cx in card_xs
    ]

    # Rect fixo do botão Voltar — calculado antes do loop
    btn_voltar_rect = pygame.Rect(WIDTH // 2 - 80, HEIGHT - 50, 160, 36)

    while result is None:
        clock.tick(FPS)
        tick += 1

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return QUIT, 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return INIT, 1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(card_rects):
                    if rect.collidepoint(mx, my):
                        result = (GAME, i + 1)
                if btn_voltar_rect.collidepoint(mx, my):
                    return INIT, 1

        # ── Fundo ────────────────────────────────────────────────────────
        window.fill((15, 12, 28))

        # Estrelas no fundo
        for sx, sy, sr in [(80, 50, 1), (200, 80, 2), (350, 30, 1),
                           (500, 60, 2), (640, 45, 1), (740, 70, 2),
                           (120, 120, 1), (420, 100, 1), (580, 115, 2)]:
            bright = int(160 + 60 * math.sin(tick * 0.05 + sx))
            pygame.draw.circle(window, (bright, bright, bright), (sx, sy), sr)

        # Título
        title = font_title.render('SELECIONE A FASE', True, AMARELO)
        window.blit(title, title.get_rect(center=(WIDTH // 2, 80)))

        sub = font_small.render(
            'Clique em uma fase para jogar', True, (160, 160, 160))
        window.blit(sub, sub.get_rect(center=(WIDTH // 2, 120)))

        # ── Cards ─────────────────────────────────────────────────────────
        for i, (num, name, color, n_stars, diff_label) in enumerate(card_data):
            cx   = card_xs[i]
            rect = card_rects[i]
            hovered = rect.collidepoint(mx, my)
            pulse   = int(5 * math.sin(tick * 0.07 + i * 2.1))

            draw_rect = rect.inflate(pulse * 2, pulse * 2) if hovered else rect

            # Sombra
            shadow = draw_rect.move(4, 4)
            pygame.draw.rect(window, (8, 6, 16), shadow, border_radius=14)

            # Card
            pygame.draw.rect(window, color, draw_rect, border_radius=14)
            border = AMARELO if hovered else (130, 120, 160)
            pygame.draw.rect(window, border, draw_rect, 3, border_radius=14)

            cy = card_y

            # Número grande
            num_surf = font_num.render(num, True, AMARELO if hovered else BRANCO)
            window.blit(num_surf, num_surf.get_rect(center=(cx, cy - 52)))

            # Nome
            name_surf = font_name.render(name, True, BRANCO)
            window.blit(name_surf, name_surf.get_rect(center=(cx, cy + 18)))

            # Estrelas de dificuldade desenhadas + rótulo
            draw_stars(window, n_stars, cx, cy + 46)
            diff_surf = font_small.render(diff_label, True, (210, 210, 200))
            window.blit(diff_surf, diff_surf.get_rect(center=(cx, cy + 64)))

            # Hint de tecla
            key_surf = font_small.render(f'[{num}]', True, (140, 140, 140))
            window.blit(key_surf, key_surf.get_rect(center=(cx, cy + 82)))

        # Botão voltar
        bvw, bvh = 160, 36
        bvx, bvy = WIDTH // 2 - bvw // 2, HEIGHT - 50
        btn_voltar_rect = pygame.Rect(bvx, bvy, bvw, bvh)
        hov_v = btn_voltar_rect.collidepoint(mx, my)
        pygame.draw.rect(window, (60, 55, 90) if hov_v else (35, 30, 58),
                         btn_voltar_rect, border_radius=8)
        pygame.draw.rect(window, (180, 170, 220) if hov_v else (110, 100, 150),
                         btn_voltar_rect, 2, border_radius=8)
        vlbl = font_small.render('< VOLTAR', True, BRANCO)
        window.blit(vlbl, vlbl.get_rect(center=btn_voltar_rect.center))

        pygame.display.flip()

    return result