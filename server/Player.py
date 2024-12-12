from .Sprite import Sprite
import pygame
from .Settings import settings
import random

class Player(Sprite):
    def __init__(self, type=1, socket=None):  
        self.type = type
        self.socket = socket      
        pos = [settings.disp_size[0]*0.5, settings.disp_size[1]*0.5]
        size = (settings.surf_player['ship'][0].get_width()/5, settings.surf_player['ship'][0].get_height()/5)         
        
        super().__init__(size, pos, settings.surf_player['ship'], settings.sound_player['ship'])
        
        self.teclas = {'esquerda':False, 'direita':False, 'cima':False, 'baixo': False}
        self.speed = 10      # velocidade da nave 
        self.delay_rocket = 10
        self.counter = 0
        
        self.score: int = 0        
        self.life = 3
        self.ups = 1
        
        self.rockets = pygame.sprite.Group()         # lista com os rockets
        self.components = pygame.sprite.Group()            # addons da nave
        
        # add jet component   
        pos = [self.col_rect.centerx, self.col_rect.bottom]
        size = (settings.surf_player['jets'][0].get_width()*2, settings.surf_player['jets'][0].get_height()*2)    
        self.components.add(Jet(pos, size, self.speed))
                                
        # Inicializa posição.
        dx = self.col_rect.centerx
        dy = self.col_rect.centery        
        if self.type == 1:
            self.col_rect.move_ip(pos[0] - dx, pos[1] - dy)        
            for comp in self.components:
                comp.col_rect.move_ip(pos[0] - dx, pos[1] - dy)
        elif self.type == 2:
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
            
    def update_power(self):
        # verificando extra power ups
        size = (settings.surf_player['extra'][0].get_width(), settings.surf_player['extra'][0].get_height())
        if self.ups == 2 and len(self.components)<self.ups:            
            pos = [self.col_rect.center[0]+50, self.col_rect.top-20]            
            self.components.add(Power(pos, size, self.speed, rotate = -15))
        elif self.ups == 3 and len(self.components)<self.ups:
            pos = [self.col_rect.center[0]-50, self.col_rect.top-20]
            self.components.add(Power(pos, size, self.speed, rotate = 15))
        elif self.ups == 4 and len(self.components)<self.ups:
            pos = [self.col_rect.center[0]-100, self.col_rect.top-20]
            self.components.add(Power(pos, size, self.speed, rotate = 30))
        elif self.ups == 5 and len(self.components)<self.ups:
            pos = [self.col_rect.center[0]+100, self.col_rect.top-20]
            self.components.add(Power(pos, size, self.speed, rotate = -30))  
    
    def update(self, player1 = True):
        self.counter += 1 
               
        # Movimentando a nave       
        if player1: self.move()
                
        #desenhando componentes e etc.
        self.components.update()
        self.rockets.update(self.ups)
        
        # desenhando jogador(nave). 
        if self.ups == 5:
            self.curr_surf = self.surfs_scaled[2]
        self.draw(settings)  
        
        #draw shield        
        center = list(self.col_rect.center)
        center[1] = center[1]+10
        if self.life == 3:            
            pygame.draw.circle(settings.window, 'blue', center, 50, width=1)
            pygame.draw.circle(settings.window, 'blue', center, 45, width=1)             
        elif self.life == 2:    
            pygame.draw.circle(settings.window, 'blue', center, 45, width=1)
     
    
    def check_collision (self, asteroids, mobs, pows, shields, boss):        
        # Checando se jogador ou algum rocket colidiu com algum rock.
        for rock in asteroids:
            jogadorColidiu = False
            #player colide asteroid
            if not rock.dead:
                if self.col_rect.colliderect(rock.col_rect):
                    offset = (rock.col_rect.x - self.col_rect.x, rock.col_rect.y - self.col_rect.y)
                    jogadorColidiu = self.mask.overlap(rock.mask, offset)
                if jogadorColidiu: 
                    rock.explode()
                    self.score = self.score + 50
                    if self.socket and settings.multiplayer:
                        if self.type == 1: message = 'dead_rock_score_player1_50_'+str(rock.ID)+'_' 
                        if self.type == 2: message = 'dead_rock_score_player2_50_'+str(rock.ID)+'_'                       
                        while len(message) < 64: message += '0'
                        self.socket.send_message(message)
                    return self.reduce_life()
            #player destroy asteroid
            for rocket in self.rockets:
                if not rock.dead:
                    rocketColidiu = rocket.col_rect.colliderect(rock.col_rect)
                    if rocketColidiu:
                        rock.explode()                                   
                        self.rockets.remove(rocket)
                        self.score = self.score + 50
                        if self.socket and settings.multiplayer:
                            if self.type == 1: message = message = 'dead_rock_score_player1_50_'\
                                +str(rock.ID)+'_rocket_'+str(rocket.ID)+'_'
                            if self.type == 2: message = message = 'dead_rock_score_player2_50_'\
                                +str(rock.ID)+'_rocket_'+str(rocket.ID)+'_'                       
                            while len(message) < 64: message += '0'
                            self.socket.send_message(message)
            # spawn life shield
            if rock.dead and rock.idx_ani >= len(rock.list_surf)-1 and rock.delay > rock.delay_ani-1:                   
                r = random.randint(1,settings.luck)                        
                if r == 1 and self.life < 3:
                    settings.ID += 1
                    shield = ShieldUP(settings.ID, rock.col_rect.center, (50,50))                               
                    shields.add(shield)                     
                    if self.socket and settings.multiplayer:
                        x = rock.col_rect.center[0]
                        y = rock.col_rect.center[1]
                        message = 'shield_'+str(settings.ID)+'_'+str(x)+'_'+str(y)\
                            +'_50_50_'
                        while len(message) < 64: message += '0'
                        self.socket.send_message(message)
        # Checando se jogador ou algum rocket colidiu com algum mob.
        for mob in mobs:
            jogadorColidiu = False
            # check player colide enemy
            if not mob.dead:
                if self.col_rect.colliderect(mob.col_rect):
                    offset = (mob.col_rect.x - self.col_rect.x, mob.col_rect.y - self.col_rect.y)
                    jogadorColidiu = self.mask.overlap(mob.mask, offset)
                if jogadorColidiu: 
                    mob.life -= 1
                    if self.socket and settings.multiplayer:                         
                        if self.type == 1: message = message = 'hurt_mob_player1_'\
                            +str(mob.ID)+'_'
                        if self.type == 2: message = message = 'hurt_mob_player2_'\
                            +str(mob.ID)+'_'                                           
                        while len(message) < 64: message += '0'
                        self.socket.send_message(message)
                    if mob.life == 0: 
                        mob.explode()
                        self.score = self.score + 100
                        if self.socket and settings.multiplayer:
                            if self.type == 1: message = message = 'dead_mob_score_player1_100_'\
                                +str(mob.ID)+'_'
                            if self.type == 2: message = message = 'dead_mob_score_player2_100_'\
                                +str(mob.ID)+'_'                       
                            while len(message) < 64: message += '0'
                            self.socket.send_message(message) 
                    else: 
                        mob.sounds[0].play()                    
                    return self.reduce_life()
            # check player destroy enemy
            for rocket in self.rockets:
                if not mob.dead:
                    rocketColidiu = rocket.col_rect.colliderect(mob.col_rect)
                    if rocketColidiu:
                        mob.life -= 1
                        if self.socket and settings.multiplayer:                                       
                            if self.type == 1: message = message = 'hurt_mob_player1_'\
                                +str(mob.ID)+'_rocket_'+str(rocket.ID)+'_'
                            if self.type == 2: message = message = 'hurt_mob_player2_'\
                                +str(mob.ID)+'_rocket_'+str(rocket.ID)+'_'                                 
                            while len(message) < 64: message += '0'
                            self.socket.send_message(message)
                        if mob.life == 0: 
                            mob.explode()
                            self.score = self.score + 100 
                            if self.socket and settings.multiplayer:
                                if self.type == 1: message = message = 'dead_mob_score_player1_100_'\
                                    +str(mob.ID)+'_rocket_'+str(rocket.ID)+'_'
                                if self.type == 2: message = message = 'dead_mob_score_player2_100_'\
                                    +str(mob.ID)+'_rocket_'+str(rocket.ID)+'_'                       
                                while len(message) < 64: message += '0'
                                self.socket.send_message(message) 
                        else: 
                            mob.sounds[0].play()                                                       
                        self.rockets.remove(rocket)
            #power up
            if mob.dead and mob.idx_ani >= len(mob.list_surf)-1 and mob.delay > mob.delay_ani-1:                   
                r = random.randint(1,settings.luck)                        
                if r == 1 and self.ups < 5:
                    settings.ID += 1
                    pow = PowerUP(settings.ID, mob.col_rect.center, (50,50))                               
                    pows.add(pow) 
                    if self.socket and settings.multiplayer:
                        x = mob.col_rect.center[0]
                        y = mob.col_rect.center[1]
                        message = 'pow_'+str(settings.ID)+'_'+str(x)+'_'+str(y)\
                            +'_50_50_'
                        while len(message) < 64: message += '0'
                        self.socket.send_message(message)                   
            # enemy rockets hit player
            for fire in mob.rockets:
                if self.col_rect.colliderect(fire.col_rect):
                    offset = (fire.col_rect.x - self.col_rect.x, fire.col_rect.y - self.col_rect.y)
                    jogadorColidiu = self.mask.overlap(fire.mask, offset)
                if jogadorColidiu: 
                    mob.rockets.remove(fire)
                    return self.reduce_life() 
        # player get powerup
        for pow in pows:
            jogadorColidiu = False
            if not pow.dead:
                if self.col_rect.colliderect(pow.col_rect):
                    offset = (pow.col_rect.x - self.col_rect.x, pow.col_rect.y - self.col_rect.y)
                    jogadorColidiu = self.mask.overlap(pow.mask, offset)
                if jogadorColidiu:
                    if self.ups < 5:
                        self.ups += 1                    
                        pow.get()
                        self.update_power()
                        if self.socket and settings.multiplayer:
                            if self.type == 1: message = 'up_player1_'+str(self.ups)+'_'+str(pow.ID)+'_'
                            if self.type == 2: message = 'up_player2_'+str(self.ups)+'_'+str(pow.ID)+'_'
                            while len(message) < 64: message += '0'
                            self.socket.send_message(message)
                        pow.kill() 
        # player get shield - life
        for shield in shields:
            jogadorColidiu = False
            if not shield.dead:
                if self.col_rect.colliderect(shield.col_rect):
                    offset = (shield.col_rect.x - self.col_rect.x, shield.col_rect.y - self.col_rect.y)
                    jogadorColidiu = self.mask.overlap(shield.mask, offset)
                if jogadorColidiu:
                    if self.life < 3:
                        self.life += 1                    
                        shield.get()
                        if self.socket and settings.multiplayer:
                            if self.type == 1: message = 'life_player1_'+str(self.life)+'_'+str(shield.ID)+'_'
                            if self.type == 2: message = 'life_player2_'+str(self.life)+'_'+str(shield.ID)+'_'
                            while len(message) < 64: message += '0'
                            self.socket.send_message(message)
                        shield.kill()    
        # check boss
        jogadorColidiu = False
        if boss != None:
            # check player colide boss
            if not boss.dead:
                if self.col_rect.colliderect(boss.col_rect):
                    offset = (boss.col_rect.x - self.col_rect.x, boss.col_rect.y - self.col_rect.y)
                    jogadorColidiu = self.mask.overlap(boss.mask, offset)
                if jogadorColidiu: 
                    boss.life -= 1
                    if self.socket and settings.multiplayer:                          
                        if self.type == 1: message = message = 'hurt_boss_player1_'
                        if self.type == 2: message = message = 'hurt_boss_player2_'                 
                        while len(message) < 64: message += '0'
                        self.socket.send_message(message)
                    if boss.life == 0: 
                        boss.explode()
                        self.score = self.score + 1000 
                        if self.socket and settings.multiplayer:
                            if self.type == 1: message = message = 'dead_boss_score_player1_1000_'
                            if self.type == 2: message = message = 'dead_boss_score_player2_1000_'           
                            while len(message) < 64: message += '0'
                            self.socket.send_message(message)
                    else: 
                        boss.sounds[0].play()
                    return self.reduce_life()
            # check player destroy boss
            for rocket in self.rockets:
                if not boss.dead:
                    rocketColidiu = rocket.col_rect.colliderect(boss.col_rect)
                    if rocketColidiu:
                        boss.life -= 1
                        if self.socket and settings.multiplayer:
                            message = message = 'hurt_boss_'  
                            if self.type == 1: message = message = 'hurt_boss_player1_'\
                                +'_rocket_'+str(rocket.ID)+'_'
                            if self.type == 2: message = message = 'hurt_boss_player2_'\
                                +'_rocket_'+str(rocket.ID)+'_'                               
                            while len(message) < 64: message += '0'
                            self.socket.send_message(message)
                        if boss.life == 0: 
                            boss.explode()
                            self.score = self.score + 1000
                            if self.socket and settings.multiplayer:
                                if self.type == 1: message = message = 'dead_boss_score_player1_1000_'\
                                    +'_rocket_'+str(rocket.ID)+'_'
                                if self.type == 2: message = message = 'dead_boss_score_player2_1000_'\
                                    +'_rocket_'+str(rocket.ID)+'_'                       
                                while len(message) < 64: message += '0'
                                self.socket.send_message(message)
                        else: 
                            boss.sounds[0].play()
                        self.rockets.remove(rocket)                                              
            # enemy rockets hit player
            for fire in boss.rockets:
                if self.col_rect.colliderect(fire.col_rect):
                    offset = (fire.col_rect.x - self.col_rect.x, fire.col_rect.y - self.col_rect.y)
                    jogadorColidiu = self.mask.overlap(fire.mask, offset)
                if jogadorColidiu: 
                    boss.rockets.remove(fire)
                    return self.reduce_life()                    
        return True
        
    def reduce_life(self):
        settings.sound_player['ship'][0].play()
        if self.life >= 1:
            if not eval(settings.hack['god']): 
                self.life -= 1
                if self.socket and settings.multiplayer:
                    if self.type == 1: message = 'life_player1_'+str(self.life)+'_'
                    if self.type == 2: message = 'life_player2_'+str(self.life)+'_'
                    while len(message) < 64: message += '0'
                    self.socket.send_message(message)
                if self.life == 0: return False
            return True
        else: return False              
    
    def new_rocket(self, socket=None):
        if self.counter >= self.delay_rocket:
            pos = [self.col_rect.centerx, self.col_rect.top]
            size = (settings.surf_player['rocket'][0].get_width(), settings.surf_player['rocket'][0].get_height())
            #speed = [0,-15]
            rotate = 0
            for i in range(1,self.ups+1): 
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
                settings.ID += 1
                rocket = Rocket(settings.ID, pos, size, speed, rotate)
                rocket.col_rect.center = pos                  
                self.rockets.add(rocket)
                if settings.multiplayer:
                    message = 'rocket_'+str(settings.ID)+'_'+str(pos[0])+'_'+str(pos[1])\
                        +'_'+str(size[0])+'_'+str(size[1])+'_'+str(speed[0])+'_'+str(speed[1])\
                        +'_'+str(rotate)+'_'
                    while len(message) < 64: message += '0'
                    socket.send_message(message)      
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
        
      
class PowerUP(Sprite):    
    def __init__(self, ID, pos, size):         
        super().__init__(size, pos, settings.surf_enemy['pows'], settings.sound_enemy['pows'])
        
        self.speed = [0,0]   # velocidade do raio     
        self.time = 200         
        self.ID = ID            
        
    def get(self):
        self.sounds[0].play()
                      
    def update(self): 
        self.time -= 1 
        if self.time > 0: self.draw(settings)
        else: self.kill()
        

class ShieldUP(Sprite):    
    def __init__(self, ID, pos, size):         
        super().__init__(size, pos, settings.surf_enemy['shield'], settings.sound_enemy['pows'])
        
        self.speed = [0,0]   # velocidade do raio     
        self.time = 300    
        self.ID = ID                 
        
    def get(self):
        self.sounds[0].play()
                      
    def update(self): 
        self.time -= 1 
        if self.time > 0: self.draw(settings)
        else: self.kill()  
        
        
class Rocket(Sprite):    
    def __init__(self, ID, pos, size, speed, rotate=0):
        super().__init__(size, pos, settings.surf_player['rocket'],
                         settings.sound_player['rocket'], rotate=rotate)
        
        self.speed = speed   # velocidade do raio
        self.ID = ID                          
        
    def shoot(self):
        self.sounds[0].play()
        
    # definindo a função mover
    def move(self):
        self.col_rect.x += self.speed[0]
        self.col_rect.y += self.speed[1]
           
    def update(self, ups): 
        if ups == 5: 
            self.curr_surf = self.surfs_scaled[1]
                     
        self.move()
        self.draw(settings)
        base_rocket = self.col_rect.bottom
        if base_rocket < 0:
            self.kill() 
            
  