import pygame
from .Constantes import *

def create_window():
    janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
    pygame.display.set_caption('Asteroides')
    # Ocultando o cursor 
    pygame.mouse.set_visible(False)     
    return janela

def colocarTexto(texto, fonte, janela, x, y):
    # Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.
    objTexto = fonte.render(texto, True, CORTEXTO)
    rectTexto = objTexto.get_rect()
    rectTexto.topleft = (x, y)
    janela.blit(objTexto, rectTexto)

def draw_background(janela, pontuacao, recorde):
    # Preenchendo o fundo da janela com a imagem correspondente.
    janela.blit(imagemFundoRedim, (0,0))
    # Colocando as pontuações.
    colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)
    colocarTexto('Recorde: ' + str(recorde), fonte, janela, 10, 40)
 