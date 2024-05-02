import pygame
from pygame import Surface

class Sprite(pygame.sprite.Sprite):
    def __init__(self, surfs:list, pos:tuple[int,int], new_size:tuple = (0,0)):
        super().__init__()
        
        #new scale
        s_list = surfs
        if new_size != (0,0):
            s_list = []
            for s in surfs:
                s = pygame.transform.scale(s, new_size)
                s_list.append(s)
            
        self.surfs_cycle = s_list
        self.surf = s_list[0]  #load once in main game
        
        # for animation
        self.animation_index = 0
        self.delay = 0
                
        self.size = self.surf.get_size()
        self.width = self.surf.get_width()
        self.height = self.surf.get_height()
        
        self.objRect = pygame.Rect(pos[0], pos[1], self.width, self.height)  
        
        #define mascara de colisao
        self.mask = pygame.mask.from_surface(self.surf)
        #self.surf_mask = self.mask.to_surface()             

    def update(self):
        pass

    def draw(self, window:Surface):        
        # draw bigger surf to window at x,y position
        window.blit(self.surf, self.objRect)
        
        #colisao debug
        #pygame.draw.rect(window,(255,255,255),self.objRect,2)
    
    
    def animation(self, ani_delay):
        self.surf = self.surfs_cycle[self.animation_index]        
        
        self.delay += 1
        if self.animation_index < len(self.surfs_cycle)-1:           
            if self.delay > ani_delay:
                self.animation_index += 1
                self.delay = 0
            return 0
        else:            
            if self.delay > ani_delay:
                self.animation_index = 0
                self.delay = 0
                return 1
            return 0
    
    
