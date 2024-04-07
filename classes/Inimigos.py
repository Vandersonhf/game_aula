import pygame
from config.Constantes import *
import random

# definindo a função moverBloco(), que registra a posição do peixe
def moverPeixe(peixe):
    peixe['objRect'].x -= peixe['vel']

def set_enemies(peixes, contador):    
    # criando os peixes e colocando-os em uma lista    
    if contador >= ITERACOES:
        # adicionando um novo peixe
        contador = 0
        posY = random.randint(0, ALTURAJANELA - ALTURAPEIXE)
        posX = LARGURAJANELA
        velRandom = random.randint(VEL - 3, VEL + 3)
        peixes.append({'objRect': pygame.Rect(posX, posY,LARGURAPEIXE,ALTURAPEIXE),
                       'imagem': imagemPeixe, 'vel': velRandom})
    return contador
    
def update_enemies(janela, peixes):
   # movendo e desenhando os peixes
    for peixe in peixes:
        moverPeixe(peixe)
        janela.blit(peixe['imagem'], peixe['objRect'])
        