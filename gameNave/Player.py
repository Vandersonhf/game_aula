import pygame
from .Rocket import Rocket
from .Sprite import Sprite
from .Rock import Rock
from .Mob import Mob
from .Jet import Jet
from .Surfaces import Surfaces
from .Sounds import Sounds
from .Display import Display

class Player(Sprite):
    def __init__(self, surfs:Surfaces, sounds:Sounds, startx:int, starty:int, display:Display):             
        self.surfs = surfs
        self.surf_jets = surfs.surf_jets # several surfaces
        self.disp_size = display.disp_size 
        self.display = display
        self.sounds = sounds          
        #scale = 1
        new_size = (surfs.surf_ship.get_width()/5, surfs.surf_ship.get_height()/5)
        super().__init__([surfs.surf_ship], (startx,starty), new_size)     #call superclass
       
        # teclas
        self.esquerda = False
        self.direita = False 
        self.cima = False
        self.baixo = False 
                                       
        self.speed = 10      # velocidade da nave 
        self.delay_rocket = 10
        self.counter = 0        
                
        self.rockets = pygame.sprite.Group()         # lista com os rockets
        self.components = pygame.sprite.Group()    # addons da nave
        
        # add jet component
        new_size = (self.surf_jets[0].get_width()*2, self.surf_jets[0].get_height()*2)
        self.components.add(Jet(self.surfs, self.objRect.centerx, 
                                self.objRect.bottom, new_size, self.speed))
                
        # Inicializa posição.
        dx = self.objRect.centerx
        dy = self.objRect.centery
        self.objRect.move_ip(startx - dx, starty - dy)        
        for comp in self.components:
            comp.objRect.move_ip(startx - dx, starty - dy)
                
        #debug
        #self.components.add(Jet([self.surf_mask], self.objRect.centerx,
        #                        self.objRect.centery-10, self.speed))
           
               
    # definindo a função mover(), que registra a posição de um jogador
    def move(self):  
        self.borda_esquerda = 0
        self.borda_superior = 0
        self.borda_direita = self.disp_size[0]
        self.borda_inferior = self.disp_size[1]
        
        if self.esquerda and self.objRect.left > self.borda_esquerda:
            self.objRect.x -= self.speed
            for comp in self.components:    # move components all along
                comp.objRect.x -= comp.speed            
        if self.direita and self.objRect.right < self.borda_direita:
            self.objRect.x += self.speed
            for comp in self.components:
                comp.objRect.x += comp.speed
        if self.cima and self.objRect.top > self.borda_superior:
            self.objRect.y -= self.speed
            for comp in self.components:
                comp.objRect.y -= comp.speed
        if self.baixo and self.objRect.bottom < self.borda_inferior:
            self.objRect.y += self.speed
            for comp in self.components:
                comp.objRect.y += comp.speed
       
        # atualiza posição mouse
        pygame.mouse.set_pos(self.objRect.centerx, self.objRect.centery)
        
        
    def update(self, rocks:list[Rock], mobs:list[Mob], score:int):
        self.counter += 1        
        # Movimentando a nave       
        self.move()
                
        #desenhando componentes e etc.
        self.components.update(self.display)
        self.rockets.update(self.display)
        
        # desenhando jogador(nave). 
        self.draw(self.display.window) 
           
        # verifica colisão
        return self.check_collision(rocks, mobs, score)                
            
    
    def check_collision(self, rocks:list[Rock], mobs:list[Mob], score:int):
        # Checando se jogador ou algum rocket colidiu com algum rock.
        for rock in rocks:
            jogadorColidiu = False
            if not rock.exploded:
                if self.objRect.colliderect(rock.objRect):
                    offset = (rock.objRect.x - self.objRect.x, rock.objRect.y - self.objRect.y)
                    jogadorColidiu = self.mask.overlap(rock.mask, offset)
                if jogadorColidiu:  
                    self.sounds.somExplosao_player.play()          
                    return False, score
            rocket:Rocket
            for rocket in self.rockets:
                if not rock.exploded:
                    rocketColidiu = rocket.objRect.colliderect(rock.objRect)
                    if rocketColidiu:
                        rock.explode()                                   
                        self.rockets.remove(rocket)
                        score = score + 50
                        
        # Checando se jogador ou algum rocket colidiu com algum mob.
        for mob in mobs:
            jogadorColidiu = False
            if not mob.exploded:
                if self.objRect.colliderect(mob.objRect):
                    offset = (mob.objRect.x - self.objRect.x, mob.objRect.y - self.objRect.y)
                    jogadorColidiu = self.mask.overlap(mob.mask, offset)
                if jogadorColidiu:  
                    self.sounds.somExplosao_player.play()          
                    return False, score
            rocket:Rocket
            for rocket in self.rockets:
                if not mob.exploded:
                    rocketColidiu = rocket.objRect.colliderect(mob.objRect)
                    if rocketColidiu:
                        mob.explode()                                   
                        self.rockets.remove(rocket)
                        score = score + 100
            for fire in mob.fires:
                if self.objRect.colliderect(fire.objRect):
                    offset = (fire.objRect.x - self.objRect.x, fire.objRect.y - self.objRect.y)
                    jogadorColidiu = self.mask.overlap(fire.mask, offset)
                if jogadorColidiu:  
                    self.sounds.somExplosao_player.play()          
                    return False, score            
            
        return True, score
        
         
    def new_rocket(self):
        if self.counter >= self.delay_rocket:
            rocket = Rocket(self.surfs, self.sounds, self.objRect.centerx, self.objRect.top, (0,-15))                    
            self.rockets.add(rocket)
            rocket.shoot()
            self.counter = 0