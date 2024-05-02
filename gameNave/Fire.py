from .Sprite import Sprite
from .Surfaces import Surfaces
from .Sounds import Sounds
from .Display import Display

class Fire(Sprite):    
    def __init__(self, surfs:Surfaces, sounds:Sounds, startx, starty, speed):
        super().__init__([surfs.surf_fire], (startx,starty), (0,0))
        self.sounds = sounds
        self.speed = speed   # velocidade do raio                          
        
    def shoot(self):
        self.sounds.somFire.play()
        
    # definindo a função mover
    def move(self):
        self.objRect.x += self.speed[0]
        self.objRect.y += self.speed[1]
    
       
    def update(self, display:Display):              
        self.move()
        self.draw(display.window)
        base_rocket = self.objRect.top
        if base_rocket > display.disp_size[1]:
            self.kill() 
        
    
    
    
        