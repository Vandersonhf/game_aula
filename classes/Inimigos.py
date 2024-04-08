import pygame
from config.Constantes import *
import random

# definindo a função mover
def moverElemento(elemento):
    elemento['objRect'].x += elemento['vel'][0]
    elemento['objRect'].y += elemento['vel'][1]

def set_enemies(asteroides, contador):    
    # Adicionando asteroides quando indicado.
    contador += 1
    if contador >= ITERACOES:
        contador = 0
        tamAsteroide = random.randint(TAMMINIMO, TAMMAXIMO)
        posX = random.randint(0, LARGURAJANELA - tamAsteroide)
        posY = - tamAsteroide
        vel_x = random.randint(-1,1)
        vel_y = random.randint(VELMINIMA, VELMAXIMA)
        asteroide = {'objRect': pygame.Rect(posX, posY, tamAsteroide, tamAsteroide),
                'imagem': pygame.transform.scale(imagemAsteroide, (tamAsteroide, tamAsteroide)),
                'vel': (vel_x, vel_y)}
        asteroides.append(asteroide)
    return contador
    
def update_enemies(janela, asteroides, raios):
    # Movimentando e desenhando os asteroides.
    for asteroide in asteroides:
        moverElemento(asteroide)
        janela.blit(asteroide['imagem'], asteroide['objRect'])
        
    # Eliminando os asteroides que passam pela base da janela.
    for asteroide in asteroides[:]:
        topo_asteroide = asteroide['objRect'].top
        if topo_asteroide > ALTURAJANELA:
            asteroides.remove(asteroide)
    
    # Movimentando e desenhando os raios.
    for raio in raios:
        moverElemento(raio)
        janela.blit(raio['imagem'], raio['objRect'])
        
    #Eliminando os raios que passam pelo topo da janela.
    for raio in raios[:]:
        base_raio = raio['objRect'].bottom
        if base_raio < 0:
            raios.remove(raio)
        