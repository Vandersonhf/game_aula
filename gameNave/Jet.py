from .Sprite import Sprite
from .Surfaces import Surfaces
from .Display import Display

class Jet(Sprite):    
    def __init__(self, surfs:Surfaces, startx:int, starty:int, size:tuple[int,int], speed:int):
        super().__init__(surfs.surf_jets, (startx,starty), size)
             
        self.jet_delay = 20
        self.objRect.center = (startx, starty+10)  # correct positioning 
        
        self.speed = speed      # velocidade da nave           
  
           
    def update(self, display:Display):             
        self.draw(display.window)
        self.animation(self.jet_delay)
        
        
   
    
    
    
    
        