import pygame
from .Sprite import Sprite
from pygame import Surface
from .Sounds import Sounds
from .Display import Display

class Rocket(Sprite):    
    def __init__(self, surf:Surface, sounds:Sounds, startx, starty):
        super().__init__(surf, startx, starty, 1)
        self.sounds = sounds
        self.speed = (0,-15)   # velocidade do raio                          
        
    def shoot(self):
        self.sounds.somTiro.play()
        
    # definindo a função mover
    def move(self):
        self.objRect.x += self.speed[0]
        self.objRect.y += self.speed[1]
    
       
    def update(self, display:Display):              
        self.move()
        self.draw(display.window)
        base_rocket = self.objRect.bottom
        if base_rocket < 0:
            self.kill() 
        
    
    
    
        