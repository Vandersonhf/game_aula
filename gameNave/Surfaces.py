import pygame
from pygame import Surface

class Surfaces():
    def __init__(self, disp_size):
         # Carregando as imagens.       
        self.surf_ship = pygame.image.load('images/ship.png')
       
        # asteroids
        self.exp_seq = pygame.image.load('sprites/asteroids-arcade.png').convert_alpha()        
        self.surf_asteroids = self.get_sub_surfs(self.exp_seq, 66,194,(58,61),(65,0),3)
        
        self.surf_fire = self.exp_seq.subsurface((198,72),(4,8)) 
        self.surf_fire = pygame.transform.rotozoom(self.surf_fire,0,3)
          
        self.surf_rocket = self.exp_seq.subsurface((173,48),(6,12)) 
        self.surf_rocket = pygame.transform.rotozoom(self.surf_rocket,0,3)
        
        self.surf_jets = self.get_sub_surfs(self.exp_seq, 71,15,(18,17),(32,0),4)
        
        sub1 = self.exp_seq.subsurface((200,5),(16,24)) 
        sub1 = pygame.transform.rotozoom(sub1,180,2)       
        sub2 = self.exp_seq.subsurface((8,197), (48, 52))
        sub3 = self.exp_seq.subsurface((207,144),(36,35))
        sub4 = self.exp_seq.subsurface((151,151), (17,18))
        sub5 = self.exp_seq.subsurface((92,156),(8,8))        
        self.surf_enemy1 = [sub1,sub2,sub3,sub4,sub5]
        
        self.surf_asteroids.insert(1,sub2)
          
        
    def get_sub_surfs(self, surf:Surface, top, left, width_height, offset_next, times):
        list = []
        for i in range(times):
            #print(top, left, width_height)
            list.append(surf.subsurface((top,left), width_height))
            top = top + offset_next[0]
            left = left + offset_next[1]
        return list