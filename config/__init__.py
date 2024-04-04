from .Runner import *
from .Display import *
from classes.Inimigos import *
from classes.Jogador import *
   
def run(pygame):
    # cria nova janela
    window = create_window(pygame)
    
    # criando um objeto pygame.time.Clock
    relogio = pygame.time.Clock()
    
    # criar jogador
    player = get_player(pygame)
    
    #criar inimigos
    enemies = get_enemies(pygame)
    
    #repetição principal
    main_loop(pygame, window, relogio, player, enemies)
    
    
    

