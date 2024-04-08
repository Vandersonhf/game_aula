import pygame
from .Events import trata_eventos
from .Display import draw_background, new_level
from .Constantes import *
from classes.Inimigos import set_enemies, update_enemies
from classes.Jogador import get_teclas, update_player

def main_loop(janela, player):
    # inicializando outras variáveis
    spawn = 0
    level = 1
    ciclos = 0
    peixes = []
    deve_continuar = True
    teclas = get_teclas()
    points = 0
    # criando um objeto pygame.time.Clock
    relogio = pygame.time.Clock()
    
    while deve_continuar:
        #verifica evetos e atualiza em memória       
        deve_continuar = trata_eventos(teclas,peixes)
        
        #criar inimigos
        spawn += 1; ciclos += 1        
        spawn = set_enemies(peixes, spawn, level, ciclos)
        
        # preenchendo o fundo de janela com a sua imagem
        draw_background(janela, points)
        
        #nova fase
        level = new_level(janela, level, ciclos)
        if ciclos >= (CICLOS*3)+INTERVAL:
            deve_continuar = False
                        
        #atualiza jogador      
        points = update_player(janela, player, teclas, peixes, points)
        #atualiza peixes
        update_enemies(janela, peixes) 
        
        # mostrando na tela tudo o que foi desenhado
        pygame.display.update()        
        # limitando a 60 quadros por segundo
        relogio.tick(60)
        
       
        
