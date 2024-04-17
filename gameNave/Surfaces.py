import pygame

class Surfaces():
    def __init__(self, disp_size):
         # Carregando as imagens.       
        self.surf_ship = pygame.image.load('images/ship.png')
        self.surf_asteroid = pygame.image.load('images/asteroid.png')
        self.surf_rocket = pygame.image.load('images/rocket.png')
        self.surf_back = pygame.image.load('images/space.jpg')
        
        #redimensionando a surf de fundo.
        self.surf_back = pygame.transform.scale(self.surf_back, disp_size)
        
        #nova escala nave
        new_size = (self.surf_ship.get_width()/5, self.surf_ship.get_height()/5)
        self.surf_ship = pygame.transform.scale(self.surf_ship, new_size)
        
        #jato nave
        self.surf_jets = [pygame.image.load(f"images/jet{i:0>2}.png") for i in range(1,4)]
        jet_list = []
        for jet in self.surf_jets:
            jet_list.append(pygame.transform.rotozoom(jet,0,2))
        self.surf_jets = jet_list