from .Runner import *
from .Display import *
from classes.Inimigos import *
from classes.Jogador import *
   
def run():
    # cria nova janela
    window = create_window()    
        
    # criar jogador
    player = get_player()
    
    #repetição principal
    main_loop(window, player)
    
    
    

