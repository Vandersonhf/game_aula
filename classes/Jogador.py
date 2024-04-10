import pygame
from game.Constantes import *

# definindo a função mover(), que registra a posição de um jogador
def moverJogador(jogador, teclas, dim_janela):
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
    # Criando jogador.
    posX = LARGURAJANELA / 2
    posY = ALTURAJANELA - 50
    jogador = {'objRect': pygame.Rect(posX, posY, LARGURANAVE, ALTURANAVE),
               'imagem': imagemNave, 'vel': VELJOGADOR}
    return jogador

def get_teclas():
    # definindo o dicionario que guardará as direcoes pressionadas
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}
    return teclas


def update_player(janela, jogador, teclas, asteroides, raios):
    # Movimentando e desenhando jogador(nave).
    moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))
    janela.blit(jogador['imagem'], jogador['objRect'])
    # Checando se jogador ou algum raio colidiu com algum asteroide.
    for asteroide in asteroides[:]:
        jogadorColidiu = jogador['objRect'].colliderect(asteroide['objRect'])
        if jogadorColidiu:            
            return False
        for raio in raios[:]:
            raioColidiu = raio['objRect'].colliderect(asteroide['objRect'])
            if raioColidiu:
                raios.remove(raio)
                asteroides.remove(asteroide)
    return True

