from config.Constantes import *

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
      
def get_player(pygame):    
    ## criando jogador
    jogador = {'objRect': pygame.Rect(300, 100, 50, 50), 'cor': VERDE, 'vel': VEL}
    return jogador

def get_teclas():
    # definindo o dicionario que guardará as direcoes pressionadas
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}
    return teclas


def update_player(pygame, janela, jogador, teclas, blocos):
    # movendo o jogador
    moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))
    # desenhando jogador
    pygame.draw.rect(janela, jogador['cor'], jogador['objRect'])
    
    # checando se jogador bateu em algum bloco ou se bloco saiu da janela para retirá-lo da lista
    for bloco in blocos[:]:
        bateu = jogador['objRect'].colliderect(bloco['objRect'])
        if bateu or bloco['objRect'].y > ALTURAJANELA:
            blocos.remove(bloco)