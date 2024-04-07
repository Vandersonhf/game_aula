import pygame
from .Constantes import *

def create_window():
    janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
    pygame.display.set_caption('Imagem e Som')   
    return janela


