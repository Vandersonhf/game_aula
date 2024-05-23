#from .Settings import *
import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, size, pos, surfs:list, sounds:list, rotate=0):
        super().__init__()
        
        self.size = size           #[width, height]
        self.pos = pos             #[x, y]        
        self.sounds = sounds
        
        surfs_scaled = []
        for s in surfs:                
             surf = pygame.transform.scale(s, size)
             surf = pygame.transform.rotozoom(surf,rotate,1)
             surfs_scaled.append(surf)
        self.curr_surf = surfs_scaled[0]
        self.list_surf = surfs_scaled     
             
        self.col_rect = pygame.Rect(tuple(pos), tuple(size))    
        self.mask = pygame.mask.from_surface(self.curr_surf)
        
        self.idx_ani = 0        
        self.delay_ani = 10    
        self.dead = False
        self.speed = 1          
        self.delay = 0      
        
    
    def update(self):
        pass

    def draw(self, settings):        
        # draw bigger surf to window at x,y position
        settings.window.blit(self.curr_surf, self.col_rect)
        
        #colisao debug
        #pygame.draw.rect(settings.window,settings.COLOR_TEXT,self.col_rect,2)
    
        
    def explode(self):
        pass
    
    def animation(self, inflate):
        self.curr_surf = self.list_surf[self.idx_ani]
        if self.dead and self.col_rect.size[0] > 1:
            old = self.col_rect.center
            self.col_rect = self.col_rect.inflate(inflate, inflate)            
            self.curr_surf = pygame.transform.scale(self.curr_surf, self.col_rect.size)   
            self.col_rect.center = old   
        
        self.delay += 1
        if self.idx_ani < len(self.list_surf)-1:           
            if self.delay > self.delay_ani:
                self.idx_ani += 1
                self.delay = 0
            return 0
        else:            
            if self.delay > self.delay_ani:
                self.idx_ani = 0
                self.delay = 0
                return 1
            return 0
    