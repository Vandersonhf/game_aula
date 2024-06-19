from .Sprite import Sprite
import pygame
from .Settings import settings

class Player(Sprite):
    def __init__(self):        
        pos = [settings.disp_size[0]*0.5, settings.disp_size[1]*0.7]
        size = (settings.surf_player['ship'][0].get_width()/5, settings.surf_player['ship'][0].get_height()/5)         
        
        super().__init__(size, pos, settings.surf_player['ship'], settings.sound_player['ship'])
        
        self.teclas = {'esquerda':False, 'direita':False, 'cima':False, 'baixo': False}
        self.speed = 10      # velocidade da nave 
        self.delay_rocket = 10
        self.counter = 0
        
        self.rockets = pygame.sprite.Group()         # lista com os rockets
        self.components = pygame.sprite.Group()            # addons da nave
        
        # add jet component   
        pos = [self.col_rect.centerx, self.col_rect.bottom]
        size = (settings.surf_player['jets'][0].get_width()*2, settings.surf_player['jets'][0].get_height()*2)    
        self.components.add(Jet(pos, size, self.speed))
                                
        # Inicializa posição.
        dx = self.col_rect.centerx
        dy = self.col_rect.centery
        self.col_rect.move_ip(pos[0] - dx, pos[1] - dy)        
        for comp in self.components:
            comp.col_rect.move_ip(pos[0] - dx, pos[1] - dy)
    
    # definindo a função mover(), que registra a posição de um jogador
    def move(self):  
        self.borda_esquerda = 0
        self.borda_superior = 0
        self.borda_direita = settings.disp_size[0]
        self.borda_inferior = settings.disp_size[1]
        
        if self.teclas['esquerda'] and self.col_rect.left > self.borda_esquerda:
            self.col_rect.x -= self.speed
            for comp in self.components:    # move components all along
                comp.col_rect.x -= comp.speed            
        if self.teclas['direita'] and self.col_rect.right < self.borda_direita:
            self.col_rect.x += self.speed
            for comp in self.components:
                comp.col_rect.x += comp.speed
        if self.teclas['cima'] and self.col_rect.top > self.borda_superior:
            self.col_rect.y -= self.speed
            for comp in self.components:
                comp.col_rect.y -= comp.speed
        if self.teclas['baixo'] and self.col_rect.bottom < self.borda_inferior:
            self.col_rect.y += self.speed
            for comp in self.components:
                comp.col_rect.y += comp.speed
       
        # atualiza posição mouse
        pygame.mouse.set_pos(self.col_rect.centerx, self.col_rect.centery)        
    
    def update(self):
        self.counter += 1 
        # verificando extra power ups
        size = (settings.surf_player['extra'][0].get_width(), settings.surf_player['extra'][0].get_height())
        if settings.ups == 2 and len(self.components)<settings.ups:            
            pos = [self.col_rect.center[0]+50, self.col_rect.top-20]            
            self.components.add(Power(pos, size, self.speed, rotate = -15))
        elif settings.ups == 3 and len(self.components)<settings.ups:
            pos = [self.col_rect.center[0]-50, self.col_rect.top-20]
            self.components.add(Power(pos, size, self.speed, rotate = 15))
        elif settings.ups == 4 and len(self.components)<settings.ups:
            pos = [self.col_rect.center[0]-100, self.col_rect.top-20]
            self.components.add(Power(pos, size, self.speed, rotate = 30))
        elif settings.ups == 5 and len(self.components)<settings.ups:
            pos = [self.col_rect.center[0]+100, self.col_rect.top-20]
            self.components.add(Power(pos, size, self.speed, rotate = -30))       
               
        # Movimentando a nave       
        self.move()
                
        #desenhando componentes e etc.
        self.components.update()
        self.rockets.update()
        
        # desenhando jogador(nave). 
        '''if settings.ups >= 3 and settings.ups < 5:
            self.curr_surf = self.surfs_scaled[1]
        elif settings.ups == 5:
            self.curr_surf = self.surfs_scaled[2]'''
        self.draw(settings)  
        
        #draw shield        
        center = list(self.col_rect.center)
        center[1] = center[1]+10
        if settings.life == 3:            
            pygame.draw.circle(settings.window, 'blue', center, 50, width=1)
            pygame.draw.circle(settings.window, 'blue', center, 45, width=1)             
        elif settings.life == 2:    
            pygame.draw.circle(settings.window, 'blue', center, 45, width=1)
              
    
    def new_rocket(self):
        if self.counter >= self.delay_rocket:
            pos = [self.col_rect.centerx, self.col_rect.top]
            size = (settings.surf_player['rocket'][0].get_width(), settings.surf_player['rocket'][0].get_height())
            #speed = [0,-15]
            rotate = 0
            for i in range(1,settings.ups+1): 
                if i == 1: 
                    pos[0] = self.col_rect.centerx           
                    speed = [0,-15]
                    rotate = 0
                if i == 2: 
                    pos[0] = self.col_rect.centerx+50
                    speed = [2,-15]
                    rotate = 0
                if i == 3: 
                    pos[0] = self.col_rect.centerx-50
                    speed = [-2,-15]
                    rotate = 0
                if i == 4: 
                    pos[0] = self.col_rect.centerx-100 
                    speed = [-5,-15] 
                    rotate = 30  
                if i == 5: 
                    pos[0] = self.col_rect.centerx+100 
                    speed = [5,-15] 
                    rotate = -30
                rocket = Rocket(pos, size, speed, rotate)
                rocket.col_rect.center = pos                  
                self.rockets.add(rocket)           
            rocket.shoot()
            self.counter = 0        
   
   
   
class Power(Sprite):
    def __init__(self, pos, size, speed, rotate=0):
        super().__init__(size, pos, settings.surf_player['extra'],
                         settings.sound_player['jets'],rotate=rotate)
             
        self.delay_ani = 1
        self.col_rect.center = (pos[0], pos[1]+10)  # correct positioning 
        
        self.speed = speed      # velocidade da nave           
             
    def update(self):             
        self.draw(settings)
        #self.animation(0)
            
            
class Jet(Sprite):
    def __init__(self, pos, size, speed):
        super().__init__(size, pos, settings.surf_player['jets'], settings.sound_player['jets'])
             
        self.delay_ani = 1
        self.col_rect.center = (pos[0], pos[1]+10)  # correct positioning 
        
        self.speed = speed      # velocidade da nave           
             
    def update(self):             
        self.draw(settings)
        self.animation(0)
        
        
        
        
class Rocket(Sprite):    
    def __init__(self, pos, size, speed, rotate=0):
        super().__init__(size, pos, settings.surf_player['rocket'],
                         settings.sound_player['rocket'], rotate=rotate)
        
        self.speed = speed   # velocidade do raio                          
        
    def shoot(self):
        self.sounds[0].play()
        
    # definindo a função mover
    def move(self):
        self.col_rect.x += self.speed[0]
        self.col_rect.y += self.speed[1]
           
    def update(self): 
        if settings.ups == 5: 
            self.curr_surf = self.surfs_scaled[1]
                     
        self.move()
        self.draw(settings)
        base_rocket = self.col_rect.bottom
        if base_rocket < 0:
            self.kill() 
            
            
class Player2(Sprite):
    def __init__(self):        
        pos = [settings.disp_size[0]*0.5, settings.disp_size[1]*0.7]
        size = (settings.surf_player['ship'][0].get_width()/5, settings.surf_player['ship'][0].get_height()/5)         
        
        super().__init__(size, pos, settings.surf_player['ship'], settings.sound_player['ship'])
        
        self.teclas = {'esquerda':False, 'direita':False, 'cima':False, 'baixo': False}
        self.speed = 10      # velocidade da nave 
        self.delay_rocket = 10
        self.counter = 0
        
        self.rockets = pygame.sprite.Group()         # lista com os rockets
        self.components = pygame.sprite.Group()            # addons da nave
        
        # add jet component   
        pos = [self.col_rect.centerx, self.col_rect.bottom]
        size = (settings.surf_player['jets'][0].get_width()*2, settings.surf_player['jets'][0].get_height()*2)    
        self.components.add(Jet(pos, size, self.speed))
                                
        # Inicializa posição.
        dx = self.col_rect.centerx
        dy = self.col_rect.centery
        self.col_rect.move_ip(pos[0] - dx, pos[1] - dy + 100)        
        for comp in self.components:
            comp.col_rect.move_ip(pos[0] - dx, pos[1] - dy + 100)
                    
        #change ship sprite
        self.curr_surf = self.surfs_scaled[1]
    
    # definindo a função mover(), que registra a posição de um jogador
    def move(self):  
        self.borda_esquerda = 0
        self.borda_superior = 0
        self.borda_direita = settings.disp_size[0]
        self.borda_inferior = settings.disp_size[1]
        
        if self.teclas['esquerda'] and self.col_rect.left > self.borda_esquerda:
            self.col_rect.x -= self.speed
            for comp in self.components:    # move components all along
                comp.col_rect.x -= comp.speed            
        if self.teclas['direita'] and self.col_rect.right < self.borda_direita:
            self.col_rect.x += self.speed
            for comp in self.components:
                comp.col_rect.x += comp.speed
        if self.teclas['cima'] and self.col_rect.top > self.borda_superior:
            self.col_rect.y -= self.speed
            for comp in self.components:
                comp.col_rect.y -= comp.speed
        if self.teclas['baixo'] and self.col_rect.bottom < self.borda_inferior:
            self.col_rect.y += self.speed
            for comp in self.components:
                comp.col_rect.y += comp.speed
       
        # atualiza posição mouse
        #pygame.mouse.set_pos(self.col_rect.centerx, self.col_rect.centery)        
    
    def update(self):
        self.counter += 1 
        # verificando extra power ups
        size = (settings.surf_player['extra'][0].get_width(), settings.surf_player['extra'][0].get_height())
        if settings.ups == 2 and len(self.components)<settings.ups:            
            pos = [self.col_rect.center[0]+50, self.col_rect.top-20]            
            self.components.add(Power(pos, size, self.speed, rotate = -15))
        elif settings.ups == 3 and len(self.components)<settings.ups:
            pos = [self.col_rect.center[0]-50, self.col_rect.top-20]
            self.components.add(Power(pos, size, self.speed, rotate = 15))
        elif settings.ups == 4 and len(self.components)<settings.ups:
            pos = [self.col_rect.center[0]-100, self.col_rect.top-20]
            self.components.add(Power(pos, size, self.speed, rotate = 30))
        elif settings.ups == 5 and len(self.components)<settings.ups:
            pos = [self.col_rect.center[0]+100, self.col_rect.top-20]
            self.components.add(Power(pos, size, self.speed, rotate = -30))       
               
        # Movimentando a nave  
        if settings.last_message:
            message = settings.last_message
            # messages down_esquerda up_esquerda down_direita ....
            split = str.split(message,'_')
            type = split[0]
            seta = split[1]
            press = True if 'down' else False
            if seta == 'espaco':
                self.new_rocket()
            else:
                self.teclas[seta] = press            
                
        self.move()
                  
        #desenhando componentes e etc.
        self.components.update()
        self.rockets.update()
        
        # desenhando jogador(nave). 
        '''if settings.ups >= 3 and settings.ups < 5:
            self.curr_surf = self.surfs_scaled[1]
        elif settings.ups == 5:
            self.curr_surf = self.surfs_scaled[2]'''
        self.draw(settings)  
        
        #draw shield        
        center = list(self.col_rect.center)
        center[1] = center[1]+10
        if settings.life == 3:            
            pygame.draw.circle(settings.window, 'blue', center, 50, width=1)
            pygame.draw.circle(settings.window, 'blue', center, 45, width=1)             
        elif settings.life == 2:    
            pygame.draw.circle(settings.window, 'blue', center, 45, width=1)
              
    
    def new_rocket(self):
        if self.counter >= self.delay_rocket:
            pos = [self.col_rect.centerx, self.col_rect.top]
            size = (settings.surf_player['rocket'][0].get_width(), settings.surf_player['rocket'][0].get_height())
            #speed = [0,-15]
            rotate = 0
            for i in range(1,settings.ups+1): 
                if i == 1: 
                    pos[0] = self.col_rect.centerx           
                    speed = [0,-15]
                    rotate = 0
                if i == 2: 
                    pos[0] = self.col_rect.centerx+50
                    speed = [2,-15]
                    rotate = 0
                if i == 3: 
                    pos[0] = self.col_rect.centerx-50
                    speed = [-2,-15]
                    rotate = 0
                if i == 4: 
                    pos[0] = self.col_rect.centerx-100 
                    speed = [-5,-15] 
                    rotate = 30  
                if i == 5: 
                    pos[0] = self.col_rect.centerx+100 
                    speed = [5,-15] 
                    rotate = -30
                rocket = Rocket(pos, size, speed, rotate)
                rocket.col_rect.center = pos                  
                self.rockets.add(rocket)           
            rocket.shoot()
            self.counter = 0 