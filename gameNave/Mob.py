import pygame
from .Sprite import Sprite
from .Display import Display
from .Surfaces import Surfaces
from .Sounds import Sounds
from .Fire import Fire

class Mob(Sprite):    
    def __init__(self, surfs:Surfaces, sounds:Sounds, startx:int, starty:int, size:tuple[int,int],
                 speed:int, display:Display):        
        super().__init__(surfs.surf_enemy1, (startx,starty), size)
        # valor por objeto
        self.surfs = surfs
        self.surf_fire = surfs.surf_fire
        self.sounds = sounds
        self.speed = speed
        self.explosion_delay = 20
        self.exploded = False  
        
        self.display = display   
        
        self.delay_fire = 60
        self.counter = 0
        self.fires = pygame.sprite.Group()  
       
        
    # definindo a função mover
    def move(self):
        self.objRect.x += self.speed[0]
        self.objRect.y += self.speed[1]
        
    
    def update(self, display:Display):        
        self.counter += 1
        if not self.exploded: self.new_fire()
        
        if self.exploded:
            done = self.animation(self.explosion_delay)            
        else: self.move()     
        
        self.draw(display.window) 
        self.fires.update(self.display)
        
        #kill explode    
        if self.exploded and done:         
            self.kill()
        
        #kill out of range
        top_rock = self.objRect.top
        if top_rock > display.disp_size[1]:
            self.kill()
                                      
        
    def explode(self):
        self.exploded = True
        self.sounds.somExplosao_nave.play()
        
        
    def new_fire(self):
        if self.counter >= self.delay_fire:
            fire = Fire(self.surfs, self.sounds, self.objRect.centerx, self.objRect.bottom, (0,10))                    
            self.fires.add(fire)
            fire.shoot()
            self.counter = 0
    
    
    
        