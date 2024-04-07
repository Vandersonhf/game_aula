from config.Constantes import *
import random

# definindo a função moverBloco(), que registra a posição do bloco
def moverBloco(bloco):
    bloco['objRect'].y += bloco['vel']


def set_enemies(pygame,blocos,contador):    
    # criando os blocos e colocando-os em uma lista    
    if contador >= ITERACOES:
        # adicionando um novo bloco
        contador = 0
        posX = random.randint(0, LARGURAJANELA - TAMANHOBLOCO)
        posY = -TAMANHOBLOCO
        velRandom = random.randint(1, VEL + 3)
        blocos.append({'objRect': pygame.Rect(posX, posY,
                TAMANHOBLOCO, TAMANHOBLOCO), 'cor': BRANCO, 'vel': velRandom})
    return contador
    

def update_enemies(pygame, janela, blocos):
   # movendo e desenhando os blocos
    for bloco in blocos:
        moverBloco(bloco)
        pygame.draw.rect(janela, bloco['cor'], bloco['objRect'])
        