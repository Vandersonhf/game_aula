from .Constantes import *

def create_window(pygame):
    janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
    pygame.display.set_caption('Colisão')   
    return janela


