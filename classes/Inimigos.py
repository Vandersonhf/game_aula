from .Figura import *
from config.Constantes import *

def get_enemies(pygame):    
    # criando os blocos e colocando-os em uma lista
    b1 = {'objRect': pygame.Rect(375, 80, 40, 40), 'cor': VERMELHO, 'vel': [0,2]}
    b2 = {'objRect': pygame.Rect(175, 200, 40, 40), 'cor': VERDE, 'vel': [0,-3]}
    b3 = {'objRect': pygame.Rect(275, 150, 40, 40), 'cor': AMARELO, 'vel': [0,-1]}
    b4 = {'objRect': pygame.Rect(75, 150, 40, 40), 'cor': AZUL, 'vel': [0,4]}
    blocos = [b1, b2, b3, b4]
    return blocos

def update_enemies(pygame, janela, bola, blocos):
    for bloco in blocos:
        # reposicionando o bloco
        mover(bloco, (LARGURAJANELA,ALTURAJANELA))
        # desenhando o bloco na janela
        pygame.draw.rect(janela, bloco['cor'], bloco['objRect'])
        # mudando a cor da bola caso colida com algum bloco
        mudarCor = bola['objRect'].colliderect(bloco['objRect'])
        if mudarCor:
            bola['cor'] = bloco['cor']      # troca cor
            bola['vel'] = [-bola['vel'][0], -bola['vel'][1]]    #inverte movimento bola
            bloco['vel'] = [-bloco['vel'][0], -bloco['vel'][1]] #inverte mov. bloco
            #blocos.remove(bloco)    # mata o inimigo?
        