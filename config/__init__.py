from .Runner import main_loop
from .Display import create_window
#from classes.Inimigos import *
from classes.Jogador import get_player
   
def run():
    # cria nova janela
    window = create_window()    
        
    # criar jogador
    player = get_player()
    
    #repetição principal
    main_loop(window, player)
    
    
    

