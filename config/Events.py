import pygame
from config.Constantes import *

def trata_eventos(teclas,jogador,raios):
    #print("Tratando...")
    for evento in pygame.event.get():
        # Se for um evento QUIT
        if evento.type == pygame.QUIT:
            terminar()
        
        # quando uma tecla é pressionada
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                terminar()
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                teclas['esquerda'] = True
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                teclas['direita'] = True
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                teclas['cima'] = True
            if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                teclas['baixo'] = True
            if evento.key == pygame.K_SPACE:
                raio = {'objRect': pygame.Rect(jogador['objRect'].centerx,
                                               jogador['objRect'].top, LARGURARAIO, ALTURARAIO),
                        'imagem': imagemRaio,
                        'vel': VELRAIO}
                raios.append(raio)
                somTiro.play()
                        
        # quando uma tecla é solta
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                teclas['esquerda'] = False
            if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                teclas['direita'] = False
            if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                teclas['cima'] = False
            if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                teclas['baixo'] = False
        
        # mouse
        if evento.type == pygame.MOUSEMOTION:
            # Se o mouse se move, movimenta jogador para onde o cursor está.
            centroX_jogador = jogador['objRect'].centerx
            centroY_jogador = jogador['objRect'].centery
            jogador['objRect'].move_ip(evento.pos[0] - centroX_jogador, evento.pos[1] - centroY_jogador)
        if evento.type == pygame.MOUSEBUTTONDOWN:
            raio = {'objRect': pygame.Rect(jogador['objRect'].centerx,
                                           jogador['objRect'].top, LARGURARAIO, ALTURARAIO),
                    'imagem': imagemRaio,
                    'vel': VELRAIO}
            raios.append(raio)
            somTiro.play()
                            
    return True


def aguardarEntrada():
    # Aguarda entrada por teclado ou clique do mouse no “x” da janela.
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                if evento.key == pygame.K_F1:
                    return
            
def terminar():
    # Termina o programa.
    pygame.quit()
    exit() 