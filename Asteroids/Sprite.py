from .Settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, size:list[int,int], pos:list[int,int], surfs:list, sounds:list):
        super().__init__()
        
        self.size = size           #[width, height]
        self.pos = pos             #[x, y]        
        self.sounds = sounds
        self.curr_surf = surfs[0]
        self.list_surf = surfs
        self.col_rect = pygame.Rect(tuple(pos), tuple(size))    
        self.mask = pygame.mask.from_surface(self.curr_surf)
        
        self.idx_ani = {'live':0, 'dead':0}        
        self.delay_ani = {'live':10, 'dead':10}    
        self.dead = False
        self.speed = 1          
        self.delay = 0      
        
    
    def update(self):
        pass

    def draw(self):        
        # draw bigger surf to window at x,y position
        window.blit(self.curr_surf, self.objRect)
        
        #colisao debug
        pygame.draw.rect(window,COLOR_TEXT,self.col_rect,2)
    
        
    def explode(self):
        pass
    
    def animation(self, live: bool):
        i = 'live' if live else 'dead'
        self.surf = self.list_surf[self.idx_ani[i]]        
        
        self.delay += 1
        if self.idx_ani[i] < len(self.list_surf)-1:           
            if self.delay > self.delay_ani[i]:
                self.idx_ani[i] += 1
                self.delay = 0
            return 0
        else:            
            if self.delay > self.delay_ani[i]:
                self.idx_ani[i] = 0
                self.delay = 0
                return 1
            return 0
    