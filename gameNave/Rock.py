import pygame
from .Sprite import Sprite
from .Display import Display
from .Surfaces import Surfaces
from .Sounds import Sounds

class Rock(Sprite):    
    def __init__(self, surfs:Surfaces, sounds:Sounds, startx:int, starty:int, size:tuple[int,int], speed:int):        
        super().__init__(surfs.surf_asteroids, (startx,starty), size)
        # valor por objeto
        self.sounds = sounds
        self.speed = speed
        self.explosion_delay = 20
        self.exploded = False
        
        #self.mask = pygame.mask.from_surface(self.surf)
        #self.surf_mask = self.mask.to_surface()
        
    # definindo a função mover
    def move(self):
        self.objRect.x += self.speed[0]
        self.objRect.y += self.speed[1]
        
    
    def update(self, display:Display):        
        if self.exploded:
            done = self.animation(self.explosion_delay)            
        else: self.move()     
        
        self.draw(display.window) 
        
        #kill explode    
        if self.exploded and done:         
            self.kill()
                     
        #kill out of range
        top_rock = self.objRect.top
        if top_rock > display.disp_size[1]:
            self.kill()
        
        
    def explode(self):
        self.exploded = True
        self.sounds.somExplosao.play()
        
        
    
    
    
        