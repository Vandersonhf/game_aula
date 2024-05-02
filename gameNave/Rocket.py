from .Sprite import Sprite
from .Surfaces import Surfaces
from .Sounds import Sounds
from .Display import Display

class Rocket(Sprite):    
    def __init__(self, surfs:Surfaces, sounds:Sounds, startx, starty, speed):
        super().__init__([surfs.surf_rocket], (startx,starty), (0,0))
        self.sounds = sounds
        self.speed = speed   # velocidade do raio                          
        
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
        
    
    
    
        