# Fireboy & Watergirl — Projeto Final DeSoft

Projeto final da disciplina de Design de Software.

## Membros do grupo

- Henrique Montoro
- Rony Goldstein
- Leo Vicentini

## Descrição

Recriação do clássico **Fireboy & Watergirl** em Python com Pygame. O jogo conta com 3 fases temáticas (Floresta, Caverna e Vulcão), cada uma com layout e desafios únicos. Dois jogadores controlam os personagens simultaneamente no mesmo teclado e precisam cooperar para resolver os puzzles e chegar às portas de saída.

**Mecânicas principais:**
- Fireboy morre ao tocar água; Watergirl morre ao tocar lava
- Piscinas de ácido verde matam os dois
- Alavancas ativam pontes deslizantes horizontais e verticais
- Botões de pressão abrem as portas de saída — é preciso coordenar os dois jogadores
- Gemas coletáveis afetam a nota final (A, B ou C)

## Controles

| Personagem | Mover | Pular |
|---|---|---|
| Fireboy (vermelho) | `A` / `D` | `W` |
| Watergirl (azul) | `←` / `→` | `↑` |

## Dependências

- Python 3.8 ou superior
- Pygame 2.x

## Como instalar as dependências

```bash
pip install pygame
```

## Como rodar o jogo

```bash
python jogo.py
```

## Vídeo de apresentação

> 🔗 **[Link do vídeo — adicionar antes da entrega]**

## Estrutura do projeto

```
pygamedesoft/
├── jogo.py          # Ponto de entrada — máquina de estados principal
├── config.py        # Constantes globais (dimensões, física, cores, estados)
├── sprites.py       # Classes dos sprites (Player, Platform, Door, Button, Lever, pools…)
├── init_screen.py   # Tela inicial
├── level_screen.py  # Tela de seleção de fase
└── game_screen.py   # Loop de jogo e construção das fases
```

## Alguns prompts gerados com auxílio de IAg
- Criar a level_screen.py com uma tela de seleção de 3 fases (Floresta, Caverna, Vulcão) com cards clicáveis e indicador de dificuldade. Quero efeito visual quando o mouse passar por cima dos cards
- Criar o game_screen.py com a fase 1 (floresta). Fireboy ativa uma alavanca que libera uma ponte, os dois cruzam e pressionam botões juntos para abrir as portas. Fireboy morre em água, Watergirl morre em lava. Adicionar gemas para coletar.
- Criar funções para renderizar fundos bonitos para cada fase, na primeira floresta com gradiente de céu, colinas e árvores, na segunda caverna escura com cristais, na terceira vulcão com silhuetas e lava.
- Adicionar uma plataforma móvel horizontal na fase 2, e duas plataformas móveis na fase 3 (sendo uma vertical). Cronômetro mais centralizado, contador de gemas.
- Adicionar um temporizador em cima das portas para elas não fecharem assim que um personagem tirar o "pé" de cima do botão de abertura da porta

## Funções extraídas 100% de IAg
make_forest_bg()
make_cave_bg()
make_volcano_bg()
draw_timer_bars()
draw_win_screen()
draw_gameover_screen()

