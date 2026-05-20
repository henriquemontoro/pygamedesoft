# -*- coding: utf-8 -*-

import pygame
import math
from config import *

POOL_HEIGHT = 16   # altura das poças (recesso raso no chão)
CLOSE_DELAY = 180  # frames antes do portal fechar (6 s a 30 fps)


def draw_player_sprite(surface, color, player_type):
    """'boy' para Fireboy, 'girl' para Watergirl. Surface: 40x50px."""
    surface.fill((0, 0, 0, 0))
    dark  = tuple(max(0,   c - 70) for c in color)
    light = tuple(min(255, c + 80) for c in color)

    if player_type == 'girl':
        # Pernas finas
        pygame.draw.rect(surface, dark, (12, 36, 7, 14))
        pygame.draw.rect(surface, dark, (21, 36, 7, 14))
        # Saia (trapézio)
        skirt = tuple(max(0, c - 25) for c in color)
        pygame.draw.polygon(surface, skirt, [(8, 33), (32, 33), (36, 50), (4, 50)])
        # Corpo estreito
        pygame.draw.rect(surface, color, (14, 20, 12, 16))
        # Braços finos
        pygame.draw.rect(surface, dark, (6,  21, 8, 12))
        pygame.draw.rect(surface, dark, (26, 21, 8, 12))
        # Cabelo (atrás, mais escuro)
        hair = tuple(max(0, c - 110) for c in color)
        pygame.draw.circle(surface, hair, (20, 11), 13)
        # Rabo de cavalo (direita)
        pygame.draw.polygon(surface, hair, [(30, 7), (40, 1), (40, 21), (30, 17)])
        # Rosto
        pygame.draw.circle(surface, light, (20, 11), 10)
        # Olhos grandes
        pygame.draw.ellipse(surface, BRANCO, (8,  7, 9, 8))
        pygame.draw.ellipse(surface, BRANCO, (23, 7, 9, 8))
        eye_col = (20, 20, 160)
        pygame.draw.circle(surface, eye_col, (12, 11), 3)
        pygame.draw.circle(surface, eye_col, (27, 11), 3)
        pygame.draw.circle(surface, BRANCO, (13, 10), 1)
        pygame.draw.circle(surface, BRANCO, (28, 10), 1)
        # Cílios
        for bx in [8, 11, 14]:
            pygame.draw.line(surface, PRETO, (bx, 7), (bx - 1, 3), 1)
        for bx in [23, 26, 29]:
            pygame.draw.line(surface, PRETO, (bx, 7), (bx + 1, 3), 1)
        # Boca (sorriso)
        pygame.draw.arc(surface, (220, 120, 150),
                        (13, 16, 14, 7), math.pi, 2 * math.pi, 2)
        # Franja
        pygame.draw.ellipse(surface, hair, (9, 0, 9, 9))
        pygame.draw.ellipse(surface, hair, (16, -1, 9, 7))

    else:
        # Pernas grossas
        pygame.draw.rect(surface, dark, (9, 34, 10, 16))
        pygame.draw.rect(surface, dark, (21, 34, 10, 16))
        # Corpo largo (ombros largos → trapézio)
        pygame.draw.polygon(surface, color, [(5, 20), (35, 20), (30, 42), (10, 42)])
        # Braços largos
        pygame.draw.rect(surface, dark, (0,  21, 7, 15))
        pygame.draw.rect(surface, dark, (33, 21, 7, 15))
        # Chamas no cabelo (antes da cabeça para ficarem atrás)
        flame = tuple(min(255, c + 50) for c in color)
        pts_outer = [(8, 4), (12, -8), (17, 2), (20, -10), (23, 2), (28, -8), (32, 4)]
        pygame.draw.polygon(surface, flame, pts_outer)
        pts_inner = [(13, 4), (17, -3), (20, 0), (23, -3), (27, 4)]
        pygame.draw.polygon(surface, AMARELO, pts_inner)
        # Cabeça sobre as chamas
        pygame.draw.circle(surface, light, (20, 12), 11)
        # Sobrancelhas franzidas
        pygame.draw.line(surface, PRETO, (10, 7), (17, 9), 2)
        pygame.draw.line(surface, PRETO, (23, 9), (30, 7), 2)
        # Olhos sérios
        pygame.draw.circle(surface, BRANCO, (15, 13), 4)
        pygame.draw.circle(surface, BRANCO, (25, 13), 4)
        pygame.draw.circle(surface, PRETO, (16, 13), 2)
        pygame.draw.circle(surface, PRETO, (26, 13), 2)
        # Boca fechada/séria
        pygame.draw.line(surface, PRETO, (15, 20), (25, 20), 2)


class Player(pygame.sprite.Sprite):

    def __init__(self, platforms, x, y, color, controls, player_type='boy'):
        pygame.sprite.Sprite.__init__(self)

        self.color      = color
        self.player_type = player_type
        self.image      = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        draw_player_sprite(self.image, color, player_type)
        self.rect       = self.image.get_rect()
        self.rect.x     = x
        self.rect.y     = y

        self.vel_x      = 0
        self.vel_y      = 0
        self.controls   = controls
        self.platforms  = platforms
        self.on_ground  = False
        self._prev_jump = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Movimento horizontal — resposta imediata frame a frame
        if keys[self.controls['left']]:
            self.vel_x = -VELOCIDADE_MOVIMENTO
        elif keys[self.controls['right']]:
            self.vel_x = VELOCIDADE_MOVIMENTO
        else:
            self.vel_x = 0

        # Pulo por borda de subida: dispara ao pressionar, mesmo andando
        jump_now = keys[self.controls['jump']]
        if jump_now and not self._prev_jump and self.on_ground:
            self.vel_y = VELOCIDADE_PULO
        self._prev_jump = jump_now

        self.vel_y += GRAVIDADE
        if self.vel_y > 15:
            self.vel_y = 15

        # ── Movimento vertical ──────────────────────────────────────────
        # int(0.8)==0 faz o player flutuar 1 frame acima do chão → on_ground
        # alterna True/False. Garantir mínimo de 1px ao cair resolve isso.
        dy = int(self.vel_y)
        if self.vel_y > 0 and dy == 0:
            dy = 1
        self.rect.y    += dy
        self.on_ground  = False

        for hit in pygame.sprite.spritecollide(self, self.platforms, False):
            if self.vel_y > 0:
                self.rect.bottom  = hit.rect.top
                self.vel_y        = 0
                self.on_ground    = True
                self._prev_jump   = False
                # Plataformas móveis: arrasta o player horizontalmente
                if hasattr(hit, 'dx') and hit.dx:
                    self.rect.x += hit.dx
                    if self.rect.left  < 0:     self.rect.left  = 0
                    if self.rect.right > WIDTH: self.rect.right = WIDTH

        # ── Movimento horizontal ─────────────────────────────────────────
        self.rect.x += self.vel_x

        if self.rect.left  < 0:      self.rect.left  = 0
        if self.rect.right > WIDTH:  self.rect.right = WIDTH

        if self.rect.top > HEIGHT + 50:
            self.rect.y = -PLAYER_HEIGHT

    def handle_event(self, event):
        pass  # tudo resolvido via get_pressed() em update()


class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, width, color=CINZA):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((width, PLATFORM_HEIGHT))
        self.image.fill(color)
        top = tuple(min(255, c + 50) for c in color)
        pygame.draw.line(self.image, top, (0, 0), (width, 0), 3)
        grain = tuple(max(0, c - 15) for c in color)
        for gx in range(20, width, 20):
            pygame.draw.line(self.image, grain, (gx, 2), (gx, PLATFORM_HEIGHT), 1)

        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class MovingPlatform(Platform):
    """Plataforma que oscila horizontalmente ou verticalmente entre dois pontos."""

    def __init__(self, x, y, width, *, end_x=None, end_y=None, speed=2, color=CINZA):
        super().__init__(x, y, width, color)
        self.start_x = x
        self.start_y = y
        self.end_x   = x if end_x is None else end_x
        self.end_y   = y if end_y is None else end_y
        self.speed   = speed
        self._dir    = 1
        self.dx      = 0   # deslocamento horizontal neste frame (para arrastar o player)

    def update(self):
        old_x = self.rect.x

        if self.end_x != self.start_x:
            self.rect.x += self.speed * self._dir
            if self._dir == 1 and self.rect.x >= self.end_x:
                self.rect.x = self.end_x;  self._dir = -1
            elif self._dir == -1 and self.rect.x <= self.start_x:
                self.rect.x = self.start_x; self._dir = 1

        if self.end_y != self.start_y:
            self.rect.y += self.speed * self._dir
            if self._dir == 1 and self.rect.y >= self.end_y:
                self.rect.y = self.end_y;  self._dir = -1
            elif self._dir == -1 and self.rect.y <= self.start_y:
                self.rect.y = self.start_y; self._dir = 1

        self.dx = self.rect.x - old_x


class Bridge(Platform):
    """Ponte deslizante ativada por uma alavanca."""
    SPEED = 12

    def __init__(self, x_closed, x_open, y, width):
        color = (145, 95, 42)
        super().__init__(x_closed, y, width, color)
        # Desenha setas na ponte para indicar que é especial
        mid_y = PLATFORM_HEIGHT // 2
        for ax in range(8, width - 8, 24):
            pygame.draw.polygon(self.image, (200, 160, 80),
                                [(ax, mid_y), (ax + 8, mid_y - 4), (ax + 8, mid_y + 4)])

        self.x_closed  = x_closed
        self.x_open    = x_open
        self._target_x = x_closed

    def activate(self, state):
        self._target_x = self.x_open if state else self.x_closed

    def update(self):
        if self.rect.x < self._target_x:
            self.rect.x = min(self.rect.x + self.SPEED, self._target_x)
        elif self.rect.x > self._target_x:
            self.rect.x = max(self.rect.x - self.SPEED, self._target_x)


class VerticalBridge(Platform):
    """Plataforma que desliza verticalmente ao ser ativada por alavanca.
    Cria um degrau/elevador quando acionada."""
    SPEED = 8

    def __init__(self, x, y_closed, y_open, width):
        color = (130, 85, 35)
        super().__init__(x, y_closed, width, color)
        # Linhas horizontais indicam movimento vertical
        for iy in range(3, PLATFORM_HEIGHT - 2, 4):
            pygame.draw.line(self.image, (200, 160, 80), (4, iy), (width - 4, iy), 1)
        # Setas apontando para cima
        cx = width // 2
        pygame.draw.polygon(self.image, (220, 190, 90),
                            [(cx, 1), (cx - 5, 8), (cx + 5, 8)])
        self.y_closed  = y_closed
        self.y_open    = y_open
        self._target_y = y_closed

    def activate(self, state):
        self._target_y = self.y_open if state else self.y_closed

    def update(self):
        if self.rect.y < self._target_y:
            self.rect.y = min(self.rect.y + self.SPEED, self._target_y)
        elif self.rect.y > self._target_y:
            self.rect.y = max(self.rect.y - self.SPEED, self._target_y)


class WaterPool(pygame.sprite.Sprite):

    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self._width = width
        self._tick  = 0
        self.image  = pygame.Surface((width, POOL_HEIGHT))
        self._draw()
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _draw(self):
        w, h = self._width, POOL_HEIGHT
        surf = self.image
        # Gradiente azul-profundo
        for y in range(h):
            t = y / max(1, h - 1)
            pygame.draw.line(surf,
                             (int(t * 5), int(145 - t * 55), int(240 - t * 65)),
                             (0, y), (w, y))
        # Ondas na superfície
        off = self._tick % 20
        for x0 in range(-20, w + 20, 20):
            x1 = x0 + off
            pygame.draw.arc(surf, (170, 235, 255), (x1, 0, 16, 6), 0, math.pi, 1)
        # Brilhos
        for i, sx in enumerate(range(8, w - 8, 28)):
            phase = (self._tick + i * 7) % 14
            if phase < 7:
                pygame.draw.circle(surf, (225, 250, 255), (sx, 3 + phase % 3), 1)
        # Borda superior
        pygame.draw.line(surf, (200, 245, 255), (0, 0), (w, 0), 1)

    def update(self):
        self._tick += 1
        if self._tick % 3 == 0:
            self._draw()


class LavaPool(pygame.sprite.Sprite):

    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self._width = width
        self._tick  = 0
        self.image  = pygame.Surface((width, POOL_HEIGHT))
        self._draw()
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _draw(self):
        w, h = self._width, POOL_HEIGHT
        surf = self.image
        # Gradiente laranja-vermelho
        for y in range(h):
            t = y / max(1, h - 1)
            pygame.draw.line(surf,
                             (int(255 - t * 70), int(120 - t * 100), 0),
                             (0, y), (w, y))
        # Ondas de superfície
        off = self._tick % 20
        for x0 in range(-20, w + 20, 20):
            x1 = x0 + off
            pygame.draw.arc(surf, (255, 70, 0), (x1, 0, 14, 6), 0, math.pi, 2)
        # Bolhas subindo
        for i, bx in enumerate(range(15, w - 15, 28)):
            phase = (self._tick + i * 11) % 20
            by = h - 2 - int(phase * (h - 4) / 20)
            if 1 < by < h:
                pygame.draw.circle(surf, (255, 200, 30), (bx, by), 2)
        # Brilho no topo
        pygame.draw.line(surf, (255, 220, 60), (0, 0), (w, 0), 2)

    def update(self):
        self._tick += 1
        if self._tick % 3 == 0:
            self._draw()


class GreenPool(pygame.sprite.Sprite):
    """Piscina de ácido verde — mata AMBOS os jogadores."""

    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        self._width = width
        self._tick  = 0
        self.image  = pygame.Surface((width, POOL_HEIGHT))
        self._draw()
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _draw(self):
        w, h = self._width, POOL_HEIGHT
        surf = self.image
        for y in range(h):
            t = y / max(1, h - 1)
            pygame.draw.line(surf,
                             (int(10 + t * 15), int(165 - t * 55), int(10 + t * 15)),
                             (0, y), (w, y))
        off = self._tick % 20
        for x0 in range(-20, w + 20, 20):
            x1 = x0 + off
            pygame.draw.arc(surf, (90, 240, 90), (x1, 0, 14, 6), 0, math.pi, 2)
        for i, bx in enumerate(range(15, w - 15, 28)):
            phase = (self._tick + i * 11) % 20
            by = h - 2 - int(phase * (h - 4) / 20)
            if 1 < by < h:
                pygame.draw.circle(surf, (160, 255, 80), (bx, by), 2)
        pygame.draw.line(surf, (130, 255, 100), (0, 0), (w, 0), 2)

    def update(self):
        self._tick += 1
        if self._tick % 3 == 0:
            self._draw()


class PushBlock(pygame.sprite.Sprite):
    """Caixa de madeira empurrável. Jogadores podem empurrá-la para alcançar lugares mais altos."""
    SIZE = 36

    def __init__(self, x, y, platforms):
        super().__init__()
        s = self.SIZE
        self.image = pygame.Surface((s, s))
        self.image.fill((139, 90, 43))
        pygame.draw.rect(self.image, (90, 58, 18), (0, 0, s, s), 3)
        for gx in [s // 3, 2 * s // 3]:
            pygame.draw.line(self.image, (108, 68, 26), (gx, 3), (gx, s - 3), 1)
        pygame.draw.line(self.image, (108, 68, 26), (3, s // 2), (s - 3, s // 2), 1)
        pygame.draw.line(self.image, (185, 135, 75), (2, 2), (s - 3, 2), 1)
        pygame.draw.line(self.image, (185, 135, 75), (2, 2), (2, s - 3), 1)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.on_ground = False
        self.dx = 0
        self._platforms = platforms

    def update(self):
        self.vel_y = min(self.vel_y + GRAVIDADE, 15)
        dy = int(self.vel_y)
        if self.vel_y > 0 and dy == 0:
            dy = 1
        self.rect.y += dy
        self.on_ground = False
        for hit in pygame.sprite.spritecollide(self, self._platforms, False):
            if hit is self:
                continue
            if self.vel_y >= 0:
                self.rect.bottom = hit.rect.top
                self.vel_y = 0
                self.on_ground = True

    def try_push(self, dx):
        self.rect.x += dx
        if self.rect.left < 0:
            self.rect.left = 0
            return
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            return
        for hit in pygame.sprite.spritecollide(self, self._platforms, False):
            if hit is self:
                continue
            if dx > 0:
                self.rect.right = hit.rect.left
            else:
                self.rect.left = hit.rect.right


class Door(pygame.sprite.Sprite):

    DOOR_WIDTH  = 40
    DOOR_HEIGHT = 60

    def __init__(self, x, y, color, label):
        pygame.sprite.Sprite.__init__(self)
        self.color  = color
        self.label  = label
        self.open   = False
        self.image  = pygame.Surface((self.DOOR_WIDTH, self.DOOR_HEIGHT), pygame.SRCALPHA)
        self._draw()
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        frame = tuple(min(255, c + 30) for c in self.color)
        if self.open:
            pygame.draw.rect(self.image, frame,
                             (0, 0, self.DOOR_WIDTH, self.DOOR_HEIGHT), 4)
            glow = tuple(min(255, c + 80) for c in self.color)
            pygame.draw.rect(self.image, glow,
                             (6, 6, self.DOOR_WIDTH - 12, self.DOOR_HEIGHT - 12), 2)
        else:
            pygame.draw.rect(self.image, self.color,
                             (0, 0, self.DOOR_WIDTH, self.DOOR_HEIGHT))
            pygame.draw.rect(self.image, frame,
                             (0, 0, self.DOOR_WIDTH, self.DOOR_HEIGHT), 3)
            pygame.draw.circle(self.image, AMARELO,
                                (self.DOOR_WIDTH - 8, self.DOOR_HEIGHT // 2), 4)
        font = pygame.font.SysFont(None, 22)
        txt  = font.render(self.label, True, BRANCO)
        self.image.blit(txt, (self.DOOR_WIDTH // 2 - txt.get_width() // 2, 4))

    def set_open(self, state):
        if self.open != state:
            self.open = state
            self._draw()


class Button(pygame.sprite.Sprite):
    """Botão de pressão. Portal fica aberto por CLOSE_DELAY frames após soltar."""

    BTN_WIDTH  = 36
    BTN_HEIGHT = 16

    def __init__(self, x, y, color, linked_doors):
        pygame.sprite.Sprite.__init__(self)
        self.color        = color
        self.linked_doors = linked_doors
        self._phys        = False   # player fisicamente em cima
        self._timer       = 0       # contagem regressiva pós-soltar
        self._doors_open  = False
        self.image        = pygame.Surface((self.BTN_WIDTH, self.BTN_HEIGHT), pygame.SRCALPHA)
        self._draw()
        self.rect         = self.image.get_rect()
        self.rect.x       = x
        self.rect.y       = y

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        h = self.BTN_HEIGHT // 2 if self._phys else self.BTN_HEIGHT
        pygame.draw.rect(self.image, CINZA_ESCURO,
                         (0, self.BTN_HEIGHT - 6, self.BTN_WIDTH, 6))
        top_y  = self.BTN_HEIGHT - h
        pygame.draw.rect(self.image, self.color,
                         (2, top_y, self.BTN_WIDTH - 4, h - 2))
        border = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.rect(self.image, border,
                         (2, top_y, self.BTN_WIDTH - 4, h - 2), 2)

    @property
    def timer_frac(self):
        """Fração do temporizador restante (1.0 = cheio, 0.0 = fechado)."""
        return self._timer / CLOSE_DELAY if self._timer > 0 else 0.0

    def check_press(self, players):
        prev_phys = self._phys
        self._phys = any(
            player.rect.bottom >= self.rect.top and
            player.rect.bottom <= self.rect.bottom + 5 and
            player.rect.right  > self.rect.left and
            player.rect.left   < self.rect.right
            for player in players
        )
        # Reinicia timer enquanto pressionado, contagem regressiva ao soltar
        if self._phys:
            self._timer = CLOSE_DELAY
        elif self._timer > 0:
            self._timer -= 1

        new_open = self._phys or self._timer > 0
        if new_open != self._doors_open:
            self._doors_open = new_open
            for door in self.linked_doors:
                door.set_open(new_open)

        if self._phys != prev_phys:
            self._draw()


class Lever(pygame.sprite.Sprite):
    """Alavanca de parede — toca uma vez para ativar/desativar (toggle)."""

    W, H = 26, 42

    def __init__(self, x, y, linked_objects):
        pygame.sprite.Sprite.__init__(self)
        self.linked       = linked_objects
        self.active       = False
        self._prev_touch  = False
        self.image        = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        self._draw()
        self.rect         = self.image.get_rect()
        self.rect.x       = x
        self.rect.y       = y

    def _draw(self):
        self.image.fill((0, 0, 0, 0))
        # Placa de fundo
        pygame.draw.rect(self.image, (60, 60, 60),
                         (3, 2, self.W - 6, self.H - 4), border_radius=4)
        pygame.draw.rect(self.image, (120, 120, 120),
                         (3, 2, self.W - 6, self.H - 4), 2, border_radius=4)
        # Cabo da alavanca
        cx = self.W // 2
        if self.active:
            # Apontando para cima (ativo) — verde
            pygame.draw.line(self.image, (0, 200, 80), (cx, self.H - 10), (cx, 10), 4)
            pygame.draw.circle(self.image, (0, 220, 100), (cx, 9), 6)
            pygame.draw.circle(self.image, (100, 255, 150), (cx, 9), 3)
        else:
            # Apontando para baixo (inativo) — vermelho
            pygame.draw.line(self.image, (200, 60, 0), (cx, 10), (cx, self.H - 10), 4)
            pygame.draw.circle(self.image, (220, 80, 0), (cx, self.H - 9), 6)
            pygame.draw.circle(self.image, (255, 140, 80), (cx, self.H - 9), 3)
        # Ponto de pivô central
        pygame.draw.circle(self.image, (180, 180, 180), (cx, self.H // 2), 4)

    def check_contact(self, players):
        in_contact = any(player.rect.colliderect(self.rect) for player in players)
        # Alterna apenas na borda de subida (entrada do contato)
        if in_contact and not self._prev_touch:
            self.active = not self.active
            self._draw()
            for obj in self.linked:
                obj.activate(self.active)
        self._prev_touch = in_contact


class Gem(pygame.sprite.Sprite):
    """Gema coletável em formato de diamante."""
    SIZE = 16

    def __init__(self, x, y, color=(255, 215, 50)):
        pygame.sprite.Sprite.__init__(self)
        s = self.SIZE
        self.image = pygame.Surface((s, s), pygame.SRCALPHA)
        # Forma de losango
        pts = [(s // 2, 0), (s - 1, s // 2), (s // 2, s - 1), (1, s // 2)]
        pygame.draw.polygon(self.image, color, pts)
        # Faceta clara (topo-direito)
        light = tuple(min(255, c + 70) for c in color)
        pts2  = [(s // 2, 2), (s - 3, s // 2), (s // 2, s // 2 - 2)]
        pygame.draw.polygon(self.image, light, pts2)
        # Contorno escuro
        dark = tuple(max(0, c - 70) for c in color)
        pygame.draw.polygon(self.image, dark, pts, 1)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y