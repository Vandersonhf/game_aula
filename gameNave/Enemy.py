import pygame
from .Sprite import Sprite
from .Display import Display
from pygame import Surface

class Enemy(Sprite):    
    def __init__(self, surf:Surface, startx, starty, size, speed):        
        super().__init__(surf, startx, starty, 1)
        # valor por objeto
        self.speed = speed
        self.surf = pygame.transform.scale(self.surf, size)        
        self.objRect = pygame.Rect(startx, starty, size[0], size[1])     #resize collision
        
        self.mask = pygame.mask.from_surface(self.surf)
        self.surf_mask = self.mask.to_surface()
        
    # definindo a função mover
    def move(self):
        self.objRect.x += self.speed[0]
        self.objRect.y += self.speed[1]
        
    
    def update(self, display:Display):        
        self.move()   
        self.draw(display.window)    
        top_rock = self.objRect.top
        if top_rock > display.disp_size[1]:
            self.kill()
        
        
    
    
    
        