import pygame
from config.Constantes import *
import random

# definindo a função moverBloco(), que registra a posição do peixe
def _moverPeixe(peixe):
    peixe['objRect'].x -= peixe['vel']

def set_enemies(peixes, spawn, level, ciclos):    
    # criando os peixes e colocando-os em uma lista    
    if spawn >= (ITERACOES/level) and ciclos < (CICLOS*level-INTERVAL):
        # adicionando um novo peixe
        spawn = 0
        posY = random.randint(0, ALTURAJANELA - ALTURAPEIXE)
        posX = LARGURAJANELA
        velRandom = random.randint(VEL - 3, VEL + 3)
        #aparecer 3 tipos de peixes
        tipo = random.randint(1,3) if level == 3 else random.randint(1,2) if level == 2 else 1
        imagemPeixe = imagemPeixe1 if tipo == 1 else imagemPeixe2 if tipo == 2 else imagemPeixe3
        # tipo 1 peixe mais fácil de pegar
        velRandom = velRandom-2 if tipo == 1 else velRandom+1 if tipo == 2 else velRandom+3
        peixes.append({'objRect': pygame.Rect(posX, posY,LARGURAPEIXE,ALTURAPEIXE),
                       'imagem': imagemPeixe, 'vel': velRandom, 'tipo': tipo})
    return spawn
    
def update_enemies(janela, peixes):
   # movendo e desenhando os peixes
    for peixe in peixes:
        _moverPeixe(peixe)
        janela.blit(peixe['imagem'], peixe['objRect'])
        