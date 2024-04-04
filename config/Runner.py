from .Events import *
from .Constantes import *
from classes.Inimigos import *
from classes.Jogador import *

def main_loop(pygame, janela, relogio, player, enemies):
    deve_continuar = True
    while deve_continuar:
        #verifica evetos e atualiza em memória       
        deve_continuar = trata_eventos(pygame)
        
        # preenchendo o fundo com a cor preta
        janela.fill(PRETO)
        
        #atualiza blocos
        update_enemies(pygame, janela, player, enemies)
          
        #atualiza bola      
        update_player(pygame, janela, player)
        
        # mostrando na tela tudo o que foi desenhado
        pygame.display.update()
        
        # limitando a 40 quadros por segundo
        relogio.tick(60)
        
       
        
