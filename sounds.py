# -*- coding: utf-8 -*-
# Geração procedural de sons — sem arquivos externos

import io
import wave
import numpy as np
import pygame

_RATE    = 44100
_sfx     = {}
_wav_bytes = {}  # bytes brutos do WAV para recriação de BytesIO a cada load
_current   = None  # nome da música em execução

# ── Frequências das notas ─────────────────────────────────────────────────────
_F = {
    'C4': 261.63, 'D4': 293.66, 'Eb4': 311.13, 'E4': 329.63,
    'F4': 349.23, 'G4': 392.00, 'Ab4': 415.30, 'A4': 440.00,
    'Bb4':466.16, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'Eb5': 622.25, 'E5': 659.25,
    'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
    'C6':1046.50,
    'R':  0,
}

def _note(name, dur, vol=0.22):
    """Gera array de amostras para uma nota musical com fade suave e harmônicos."""
    freq = _F.get(name, 0)
    n    = int(dur * _RATE)
    if freq == 0:
        return np.zeros(n)
    t = np.linspace(0, dur, n, False)
    w = np.sin(2 * np.pi * freq * t)
    w += 0.30 * np.sin(4 * np.pi * freq * t)   # 2.º harmônico
    w += 0.08 * np.sin(6 * np.pi * freq * t)   # 3.º harmônico
    w *= vol / 1.38
    fade = min(int(n * 0.07), 700)
    w[:fade]  *= np.linspace(0, 1, fade)
    w[-fade:] *= np.linspace(1, 0, fade)
    return w

def _seq(pairs, vol=0.22):
    """Concatena uma sequência de notas (nome, duração) em um único array de amostras."""
    return np.concatenate([_note(n, d, vol) for n, d in pairs])

def _to_sound(arr):
    """Converte array de amostras em objeto pygame.Sound estéreo de 16 bits."""
    arr  = np.clip(arr, -1, 1)
    s16  = (arr * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([s16, s16]))

def _to_wav(arr):
    """Converte array para bytes WAV (armazenamos os bytes brutos, não o BytesIO)."""
    arr  = np.clip(arr, -1, 1)
    s16  = (arr * 32767).astype(np.int16)
    buf  = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(_RATE)
        wf.writeframes(np.column_stack([s16, s16]).tobytes())
    return buf.getvalue()  # retorna bytes, não BytesIO


def init():
    """Gera todos os sons. Chamar após pygame.mixer.init()."""
    global _RATE
    info = pygame.mixer.get_init()
    if info:
        _RATE = info[0]

    # ── Música do menu — C maior, alegre ─────────────────────────────────
    menu = _seq([
        ('C5', .20), ('E5', .20), ('G5', .40), ('E5', .20),
        ('C5', .20), ('D5', .20), ('F5', .20), ('A5', .40),
        ('G5', .20), ('E5', .20), ('C5', .40), ('G4', .20),
        ('A4', .20), ('B4', .20), ('C5', .50), ('R',  .30),
    ])
    _wav_bytes['menu'] = _to_wav(menu)

    # ── Música das fases — lá menor, aventura ────────────────────────────
    game = _seq([
        ('A4', .15), ('C5', .15), ('E5', .30), ('D5', .15),
        ('B4', .15), ('G4', .15), ('A4', .30), ('R',  .15),
        ('E4', .15), ('G4', .15), ('A4', .30), ('B4', .15),
        ('C5', .15), ('D5', .15), ('E5', .40), ('R',  .30),
    ], vol=0.20)
    _wav_bytes['game'] = _to_wav(game)

    # ── SFX: morte — descida triste ───────────────────────────────────────
    _sfx['death'] = _to_sound(_seq([
        ('A4', .10), ('G4', .10), ('F4', .10),
        ('Eb4',.12), ('D4', .18), ('C4', .32),
    ], vol=0.38))

    # ── SFX: clique de botão — dois tons rápidos ──────────────────────────
    _sfx['click'] = _to_sound(_seq([('E5', .05), ('G5', .07)], vol=0.32))

    # ── SFX: alavanca acionada — clique metálico ──────────────────────────
    _sfx['lever'] = _to_sound(_seq([
        ('G4', .03), ('R', .02), ('D5', .05), ('G5', .09),
    ], vol=0.42))

    # ── SFX: porta abrindo — arpejo ascendente ────────────────────────────
    _sfx['door'] = _to_sound(_seq([
        ('E4', .06), ('G4', .06), ('B4', .06), ('E5', .22),
    ], vol=0.30))

    # ── SFX: gema coletada — brilho agudo ─────────────────────────────────
    _sfx['gem'] = _to_sound(_seq([
        ('A5', .04), ('C6', .10),
    ], vol=0.36))

    # ── Fanfarra de vitória — acorde ascendente feliz ─────────────────────
    win = _seq([
        ('C5', .09), ('E5', .09), ('G5', .09),
        ('C5', .09), ('E5', .09), ('G5', .09),
        ('C6', .45), ('R',  .06),
        ('G5', .09), ('A5', .09), ('B5', .09), ('C6', .55),
    ], vol=0.30)
    _wav_bytes['win'] = _to_wav(win)


def play_music(name, loops=-1):
    """Toca música. loops=-1 para repetir sempre, loops=0 para tocar uma vez."""
    global _current
    if name == _current and pygame.mixer.music.get_busy():
        return
    _current = name
    if name in _wav_bytes:
        # Cria um BytesIO novo a cada chamada — pygame fecha o objeto após o load
        buf = io.BytesIO(_wav_bytes[name])
        pygame.mixer.music.load(buf)
        pygame.mixer.music.set_volume(_NORMAL_VOL)
        pygame.mixer.music.play(loops)


def stop_music():
    """Para a música em execução e limpa o estado atual."""
    global _current
    _current = None
    pygame.mixer.music.stop()


_NORMAL_VOL = 0.45

def pause_music():
    """Silencia a música durante o pause (não trava o áudio)."""
    pygame.mixer.music.set_volume(0)


def resume_music():
    """Restaura o volume normal após o pause."""
    pygame.mixer.music.set_volume(_NORMAL_VOL)


def play_sfx(name):
    """Reproduz um efeito sonoro pelo nome, se disponível."""
    if name in _sfx:
        _sfx[name].play()