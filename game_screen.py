# -*- coding: utf-8 -*-

import pygame
import math
from config import *
from sprites import *

GROUND_Y = HEIGHT - 40   # y do topo do chão
COR_CHAO = (75, 50, 22)
COR_PLAT = (115, 78, 38)

# ──────────────────────────────────────────────────────────────────────────────
# Layout do nível
#
#  [F-Door]                          [W-Door]
#  [L3: 0-180, y=260]      [R3: 620-800, y=260]
#
#  [L2: 0-180]  [Bridge→]  [M: 380-600] [R2: 600-800]  y=360
#  [Lever on L2]           [BtnW][BtnF]
#
#  [L1: 0-180]                         [R1: 620-800]  y=460
#
#  [Gnd-L]  [Water 190-390]  [Gnd-M]  [Lava 410-610]  [Gnd-R]   y=560
#
# Puzzle: Fireboy toca a alavanca → ponte desliza → ambos vão para M →
#  Fireboy pisa no botão vermelho (abre porta da Watergirl),
#  Watergirl pisa no botão azul (abre porta do Fireboy).
#  Temporizador de 6s: após soltar o botão o portal ainda fica aberto 6s.
# ──────────────────────────────────────────────────────────────────────────────


def make_forest_bg():
    """Pré-renderiza o fundo de floresta uma única vez."""
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


def draw_hud(window, font, elapsed_frames=0, gems_collected=0, total_gems=0):
    ctrl = font.render(
        'Fireboy: WASD  |  Watergirl: Setas  |  ESC: Menu', True, (220, 220, 220))
    window.blit(ctrl, (10, 10))

    # Cronômetro
    secs = elapsed_frames // FPS
    timer_txt = font.render(f'Tempo: {secs}s', True, AMARELO)
    window.blit(timer_txt, (WIDTH - timer_txt.get_width() - 10, 10))

    # Gemas coletadas
    gems_txt = font.render(f'Gemas: {gems_collected}/{total_gems}', True, (255, 215, 50))
    window.blit(gems_txt, (WIDTH - gems_txt.get_width() - 10, 28))

    hint = font.render(
        'Ative a alavanca → cruze a ponte → pressione os botoes juntos!',
        True, (200, 220, 180))
    window.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT - 22))


def draw_win_screen(window, font_big, font_small, tick, grade='C', elapsed_frames=0):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    window.blit(overlay, (0, 0))

    if (tick // 20) % 2 == 0:
        txt = font_big.render('VOCES VENCERAM!', True, AMARELO)
        window.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70)))

    grade_colors = {'A': (255, 215, 0), 'B': (180, 180, 200), 'C': (180, 110, 40)}
    grade_labels = {'A': 'NOTA A  — INCRIVEL!', 'B': 'NOTA B  — BOM!', 'C': 'NOTA C  — COMPLETADO!'}
    gc = grade_colors.get(grade, BRANCO)
    gl = grade_labels.get(grade, f'NOTA {grade}')
    grade_txt = font_big.render(gl, True, gc)
    window.blit(grade_txt, grade_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    secs = elapsed_frames // FPS
    time_txt = font_small.render(f'Tempo: {secs}s', True, BRANCO)
    window.blit(time_txt, time_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 44)))

    sub = font_small.render(
        'ESPACO para jogar novamente  |  ESC para sair', True, BRANCO)
    window.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))


def draw_gameover_screen(window, font_big, font_small, who_died):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    window.blit(overlay, (0, 0))
    txt = font_big.render(f'{who_died} morreu!', True, VERMELHO)
    window.blit(txt, txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30)))
    sub = font_small.render(
        'ESPACO para tentar novamente  |  ESC para sair', True, BRANCO)
    window.blit(sub, sub.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))


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


def game_screen(window):
    clock = pygame.time.Clock()

    font_big   = pygame.font.SysFont(None, 64)
    font_small = pygame.font.SysFont(None, 28)
    font_hud   = pygame.font.SysFont(None, 22)

    bg = make_forest_bg()

    def reset():
        (all_sprites, platforms, water_pools, lava_pools,
         buttons_group, levers_group,
         door_fire, door_water, btn_red, btn_blue,
         gems_group, total_gems) = build_level()

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

    while state != QUIT:
        clock.tick(FPS)
        tick += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = QUIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = INIT
                if event.key == pygame.K_SPACE:
                    if game_state in ('win', 'dead'):
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

            if game_state == 'playing':
                fireboy.handle_event(event)
                watergirl.handle_event(event)

        if state == INIT:
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
        draw_hud(window, font_hud, elapsed_frames, gems_collected, total_gems)

        if game_state == 'win':
            draw_win_screen(window, font_big, font_small, tick, grade, elapsed_frames)
        elif game_state == 'dead':
            draw_gameover_screen(window, font_big, font_small, dead_who)

        pygame.display.flip()

    return state
