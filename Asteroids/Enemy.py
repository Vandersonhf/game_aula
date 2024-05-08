from .Settings import *
from .Sprite import Sprite

class Asteroid(Sprite):    
    def __init__(self, pos:list[int,int], size:list[int,int], speed:list[int,int]):               
        super().__init__(size, pos, surf_enemy['asteroid'], sound_enemy['asteroid'])
        
        # valor por objeto
        self.speed = speed
        self.delay_ani['dead'] = 20       
        
    # definindo a função mover
    def move(self):
        self.col_rect.x += self.speed[0]
        self.col_rect.y += self.speed[1]
            
    def update(self):        
        if self.dead:
            done = self.animation()            
        else: self.move()     
        
        self.draw(window) 
        
        #kill explode    
        if self.dead and done:         
            self.kill()
                     
        #kill out of range
        top_rock = self.col_rect.top
        if top_rock > disp_size[1]:
            self.kill()       
        
    def explode(self):
        self.dead = True
        self.sounds[0].play()
        
        

class Mob(Sprite):    
    def __init__(self, pos:list[int,int], size:list[int,int], speed:list[int,int]):
        super().__init__(size, pos, surf_enemy['enemy1'], sound_enemy['enemy1'])
        
        # valor por objeto      
        self.speed = speed
        self.delay_ani['dead'] = 20 
        
        self.delay_fire = 60
        self.counter = 0
        self.rockets = pygame.sprite.Group()  
               
    # definindo a função mover
    def move(self):
        self.col_rect.x += self.speed[0]
        self.col_rect.y += self.speed[1]
            
    def update(self):        
        self.counter += 1
        if not self.dead: self.new_fire()
        
        if self.dead:
            done = self.animation()            
        else: self.move()     
        
        self.draw(window) 
        self.rockets.update()
        
        #kill explode    
        if self.dead and done:         
            self.kill()
        
        #kill out of range
        top_rock = self.col_rect.top
        if top_rock > disp_size[1]:
            self.kill()                                     
        
    def explode(self):
        self.dead = True
        self.sounds[0].play()
                
    def new_fire(self):
        if self.counter >= self.delay_fire:
            fire = Rocket()                    
            self.rockets.add(fire)
            fire.shoot()
            self.counter = 0
            


class Rocket(Sprite):    
    def __init__(self): 
        pos = [self.col_rect.centerx, self.col_rect.bottom]       
        size = (surf_enemy['rocket1'][0].get_width(), surf_enemy['rocket1'][0].get_height())
        super().__init__(size, pos, surf_enemy['rocket1'], sound_enemy['rocket1'])
        
        self.speed = [0,10]   # velocidade do raio                          
        
    def shoot(self):
        self.sounds.somFire.play()
        
    # definindo a função mover
    def move(self):
        self.col_rect.x += self.speed[0]
        self.col_rect.y += self.speed[1]
           
    def update(self):              
        self.move()
        self.draw(window)
        base_rocket = self.col_rect.top
        if base_rocket > disp_size[1]:
            self.kill() 