import server
from server.Socket import *

if __name__ == '__main__':
    '''inicialização do jogo'''    
    
    server.run_game()
    
'''
main client - runs main game and player 1
sends to client signals of sprites
        
messages P2 to server
    update_type_number_attr_value    

message server to P2
    create_type_number_pos_vel
    update_type_number_attr_value
    destroy_type_number

'''