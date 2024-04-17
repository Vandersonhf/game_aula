import pygame
from pygame import Surface

class Sprite(pygame.sprite.Sprite):
    def __init__(self, surf:Surface, startx:int, starty:int, scale):
        super().__init__()

        self.surf = surf  #load once in main game
        #new scale
        new_size = (self.surf.get_width()*scale, self.surf.get_height()*scale)
        self.surf = pygame.transform.scale(self.surf, new_size)
        
        self.size = self.surf.get_size()
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()
        
        self.objRect = pygame.Rect(startx, starty, self.width, self.height)               

    def update(self):
        pass

    def draw(self, window:Surface):        
        # draw bigger surf to window at x,y position
        window.blit(self.surf, self.objRect)
        
        #colisao debug
        pygame.draw.rect(window,(255,255,255),self.objRect,2)
