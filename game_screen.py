# -*- coding: utf-8 -*-

import pygame
import math
from config import *
from sprites import *

GROUND_Y = HEIGHT - 40   # y do topo do chão
COR_CHAO = (75, 50, 22)
COR_PLAT = (115, 78, 38)

#Obtido com ajuda de IAg - pré-renderiza o fundo de floresta uma única vez
def make_forest_bg():
    bg = pygame.Surface((WIDTH, HEIGHT))

    sky_top = (110, 190, 255)
    sky_bot = (165, 225, 195)
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(sky_top[0] + t * (sky_bot[0] - sky_top[0]))
        g = int(sky_top[1] + t * (sky_bot[1] - sky_top[1]))
        b = int(sky_top[2] + t * (sky_bot[2] - sky_top[2]))
        pygame.draw.line(bg, (r, g, b), (0, y), (WIDTH, y))

    for cx, cy, cw, ch in [(130, 55, 90, 32), (315, 38, 115, 42),
                            (548, 62, 88, 30), (718, 44, 82, 28)]:
        pygame.draw.ellipse(bg, (245, 248, 255), (cx - cw // 2, cy - ch // 2, cw, ch))
        pygame.draw.ellipse(bg, (255, 255, 255), (cx - cw // 4, cy - ch, cw // 2, ch))
        pygame.draw.ellipse(bg, (240, 244, 255),
                            (cx + cw // 6, cy - ch * 3 // 4, cw // 3, ch // 2))

    pts_hill = [(0, HEIGHT)]
    for x in range(0, WIDTH + 1, 12):
        y_h = int(355 + 42 * math.sin(x * 0.019) + 22 * math.sin(x * 0.047 + 1))
        pts_hill.append((x, y_h))
    pts_hill.append((WIDTH, HEIGHT))
    pygame.draw.polygon(bg, (55, 110, 65), pts_hill)
    pygame.draw.lines(bg, (78, 140, 85), False, pts_hill[1:-1], 2)

    for tx in range(-30, WIDTH + 30, 62):
        th = int(230 + (tx * 7 % 55))
        pygame.draw.rect(bg, (58, 38, 15), (tx + 23, th + 50, 14, 120))
        pygame.draw.circle(bg, (28, 88, 42), (tx + 30, th + 42), 46)
        pygame.draw.circle(bg, (38, 108, 52), (tx + 30, th + 24), 34)
        pygame.draw.circle(bg, (52, 128, 62), (tx + 30, th + 10), 22)

    for tx, ty, tr in [(-15, 240, 72), (62, 268, 65), (698, 252, 68),
                        (758, 270, 62), (132, 288, 58), (652, 282, 60)]:
        cx = tx + 30
        pygame.draw.rect(bg, (45, 28, 8), (cx - 12, ty + tr, 24, HEIGHT))
        pygame.draw.circle(bg, (20, 70, 30), (cx, ty + 40), tr)
        pygame.draw.circle(bg, (30, 88, 40), (cx, ty + 20), tr - 14)
        pygame.draw.circle(bg, (42, 108, 50), (cx, ty + 4),  tr - 28)

    pygame.draw.rect(bg, (62, 95, 38), (0, GROUND_Y - 6, WIDTH, 6))
    return bg

#Obtido com ajuda de IAg
def make_cave_bg():
    """Pré-renderiza o fundo de caverna."""
    bg = pygame.Surface((WIDTH, HEIGHT))

    # Gradiente escuro azul-roxo
    for y in range(HEIGHT):
        t = y / HEIGHT
        pygame.draw.line(bg, (int(18 + t*20), int(12 + t*18), int(38 + t*22)), (0, y), (WIDTH, y))

    # Blocos de pedra no fundo (textura de parede)
    for row in range(0, HEIGHT, 32):
        offset = 16 if (row // 32) % 2 else 0
        for col in range(-offset, WIDTH + 32, 32):
            shade = 28 + (col // 32 + row // 32) % 3 * 5
            pygame.draw.rect(bg, (shade, shade - 5, shade + 8), (col + 1, row + 1, 30, 30))
            pygame.draw.rect(bg, (20, 15, 35), (col, row, 32, 32), 1)

    # Estalactites no teto
    for sx in range(0, WIDTH + 40, 38):
        h = int(30 + 20 * math.sin(sx * 0.07 + 0.8))
        pygame.draw.polygon(bg, (45, 35, 65), [(sx, 0), (sx + 18, 0), (sx + 9, h)])
        pygame.draw.polygon(bg, (60, 48, 80), [(sx + 4, 0), (sx + 14, 0), (sx + 9, h - 6)])

    # Cristais bioluminescentes no chão da caverna
    crystal_data = [(80, GROUND_Y - 20, (50, 200, 255)),
                    (220, GROUND_Y - 18, (100, 255, 180)),
                    (500, GROUND_Y - 22, (180, 120, 255)),
                    (680, GROUND_Y - 19, (50, 220, 255)),
                    (340, GROUND_Y - 16, (120, 255, 160))]
    for cx, cy, cc in crystal_data:
        # Brilho (glow simples)
        for r in [18, 13, 8]:
            glow = tuple(max(0, c // (r // 4 + 1)) for c in cc)
            pygame.draw.circle(bg, glow, (cx, cy), r)
        pygame.draw.circle(bg, cc, (cx, cy), 6)
        # Pontas do cristal
        pygame.draw.polygon(bg, cc, [(cx - 5, cy + 2), (cx + 5, cy + 2), (cx, cy - 18)])
        pygame.draw.polygon(bg, cc, [(cx - 3, cy + 2), (cx + 3, cy + 2), (cx + 6, cy - 10)])

    # Gotas d'água no teto
    for dx in range(30, WIDTH, 90):
        pygame.draw.circle(bg, (80, 130, 200), (dx, 5), 3)
        pygame.draw.line(bg, (80, 130, 200), (dx, 8), (dx, 18), 1)

    pygame.draw.rect(bg, (35, 28, 55), (0, GROUND_Y - 6, WIDTH, 6))
    return bg

#Obtido com ajuda de IAg
def make_volcano_bg():
    """Pré-renderiza o fundo de vulcão."""
    bg = pygame.Surface((WIDTH, HEIGHT))

    # Céu avermelhado com fumaça
    for y in range(HEIGHT):
        t = y / HEIGHT
        pygame.draw.line(bg, (int(100 + t*60), int(20 + t*30), int(5 + t*8)), (0, y), (WIDTH, y))

    # Silhuetas de vulcões ao fundo
    for vx, vw, vh in [(110, 200, 210), (690, 220, 230), (400, 180, 195)]:
        pts = [(vx - vw // 2, HEIGHT), (vx, HEIGHT - vh), (vx + vw // 2, HEIGHT)]
        pygame.draw.polygon(bg, (55, 18, 8), pts)
        # Cratera com lava brilhante
        pygame.draw.ellipse(bg, (220, 70, 0), (vx - 22, HEIGHT - vh + 2, 44, 18))
        pygame.draw.ellipse(bg, (255, 180, 30), (vx - 12, HEIGHT - vh + 5, 24, 10))
        # Nuvens de fumaça
        for fx, fy, fr in [(vx - 10, HEIGHT - vh - 25, 14),
                           (vx + 5,  HEIGHT - vh - 38, 18),
                           (vx - 20, HEIGHT - vh - 48, 12)]:
            pygame.draw.circle(bg, (70, 28, 12), (fx, fy), fr)

    # Riachos de lava nas laterais
    for lx in [15, WIDTH - 15]:
        for seg in range(60, HEIGHT - 80, 40):
            pygame.draw.rect(bg, (180, 50, 0), (lx - 5, seg, 10, 36))
            pygame.draw.rect(bg, (255, 130, 0), (lx - 2, seg + 5, 4, 24))

    # Pedras vulcânicas em primeiro plano
    for rx in range(0, WIDTH + 50, 55):
        rh = int(18 + 10 * math.sin(rx * 0.09 + 2.1))
        pygame.draw.polygon(bg, (60, 22, 10),
                            [(rx, HEIGHT), (rx + 26, HEIGHT), (rx + 13, HEIGHT - rh)])

    pygame.draw.rect(bg, (70, 25, 10), (0, GROUND_Y - 6, WIDTH, 6))
    return bg

#Extraído com ajuda de IAg
def draw_timer_bars(window, buttons, doors, font):
    """Desenha barra de contagem regressiva acima de cada porta aberta."""
    for btn, door in zip(buttons, doors):
        frac = btn.timer_frac
        if frac > 0 and not btn._phys:
            bw = door.DOOR_WIDTH
            bx = door.rect.x
            by = door.rect.top - 10
            # Fundo cinza
            pygame.draw.rect(window, (80, 80, 80), (bx, by, bw, 6))
            # Barra colorida (verde → amarelo → vermelho)
            bar_color = (
                int(255 * (1 - frac)),
                int(255 * frac),
                0
            )
            pygame.draw.rect(window, bar_color, (bx, by, int(bw * frac), 6))
            # Segundos restantes
            secs = math.ceil(btn._timer / FPS)
            txt = font.render(str(secs), True, AMARELO)
            window.blit(txt, (bx + bw // 2 - txt.get_width() // 2, by - 16))


def draw_hud(window, font, font_timer, elapsed_frames=0, gems_collected=0, total_gems=0):
    ctrl = font.render(
        'Fireboy: WASD  |  Watergirl: Setas', True, (220, 220, 220))
    window.blit(ctrl, (10, 10))

    # Cronômetro grande e centralizado
    secs = elapsed_frames // FPS
    timer_txt = font_timer.render(f'{secs}s', True, AMARELO)
    window.blit(timer_txt, timer_txt.get_rect(center=(WIDTH // 2, 24)))

    # Gemas coletadas
    gems_txt = font.render(f'Gemas: {gems_collected}/{total_gems}', True, (255, 215, 50))
    window.blit(gems_txt, (WIDTH - gems_txt.get_width() - 10, 10))

    hint = font.render(
        'Alavanca abre a ponte  |  Pressione os botões juntos para abrir as portas!',
        True, (200, 220, 180))
    window.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 22))


def _draw_overlay_btn(window, text, cx, cy, font, mx, my, w=220, h=46):
    rect = pygame.Rect(cx - w // 2, cy - h // 2, w, h)
    hov  = rect.collidepoint(mx, my)
    bg   = (80, 75, 110) if hov else (45, 42, 70)
    bord = (230, 220, 255) if hov else (150, 140, 190)
    pygame.draw.rect(window, bg,   rect, border_radius=10)
    pygame.draw.rect(window, bord, rect, 2, border_radius=10)
    surf = font.render(text, True, BRANCO)
    window.blit(surf, surf.get_rect(center=rect.center))
    return rect

#Extraído com ajuda de IAg
def draw_win_screen(window, font_big, font_small, tick, mx, my,
                    grade='C', elapsed_frames=0):
    """Retorna (btn_novamente, btn_menu)."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    window.blit(overlay, (0, 0))

    if (tick // 20) % 2 == 0:
        txt = font_big.render('VOCÊS VENCERAM!', True, AMARELO)
        window.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 90)))

    grade_colors = {'A': (255, 215, 0), 'B': (180, 180, 200), 'C': (180, 110, 40)}
    grade_labels = {'A': 'NOTA A  —  INCRÍVEL!', 'B': 'NOTA B  —  BOM!',
                    'C': 'NOTA C  —  COMPLETADO!'}
    gc = grade_colors.get(grade, BRANCO)
    gl = grade_labels.get(grade, f'NOTA {grade}')
    grade_txt = font_big.render(gl, True, gc)
    window.blit(grade_txt, grade_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))

    secs = elapsed_frames // FPS
    time_txt = font_small.render(f'Tempo: {secs}s', True, (210, 210, 210))
    window.blit(time_txt, time_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 28)))

    cy_btn = HEIGHT // 2 + 80
    font_btn = pygame.font.SysFont(None, 30)
    btn_novamente = _draw_overlay_btn(
        window, 'JOGAR NOVAMENTE', WIDTH // 2 - 125, cy_btn, font_btn, mx, my, w=220, h=44)
    btn_menu = _draw_overlay_btn(
        window, 'SELECIONAR FASE', WIDTH // 2 + 125, cy_btn, font_btn, mx, my, w=220, h=44)
    return btn_novamente, btn_menu

#Extraído com ajuda de IAg
def draw_gameover_screen(window, font_big, font_small, who_died, mx, my):
    """Retorna (btn_novamente, btn_menu)."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    window.blit(overlay, (0, 0))

    txt = font_big.render(f'{who_died} morreu!', True, VERMELHO)
    window.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 55)))

    font_btn = pygame.font.SysFont(None, 30)
    cy_btn = HEIGHT // 2 + 20
    btn_novamente = _draw_overlay_btn(
        window, 'TENTAR NOVAMENTE', WIDTH // 2 - 125, cy_btn, font_btn, mx, my, w=230, h=44)
    btn_menu = _draw_overlay_btn(
        window, 'SELECIONAR FASE', WIDTH // 2 + 125, cy_btn, font_btn, mx, my, w=220, h=44)
    return btn_novamente, btn_menu


def build_level():
    all_sprites   = pygame.sprite.Group()
    platforms     = pygame.sprite.Group()
    water_pools   = pygame.sprite.Group()
    lava_pools    = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    levers_group  = pygame.sprite.Group()
    gems_group    = pygame.sprite.Group()

    def add_plat(x, y, w, color=COR_PLAT):
        p = Platform(x, y, w, color)
        platforms.add(p); all_sprites.add(p)
        return p

    def add_water(x, y, w):
        p = WaterPool(x, y, w)
        water_pools.add(p); all_sprites.add(p)

    def add_lava(x, y, w):
        p = LavaPool(x, y, w)
        lava_pools.add(p); all_sprites.add(p)

    def add_gem(x, y, color=(255, 215, 50)):
        g = Gem(x, y, color)
        gems_group.add(g); all_sprites.add(g)

    PH = POOL_HEIGHT  # alias curto

    # ── Chão ──────────────────────────────────────────────────────────────
    add_plat(0, GROUND_Y, WIDTH, COR_CHAO)

    # Poças no chão — pulável com espaço (largura ≤ 120px → distância ≤ 160px ok)
    # Água (x 230-310, 80px): Fireboy precisa pular
    add_water(230, GROUND_Y - PH, 80)
    # Lava (x 450-530, 80px): Watergirl precisa pular
    add_lava (450, GROUND_Y - PH, 80)
    # Gemas no centro de cada poça — só a cor imune consegue coletar andando
    add_gem(270, GROUND_Y - PH - 8)   # sobre água  → Watergirl
    add_gem(490, GROUND_Y - PH - 8)   # sobre lava  → Fireboy

    # ── Lado esquerdo — caminho do Fireboy ───────────────────────────────
    add_plat(0, 460, 200)   # L1
    add_plat(0, 360, 200)   # L2
    add_plat(0, 260, 160)   # L3 — próximo à porta do Fireboy

    # Poça de lava em L1 — 60px, facilmente pulável
    add_lava(70, 460 - PH, 60)
    add_gem(100, 460 - PH - 8)   # só Fireboy coleta (andando pela lava)

    # Alavanca no fim de L2 — ativa a ponte
    bridge = Bridge(x_closed=-240, x_open=200, y=360, width=240)
    platforms.add(bridge); all_sprites.add(bridge)

    lever = Lever(x=162, y=318, linked_objects=[bridge])
    levers_group.add(lever); all_sprites.add(lever)

    # Gema segura em L3
    add_gem(80, 248)

    # ── Plataforma central M (conectada pela ponte à esquerda e R2 à direita) ──
    # Quando a ponte está aberta: L2(0-200) + bridge(200-440) + M(420-640) contínuos.
    # Sem a ponte, lacuna L2→M é 220 px (> alcance máximo de pulo de ~162 px).
    add_plat(420, 360, 220)   # M

    # Poça de água em M — 50px, separando as zonas dos dois personagens
    add_water(480, 360 - PH, 50)
    add_gem(505, 360 - PH - 8)   # sobre água em M → só Watergirl coleta

    # ── Plataforma direita — caminho da Watergirl ────────────────────────
    add_plat(590, 360, 210)   # R2 — sobrepõe M em x 590-640, formando superfície contínua
    add_plat(600, 460, 200)   # R1
    add_plat(640, 260, 160)   # R3 — próximo à porta da Watergirl

    # Poça de água em R1 — 60px, facilmente pulável
    add_water(670, 460 - PH, 60)
    add_gem(700, 460 - PH - 8)   # só Watergirl coleta (andando pela água)

    # Gema segura em R3
    add_gem(720, 248)

    # ── Portas de saída ──────────────────────────────────────────────────
    door_fire  = Door(x=20,  y=205, color=(200, 60, 60), label='F')
    door_water = Door(x=745, y=205, color=(60, 60, 200), label='W')
    all_sprites.add(door_fire, door_water)

    # ── Botões na plataforma M ───────────────────────────────────────────
    btn_red  = Button(x=432, y=344, color=(200, 80, 80), linked_doors=[door_water])
    btn_blue = Button(x=565, y=344, color=(80, 80, 200), linked_doors=[door_fire])
    buttons_group.add(btn_red, btn_blue)
    all_sprites.add(btn_red, btn_blue)

    total_gems = len(gems_group)
    return (all_sprites, platforms, water_pools, lava_pools,
            buttons_group, levers_group,
            door_fire, door_water, btn_red, btn_blue,
            gems_group, total_gems)


def build_level_2():
    """Fase 2 — Caverna: lago de ácido domina o chão; jogadores cruzam para o lado oposto.

    Chão: lago de ácido verde x=140-660 — subida imediata obrigatória.
    Andar 1 (y=470): Left + plataforma móvel + Right.
    Andar 2 (y=380): Left [alavanca] + Ponte → Right (maior, com perigos).
    Andar 3 (y=290): Left3 | Center3 [botões / ácido entre eles] | Right3.
    Portas: Watergirl à esquerda (y=230), Fireboy à direita (y=230).
    Puzzle: Fireboy vem da esquerda, pressiona btn_red (abre porta da Watergirl à esquerda).
            Watergirl vem da direita, pressiona btn_blue (abre porta do Fireboy à direita).
            Depois ambos cruzam o ácido para entrar na porta do lado oposto.
    """
    all_sprites   = pygame.sprite.Group()
    platforms     = pygame.sprite.Group()
    water_pools   = pygame.sprite.Group()
    lava_pools    = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    levers_group  = pygame.sprite.Group()
    gems_group    = pygame.sprite.Group()

    COR_CAVE = (50, 40, 75)
    COR_DARK = (35, 28, 55)

    def add_plat(x, y, w, color=COR_CAVE):
        p = Platform(x, y, w, color)
        platforms.add(p); all_sprites.add(p); return p

    def add_water(x, y, w):
        p = WaterPool(x, y, w); water_pools.add(p); all_sprites.add(p)

    def add_lava(x, y, w):
        p = LavaPool(x, y, w); lava_pools.add(p); all_sprites.add(p)

    def add_green(x, y, w):
        p = GreenPool(x, y, w)
        water_pools.add(p); lava_pools.add(p); all_sprites.add(p)

    def add_gem(x, y, color=(140, 220, 255)):
        g = Gem(x, y, color); gems_group.add(g); all_sprites.add(g)

    PH = POOL_HEIGHT

    # ── Chão — lago de ácido verde domina o centro ────────────────────────
    add_plat(0, GROUND_Y, WIDTH, COR_DARK)
    add_green(140, GROUND_Y - PH, 520)   # ácido x=140-660

    # ── Andar 1 (y=470) ───────────────────────────────────────────────────
    add_plat(0, 470, 200, COR_CAVE)       # Left1
    add_plat(610, 470, 190, COR_CAVE)     # Right1
    add_lava(30, 470 - PH, 70)
    add_gem(65, 470 - PH - 8, (255, 140, 100))
    add_water(650, 470 - PH, 70)
    add_gem(685, 470 - PH - 8)
    mp1 = MovingPlatform(210, 470, 100, end_x=500, speed=2, color=(65, 52, 95))
    platforms.add(mp1); all_sprites.add(mp1)
    add_gem(355, 438)

    # ── Andar 2 (y=380): Left2 [alavanca] + Ponte + Right2 ───────────────
    add_plat(0, 380, 240, COR_CAVE)       # Left2
    add_plat(455, 380, 345, COR_CAVE)     # Right2 (largo)
    add_water(510, 380 - PH, 70)
    add_green(630, 380 - PH, 70)
    add_gem(110, 348)
    add_gem(740, 348, (255, 140, 100))

    bridge = Bridge(x_closed=-240, x_open=240, y=380, width=240)
    platforms.add(bridge); all_sprites.add(bridge)
    lever = Lever(x=192, y=338, linked_objects=[bridge])
    levers_group.add(lever); all_sprites.add(lever)

    # ── Andar 3 (y=290): Left3 | Center3 [botões] | Right3 ───────────────
    add_plat(0, 290, 210, COR_CAVE)       # Left3
    add_plat(260, 290, 280, COR_CAVE)     # Center3 (botões aqui)
    add_plat(580, 290, 220, COR_CAVE)     # Right3
    add_green(300, 290 - PH, 200)         # ácido largo entre botões (200px — intransponível)
    add_gem(80, 258)
    add_gem(700, 258, (255, 140, 100))

    # Portas trocadas: Watergirl à esquerda, Fireboy à direita
    door_water = Door(x=20,  y=230, color=(60, 60, 200), label='W')
    door_fire  = Door(x=742, y=230, color=(200, 60, 60), label='F')
    all_sprites.add(door_fire, door_water)

    btn_red  = Button(x=262, y=274, color=(200, 80, 80), linked_doors=[door_water])
    btn_blue = Button(x=502, y=274, color=(80, 80, 200), linked_doors=[door_fire])
    buttons_group.add(btn_red, btn_blue); all_sprites.add(btn_red, btn_blue)

    total_gems = len(gems_group)
    return (all_sprites, platforms, water_pools, lava_pools,
            buttons_group, levers_group,
            door_fire, door_water, btn_red, btn_blue,
            gems_group, total_gems)


def build_level_3():
    """Fase 3 — Vulcão: labirinto de corredores horizontais + ponte vertical.

    Estrutura em 3 corredores (A, B, C) em vez de torre vertical.
    Chão: quase inteiramente perigoso (lava + ácido + água).
    Corredor A (y=470): dois lados + plataforma móvel obrigatória.
    Corredor B (y=370): alavanca ativa Ponte horizontal E Ponte Vertical.
      - Ponte: conecta B-Left a B-Right (gap intransponível sem ela).
      - Ponte Vertical: sobe de y=370 para y=270 — cria acesso ao Corredor C.
    Corredor C (y=270): botões separados por ácido; portas nos extremos.
    Puzzle: mesma lógica de cruzamento — pressionar botão no lado oposto, depois ir à porta.
    """
    all_sprites   = pygame.sprite.Group()
    platforms     = pygame.sprite.Group()
    water_pools   = pygame.sprite.Group()
    lava_pools    = pygame.sprite.Group()
    buttons_group = pygame.sprite.Group()
    levers_group  = pygame.sprite.Group()
    gems_group    = pygame.sprite.Group()

    COR_VOLC = (80, 35, 15)
    COR_DARK = (65, 22, 8)

    def add_plat(x, y, w, color=COR_VOLC):
        p = Platform(x, y, w, color)
        platforms.add(p); all_sprites.add(p); return p

    def add_water(x, y, w):
        p = WaterPool(x, y, w); water_pools.add(p); all_sprites.add(p)

    def add_lava(x, y, w):
        p = LavaPool(x, y, w); lava_pools.add(p); all_sprites.add(p)

    def add_green(x, y, w):
        p = GreenPool(x, y, w)
        water_pools.add(p); lava_pools.add(p); all_sprites.add(p)

    def add_gem(x, y, color=(255, 160, 50)):
        g = Gem(x, y, color); gems_group.add(g); all_sprites.add(g)

    PH = POOL_HEIGHT

    # ── Chão — quase inteiramente perigoso ────────────────────────────────
    add_plat(0, GROUND_Y, WIDTH, COR_DARK)
    add_lava(70, GROUND_Y - PH, 240)      # x=70-310
    add_green(310, GROUND_Y - PH, 230)    # x=310-540
    add_water(540, GROUND_Y - PH, 190)    # x=540-730

    # ── Corredor A (y=470): duas metades + plat. móvel obrigatória ────────
    add_plat(0, 470, 250, COR_VOLC)       # A-Left
    add_plat(500, 470, 300, COR_VOLC)     # A-Right
    add_lava(30, 470 - PH, 90)
    add_gem(75, 470 - PH - 8, (255, 120, 60))
    add_water(670, 470 - PH, 80)
    add_gem(710, 470 - PH - 8, (140, 220, 255))
    mp1 = MovingPlatform(260, 470, 110, end_x=490, speed=3, color=(110, 45, 15))
    platforms.add(mp1); all_sprites.add(mp1)
    add_gem(350, 438, (255, 220, 80))

    # ── Corredor B (y=370): alavanca ativa ponte + ponte vertical ─────────
    add_plat(0, 370, 320, COR_VOLC)       # B-Left (x=0-320)
    add_plat(540, 370, 260, COR_VOLC)     # B-Right (x=540-800)

    # Ponte Vertical: sobe de B (y=370) ao Corredor C (y=270)
    # Quando ativa, cria plataforma em y=270 → jogadores saltam do Corredor B para C
    vbridge = VerticalBridge(x=110, y_closed=370, y_open=270, width=90)
    platforms.add(vbridge); all_sprites.add(vbridge)

    # Ponte horizontal: quando aberta abrange x=320-600 → conecta B-Left a B-Right
    bridge = Bridge(x_closed=-320, x_open=320, y=370, width=280)
    platforms.add(bridge); all_sprites.add(bridge)

    lever = Lever(x=266, y=328, linked_objects=[bridge, vbridge])
    levers_group.add(lever); all_sprites.add(lever)

    add_lava(30, 370 - PH, 70)           # lava em B-Left (Fireboy passa)
    add_green(560, 370 - PH, 80)         # ácido em B-Right (ambos evitam)
    add_gem(150, 338)
    add_gem(680, 338, (140, 220, 255))

    # ── Corredor C (y=270): botões e portas ───────────────────────────────
    add_plat(0, 270, 220, COR_VOLC)      # C-Left (VBridge chega aqui)
    add_plat(280, 270, 270, COR_VOLC)    # C-Center (botões)
    add_plat(610, 270, 190, COR_VOLC)    # C-Right

    add_green(340, 270 - PH, 170)        # ácido largo entre botões (intransponível)
    add_lava(30, 270 - PH, 70)           # C-Left (Fireboy passa)
    add_water(640, 270 - PH, 70)         # C-Right (Watergirl passa)
    add_gem(80, 238)
    add_gem(720, 238, (140, 220, 255))

    # Portas no topo de C-Left e C-Right
    door_fire  = Door(x=20,  y=210, color=(200, 60, 60), label='F')
    door_water = Door(x=750, y=210, color=(60, 60, 200), label='W')
    all_sprites.add(door_fire, door_water)

    # btn_red (x=288) à esquerda do ácido → Fireboy pressiona, abre porta da Watergirl (direita)
    # btn_blue (x=508) à direita do ácido → Watergirl pressiona, abre porta do Fireboy (esquerda)
    # Após pressionar: ambos cruzam C para entrar nas portas do lado oposto
    btn_red  = Button(x=288, y=254, color=(200, 80, 80), linked_doors=[door_water])
    btn_blue = Button(x=508, y=254, color=(80, 80, 200), linked_doors=[door_fire])
    buttons_group.add(btn_red, btn_blue); all_sprites.add(btn_red, btn_blue)

    total_gems = len(gems_group)
    return (all_sprites, platforms, water_pools, lava_pools,
            buttons_group, levers_group,
            door_fire, door_water, btn_red, btn_blue,
            gems_group, total_gems)



_LEVEL_BUILDERS = {
    1: (build_level,   make_forest_bg),
    2: (build_level_2, make_cave_bg),
    3: (build_level_3, make_volcano_bg),
}


def game_screen(window, level=1):
    clock = pygame.time.Clock()

    font_big   = pygame.font.SysFont(None, 64)
    font_small = pygame.font.SysFont(None, 28)
    font_hud   = pygame.font.SysFont(None, 22)
    font_timer = pygame.font.SysFont(None, 48)

    build_fn, bg_fn = _LEVEL_BUILDERS.get(level, _LEVEL_BUILDERS[1])
    bg = bg_fn()

    def reset():
        (all_sprites, platforms, water_pools, lava_pools,
         buttons_group, levers_group,
         door_fire, door_water, btn_red, btn_blue,
         gems_group, total_gems) = build_fn()

        fb_ctrl = {'left': pygame.K_a, 'right': pygame.K_d, 'jump': pygame.K_w}
        wg_ctrl = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'jump': pygame.K_UP}

        fireboy   = Player(platforms, x=40,  y=510, color=(220, 60, 60),
                           controls=fb_ctrl, player_type='boy')
        watergirl = Player(platforms, x=750, y=510, color=(60, 60, 220),
                           controls=wg_ctrl, player_type='girl')
        all_sprites.add(fireboy, watergirl)

        return (all_sprites, water_pools, lava_pools,
                buttons_group, levers_group,
                door_fire, door_water, btn_red, btn_blue,
                fireboy, watergirl,
                gems_group, total_gems)

    (all_sprites, water_pools, lava_pools,
     buttons_group, levers_group,
     door_fire, door_water, btn_red, btn_blue,
     fireboy, watergirl,
     gems_group, total_gems) = reset()

    state          = GAME
    game_state     = 'playing'
    dead_who       = ''
    tick           = 0
    elapsed_frames = 0
    gems_collected = 0
    grade          = 'C'
    overlay_btns   = (None, None)   # (btn_novamente, btn_menu)

    def do_reset():
        nonlocal game_state, tick, elapsed_frames, gems_collected, grade
        nonlocal all_sprites, water_pools, lava_pools, buttons_group, levers_group
        nonlocal door_fire, door_water, btn_red, btn_blue, fireboy, watergirl
        nonlocal gems_group, total_gems
        (all_sprites, water_pools, lava_pools,
         buttons_group, levers_group,
         door_fire, door_water, btn_red, btn_blue,
         fireboy, watergirl,
         gems_group, total_gems) = reset()
        game_state     = 'playing'
        tick           = 0
        elapsed_frames = 0
        gems_collected = 0
        grade          = 'C'

    while state != QUIT:
        clock.tick(FPS)
        tick += 1
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = LEVEL_SELECT

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state in ('win', 'dead'):
                    btn_nov, btn_men = overlay_btns
                    if btn_nov and btn_nov.collidepoint(mx, my):
                        do_reset()
                    elif btn_men and btn_men.collidepoint(mx, my):
                        state = LEVEL_SELECT

            if game_state == 'playing':
                fireboy.handle_event(event)
                watergirl.handle_event(event)

        if state == LEVEL_SELECT:
            break

        if game_state == 'playing':
            elapsed_frames += 1
            all_sprites.update()

            # Alavancas verificam contato com jogadores
            for lev in levers_group:
                lev.check_contact([fireboy, watergirl])

            # Botões atualizam temporizador e portais
            for btn in buttons_group:
                btn.check_press([fireboy, watergirl])

            # Coleta de gemas
            before = len(gems_group)
            pygame.sprite.spritecollide(fireboy,   gems_group, True)
            pygame.sprite.spritecollide(watergirl, gems_group, True)
            gems_collected += before - len(gems_group)

            # Morre apenas quando estiver no chão — permite pular por cima das poças
            if fireboy.on_ground and pygame.sprite.spritecollide(fireboy, water_pools, False):
                game_state = 'dead'
                dead_who   = 'Fireboy'
            if watergirl.on_ground and pygame.sprite.spritecollide(watergirl, lava_pools, False):
                game_state = 'dead'
                dead_who   = 'Watergirl'

            # Vitória: ambos dentro das suas portas abertas
            fb_in = door_fire.open  and fireboy.rect.colliderect(door_fire.rect)
            wg_in = door_water.open and watergirl.rect.colliderect(door_water.rect)
            if fb_in and wg_in:
                time_ok  = elapsed_frames < 20 * FPS   # menos de 20 segundos
                all_gems = gems_collected >= total_gems
                if time_ok and all_gems:
                    grade = 'A'
                elif time_ok or all_gems:
                    grade = 'B'
                else:
                    grade = 'C'
                game_state = 'win'

        # ── Desenha ───────────────────────────────────────────────────
        window.blit(bg, (0, 0))
        all_sprites.draw(window)

        # Barras de temporizador sobre as portas
        draw_timer_bars(window,
                        [btn_red,  btn_blue],
                        [door_water, door_fire],
                        font_hud)
        draw_hud(window, font_hud, font_timer, elapsed_frames, gems_collected, total_gems)

        if game_state == 'win':
            overlay_btns = draw_win_screen(
                window, font_big, font_small, tick, mx, my, grade, elapsed_frames)
        elif game_state == 'dead':
            overlay_btns = draw_gameover_screen(
                window, font_big, font_small, dead_who, mx, my)
        else:
            overlay_btns = (None, None)

        pygame.display.flip()

    return state