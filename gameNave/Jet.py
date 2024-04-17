import pygame
from .Sprite import Sprite
from .Surfaces import Surfaces
from .Display import Display

class Jet(Sprite):    
    def __init__(self, surfaces:Surfaces, startx, starty):
        super().__init__(surfaces[0], startx, starty, 1)
                                    
        self.fly_cycle = surfaces
        self.animation_index = 0
        self.delay = 0
        self.jet_delay = 7
        self.objRect.center = (startx, starty+10)  # correct positioning 
        
        self.speed = 5      # velocidade da nave           
  
           
    def update(self, display:Display):             
        self.draw(display.window)
        self.fly_animation()
        
        
    def fly_animation(self):
        self.surf = self.fly_cycle[self.animation_index]        
        
        if self.animation_index < len(self.fly_cycle)-1:
            self.delay += 1
            if self.delay > self.jet_delay:
                self.animation_index += 1
                self.delay = 0
        else:
            self.animation_index = 0  
    
    
    
    
        