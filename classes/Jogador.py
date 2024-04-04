from .Figura import *
from config.Constantes import *

def get_player(pygame):    
    # criando a bola
    bola = {'objRect': pygame.Rect(270, 330, 30, 30), 'cor': BRANCO, 'vel': [3,3]}
    return bola

def update_player(pygame, janela, bola):
    # reposicionando e desenha a bola
    mover(bola, (LARGURAJANELA, ALTURAJANELA))
    pygame.draw.ellipse(janela, bola['cor'], bola['objRect'])