from .Sprite import Sprite
import pygame
from .Settings import settings

class Asteroid(Sprite):    
    def __init__(self, ID, pos, size, speed):                       
        super().__init__(size, pos, settings.surf_enemy['asteroid'], settings.sound_enemy['asteroid'])
        
        # valor por objeto
        self.speed = speed
        self.delay_ani = 1   
        self.ID = ID    
        
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
    def __init__(self, ID, pos, size, speed, mob_surf, mob_fire_delay, type):
        '''pos, size and speed = tuple[int,int]'''        
        super().__init__(size, pos, settings.surf_enemy[mob_surf], settings.sound_enemy['enemy1'])
        
        # valor por objeto      
        self.speed = speed
        self.delay_ani = 2 
        self.maxlife = 2
        self.life = self.maxlife
        self.type = type 
        self.ID = ID
        
        self.delay_fire = mob_fire_delay
        self.counter = 0
        self.rockets = pygame.sprite.Group() 
        self.pows = pygame.sprite.Group() 
        self.done = False
               
    # definindo a função mover
    def move_chase(self, player_pos):
        if not self.dead:
            if self.type > 3: 
                if self.col_rect.centerx < player_pos:
                    self.col_rect.x += 3
                else: self.col_rect.x += -3
            else: self.col_rect.x += self.speed[0] 
            #if self.col_rect.y<settings.disp_size[1]/2:
            self.col_rect.y += self.speed[1] 
    
    def move(self):
        if not self.dead:
            self.col_rect.x += self.speed[0]             
            self.col_rect.y += self.speed[1] 
            
    def update(self):        
        self.counter += 1
        if not self.dead: 
            self.new_fire()
            self.move()
        
        if self.dead:
            self.done = self.animation(-1)            
        
        self.draw(settings) 
        self.rockets.update()
        
        #kill explode    
        if self.dead and self.done:
            self.kill()
            
        #draw life bar
        if not self.dead: 
            rect = pygame.Rect(self.col_rect.left, self.col_rect.top-15,
                                    self.col_rect.width, 13)  
            life_rect = pygame.Rect(self.col_rect.left+2, self.col_rect.top-13,
                                    int((self.col_rect.width*self.life)/self.maxlife)-4, 8)      
            if not self.dead: pygame.draw.rect(settings.window, 'gray', rect)
            pygame.draw.rect(settings.window, 'red', life_rect)
        
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
            fire = Rocket(pos, size, (0,15))                    
            self.rockets.add(fire)
            fire.shoot()
            self.counter = 0
            

class Boss(Sprite):    
    def __init__(self, pos, size, speed, mob_surf, mob_fire_delay):        
        super().__init__(size, pos, settings.surf_enemy[mob_surf], settings.sound_enemy['enemy1'])
        
        # valor por objeto      
        self.speed = speed
        self.delay_ani = 2 
        self.maxlife = 100
        self.life = self.maxlife
        
        self.delay_fire = mob_fire_delay
        self.counter = 0
        self.rockets = pygame.sprite.Group()
        self.done = False
               
    # definindo a função mover
    def move_chase(self, player_pos):
        if not self.dead:
            if self.col_rect.centerx < player_pos:
                self.col_rect.x += 3
            else: self.col_rect.x += -3            
            if self.col_rect.y<settings.disp_size[1]/3:
                self.col_rect.y += self.speed[1] 
                
    def move(self):
        if not self.dead:
            self.col_rect.x += self.speed[0]             
            self.col_rect.y += self.speed[1]
            
    def update(self):        
        self.counter += 1
        if not self.dead: 
            self.new_fire()
            self.move()
        
        if self.dead:
            self.done = self.animation(-1)            
        #else: self.move()     
        
        self.draw(settings) 
        self.rockets.update()
        
        #draw life bar
        rect = pygame.Rect(self.col_rect.left, self.col_rect.top-10,
                                self.col_rect.width, 13)  
        life_rect = pygame.Rect(self.col_rect.left+2, self.col_rect.top-8,
                                int((self.col_rect.width*self.life)/self.maxlife)-4, 8)      
        if not self.dead: pygame.draw.rect(settings.window, 'gray', rect)
        pygame.draw.rect(settings.window, 'red', life_rect)
        
        #kill explode    
        if self.dead and self.done:
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
            fire = Rocket(pos, size, (0,15))                    
            self.rockets.add(fire)
            fire.shoot()
            #second
            pos = [self.col_rect.centerx-100, self.col_rect.bottom-100] 
            fire = Rocket(pos, size, (-2,15))                    
            self.rockets.add(fire)
            fire.shoot()
            #third
            pos = [self.col_rect.centerx+100, self.col_rect.bottom-100]
            fire = Rocket(pos, size, (2,15))                    
            self.rockets.add(fire)
            fire.shoot()
            self.counter = 0


class Rocket(Sprite):    
    def __init__(self, pos, size, speed):         
        super().__init__(size, pos, settings.surf_enemy['rocket1'], settings.sound_enemy['rocket1'])
        
        self.speed = speed   # velocidade do raio                          
        
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
    