from .Events import *
from .Constantes import *
from classes.Inimigos import *
from classes.Jogador import *

def main_loop(pygame, janela, relogio, player):
    # inicializando outras variáveis
    contador = 0
    blocos = []
    deve_continuar = True
    teclas = get_teclas()
    
    while deve_continuar:
        #verifica evetos e atualiza em memória       
        deve_continuar = trata_eventos(pygame,teclas,blocos)
        
        #criar inimigos
        contador += 1
        contador = set_enemies(pygame,blocos,contador)
        
        # preenchendo o fundo com a cor preta
        janela.fill(PRETO)
                        
        #atualiza jogador      
        update_player(pygame, janela, player, teclas, blocos)
        #atualiza blocos
        update_enemies(pygame, janela, blocos) 
        
        # mostrando na tela tudo o que foi desenhado
        pygame.display.update()        
        # limitando a 60 quadros por segundo
        relogio.tick(60)
        
       
        
