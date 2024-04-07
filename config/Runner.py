import pygame
from .Events import *
from .Constantes import *
from classes.Inimigos import *
from classes.Jogador import *

def main_loop(janela, player):
    # inicializando outras variáveis
    contador = 0
    peixes = []
    deve_continuar = True
    teclas = get_teclas()
    # criando um objeto pygame.time.Clock
    relogio = pygame.time.Clock()
    
    while deve_continuar:
        #verifica evetos e atualiza em memória       
        deve_continuar = trata_eventos(teclas,peixes)
        
        #criar inimigos
        contador += 1
        contador = set_enemies(peixes,contador)
        
        # preenchendo o fundo de janela com a sua imagem
        janela.blit(imagemFundo, (-1000,-1000))
                        
        #atualiza jogador      
        update_player(janela, player, teclas, peixes)
        #atualiza peixes
        update_enemies(janela, peixes) 
        
        # mostrando na tela tudo o que foi desenhado
        pygame.display.update()        
        # limitando a 60 quadros por segundo
        relogio.tick(60)
        
       
        
