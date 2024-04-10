import pygame

class Images():
    def __init__(self, disp_size):
         # Carregando as imagens.
        #self.imagemNave = pygame.image.load('images/nave.png')
        self.imagemNave = pygame.image.load('images/nave2.png')
        self.imagemAsteroide = pygame.image.load('images/asteroid.png')
        self.imagemRaio = pygame.image.load('images/missil.png')
        self.imagemFundo = pygame.image.load('images/space.jpg')
        
        #redimensionando a imagem de fundo.
        self.imagemFundo = pygame.transform.scale(self.imagemFundo, disp_size)
        
        #nova escala nave
        new_size = (self.imagemNave.get_width()/5, self.imagemNave.get_height()/5)
        self.imagemNave = pygame.transform.scale(self.imagemNave, new_size)
        
        self.LARGURANAVE = self.imagemNave.get_width()
        self.ALTURANAVE = self.imagemNave.get_height()
        self.LARGURARAIO = self.imagemRaio.get_width()
        self.ALTURARAIO = self.imagemRaio.get_height()
    
    