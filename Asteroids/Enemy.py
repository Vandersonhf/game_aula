#from .Settings import Settings
from .Sprite import Sprite
import pygame
from .Settings import settings
import random

class Asteroid(Sprite):    
    def __init__(self, pos:list[int,int], size:list[int,int], speed:list[int,int]):                       
        super().__init__(size, pos, settings.surf_enemy['asteroid'], settings.sound_enemy['asteroid'])
        
        # valor por objeto
        self.speed = speed
        self.delay_ani = 1       
        
    # definindo a função mover
    def move(self):
        self.col_rect.x += self.speed[0]
        self.col_rect.y += self.speed[1]
            
    def update(self):        
        if self.dead:
            done = self.animation(1)            
        else: self.move()     
        
        self.draw(settings) 
        
        #kill explode    
        if self.dead and done:         
            self.kill()
                     
        #kill out of range
        top_rock = self.col_rect.top
        if top_rock > settings.disp_size[1]:
            self.kill()       
        
    def explode(self):
        self.dead = True
        self.sounds[0].play()
        self.col_rect = self.col_rect.inflate(1,1)
        self.curr_surf = pygame.transform.scale(self.curr_surf, self.col_rect.size)
        
        

class Mob(Sprite):    
    def __init__(self, pos:list[int,int], size:list[int,int], speed:list[int,int],mob_surf, mob_fire_delay):
        
        
        super().__init__(size, pos, settings.surf_enemy[mob_surf], settings.sound_enemy['enemy1'])
        
        # valor por objeto      
        self.speed = speed
        self.delay_ani = 2 
        
        self.delay_fire = mob_fire_delay
        self.counter = 0
        self.rockets = pygame.sprite.Group() 
        self.pows = pygame.sprite.Group() 
        self.done = False
               
    # definindo a função mover
    def move(self):
        self.col_rect.x += self.speed[0]
        self.col_rect.y += self.speed[1]
            
    def update(self):        
        self.counter += 1
        if not self.dead: self.new_fire()
        
        if self.dead:
            self.done = self.animation(-1)            
        else: self.move()     
        
        self.draw(settings) 
        self.rockets.update()
        
        #kill explode    
        if self.dead and self.done:
            self.kill()
        
        #kill out of range
        top_rock = self.col_rect.top
        if top_rock > settings.disp_size[1]:
            self.kill()                                     
        
    def explode(self):
        self.dead = True
        self.sounds[0].play()
        self.col_rect = self.col_rect.inflate(30,30)
        self.curr_surf = pygame.transform.scale(self.curr_surf, self.col_rect.size)
                
    def new_fire(self):
        if self.counter >= self.delay_fire:
            pos = [self.col_rect.centerx, self.col_rect.bottom]       
            size = (settings.surf_enemy['rocket1'][0].get_width(), settings.surf_enemy['rocket1'][0].get_height())
            fire = Rocket(pos, size, self.speed)                    
            self.rockets.add(fire)
            fire.shoot()
            self.counter = 0
            

class Boss(Sprite):    
    def __init__(self, pos:list[int,int], size:list[int,int], speed:list[int,int],mob_surf, mob_fire_delay):
        
        
        super().__init__(size, pos, settings.surf_enemy[mob_surf], settings.sound_enemy['enemy1'])
        
        # valor por objeto      
        self.speed = speed
        self.delay_ani = 2 
        
        self.delay_fire = mob_fire_delay
        self.counter = 0
        self.rockets = pygame.sprite.Group() 
        self.pows = pygame.sprite.Group() 
        self.done = False
               
    # definindo a função mover
    def move(self):
        self.col_rect.x += self.speed[0]
        self.col_rect.y += self.speed[1]
            
    def update(self):        
        self.counter += 1
        if not self.dead: self.new_fire()
        
        if self.dead:
            self.done = self.animation(-1)            
        else: self.move()     
        
        self.draw(settings) 
        self.rockets.update()
        
        #kill explode    
        if self.dead and self.done:
            self.kill()
        
        #kill out of range
        top_rock = self.col_rect.top
        if top_rock > settings.disp_size[1]:
            self.kill()                                     
        
    def explode(self):
        self.dead = True
        self.sounds[0].play()
        self.col_rect = self.col_rect.inflate(30,30)
        self.curr_surf = pygame.transform.scale(self.curr_surf, self.col_rect.size)
                
    def new_fire(self):
        if self.counter >= self.delay_fire:
            pos = [self.col_rect.centerx, self.col_rect.bottom]       
            size = (settings.surf_enemy['rocket1'][0].get_width(), settings.surf_enemy['rocket1'][0].get_height())
            fire = Rocket(pos, size, self.speed)                    
            self.rockets.add(fire)
            fire.shoot()
            self.counter = 0


class Rocket(Sprite):    
    def __init__(self, pos, size, speed):         
        super().__init__(size, pos, settings.surf_enemy['rocket1'], settings.sound_enemy['rocket1'])
        
        self.speed = [0,speed[1]+10]   # velocidade do raio                          
        
    def shoot(self):
        self.sounds[0].play()
        
    # definindo a função mover
    def move(self):
        self.col_rect.x += self.speed[0]
        self.col_rect.y += self.speed[1]
           
    def update(self):              
        self.move()
        self.draw(settings)
        base_rocket = self.col_rect.top
        if base_rocket > settings.disp_size[1]:
            self.kill() 
           
            
class PowerUP(Sprite):    
    def __init__(self, pos, size):         
        super().__init__(size, pos, settings.surf_enemy['pows'], settings.sound_enemy['pows'])
        
        self.speed = [0,0]   # velocidade do raio     
        self.time = 200                     
        
    def get(self):
        self.sounds[0].play()
                      
    def update(self): 
        self.time -= 1 
        if self.time > 0: self.draw(settings)
        else: self.kill()
        

class ShieldUP(Sprite):    
    def __init__(self, pos, size):         
        super().__init__(size, pos, settings.surf_enemy['shield'], settings.sound_enemy['pows'])
        
        self.speed = [0,0]   # velocidade do raio     
        self.time = 300                     
        
    def get(self):
        self.sounds[0].play()
                      
    def update(self): 
        self.time -= 1 
        if self.time > 0: self.draw(settings)
        else: self.kill()
        