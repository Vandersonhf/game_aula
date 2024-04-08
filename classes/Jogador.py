import pygame
from config.Constantes import *

# definindo a função mover(), que registra a posição de um jogador
def _moverJogador(jogador, teclas, dim_janela):
    borda_esquerda = 0
    borda_superior = 0
    borda_direita = dim_janela[0]
    borda_inferior = dim_janela[1]
    
    if teclas['esquerda'] and jogador['objRect'].left > borda_esquerda:
        jogador['objRect'].x -= jogador['vel']
    if teclas['direita'] and jogador['objRect'].right < borda_direita:
        jogador['objRect'].x += jogador['vel']
    if teclas['cima'] and jogador['objRect'].top > borda_superior:
        jogador['objRect'].y -= jogador['vel']
    if teclas['baixo'] and jogador['objRect'].bottom < borda_inferior:
        jogador['objRect'].y += jogador['vel']
      
def get_player():    
    ## criando jogador
    jogador = {'objRect': pygame.Rect(300,100,LARGURATUBARAO,ALTURATUBARAO),
               'imagem': imagemTubarao, 'vel': VEL}
    return jogador

def get_teclas():
    # definindo o dicionario que guardará as direcoes pressionadas
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}
    return teclas


def update_player(janela, jogador, teclas, peixes, points):
    # movendo o jogador
    _moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))    
    # desenhando jogador
    janela.blit(jogador['imagem'], jogador['objRect'])
    
    # checando se jogador comeu algum peixe ou se o peixe saiu da janela para retirá-lo da lista
    for peixe in peixes[:]:
        comeu = jogador['objRect'].colliderect(peixe['objRect'])
        if comeu and somAtivado:
            # som e pontuação diferentes
            if peixe['tipo'] == 1:
                somComer1.play()
                points += 10
            elif peixe['tipo'] == 2:
                somComer2.play()
                points += 30
            else:
                somComer3.play()
                points += 50
        if comeu or peixe['objRect'].x > LARGURAJANELA or (peixe['objRect'].x < 0):
            peixes.remove(peixe)
    return points