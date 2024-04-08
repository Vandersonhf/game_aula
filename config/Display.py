import pygame
from .Constantes import *

def create_window():
    janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
    pygame.display.set_caption('Imagem e Som')   
    return janela


def draw_background(janela, points):
    janela.blit(imagemFundo, (0,0))
    pygame.draw.line(janela, PRETO, (10, 25), (200, 25), 2)
    
    # Trabalhando com texto
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f'Score:{points}', True, PRETO)
    janela.blit(texto, [10, 8])
    
def new_level(janela, level, ciclos):
    if ciclos >= 1 and ciclos <= INTERVAL:        
        _print_level(janela,level)
    elif ciclos >= CICLOS and ciclos <= CICLOS+INTERVAL:
        if ciclos == CICLOS:
            level += 1
        _print_level(janela,level)
    elif ciclos >= (CICLOS*2) and ciclos <= (CICLOS*2)+INTERVAL:
        if ciclos == (CICLOS*2):
            level += 1
        _print_level(janela,level)
    elif ciclos >= (CICLOS*3) and ciclos <= (CICLOS*3)+INTERVAL:
        _end_game(janela)
    return level

def _print_level(janela, level):
    fonte = pygame.font.Font(None, 60)
    texto = fonte.render(f'Level {level}', True, PRETO)
    janela.blit(texto, [LARGURAJANELA/2-60, ALTURAJANELA/2])
    
def _end_game(janela):
    fonte = pygame.font.Font(None, 60)
    texto = fonte.render(f'Game Clear!!!', True, PRETO)
    janela.blit(texto, [LARGURAJANELA/2-100, ALTURAJANELA/2])