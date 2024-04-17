import pygame
from .Rocket import Rocket
from .Sprite import Sprite
from .Enemy import Enemy
from .Jet import Jet
from .Surfaces import Surfaces
from .Sounds import Sounds
from .Display import Display

class Player(Sprite):
    def __init__(self, surfaces:Surfaces, sounds:Sounds, startx, starty, display:Display):             
        self.surf = surfaces.surf_ship
        self.surf_rocket = surfaces.surf_rocket
        self.surf_jets = surfaces.surf_jets # several surfaces
        self.disp_size = display.disp_size 
        self.display = display
        self.sounds = sounds          
        scale = 1 
        super().__init__(self.surf, startx, starty, scale)     #call superclass
       
        # teclas
        self.esquerda = False
        self.direita = False 
        self.cima = False
        self.baixo = False 
                                       
        self.speed = 5      # velocidade da nave           
                
        self.rockets = pygame.sprite.Group()         # lista com os rockets
        self.components = pygame.sprite.Group()    # addons da nave
        
        # add jet component
        self.components.add(Jet(self.surf_jets, self.objRect.centerx, self.objRect.bottom))
                
        # Inicializa posição.
        dx = self.objRect.centerx
        dy = self.objRect.centery
        self.objRect.move_ip(startx - dx, starty - dy)        
        for comp in self.components:
            comp.objRect.move_ip(startx - dx, starty - dy)
            
        #define mascara de colisao
        self.mask = pygame.mask.from_surface(self.surf)
        self.surf_mask = self.mask.to_surface()
                
        #debug
        self.components.add(Jet([self.surf_mask], self.objRect.centerx, self.objRect.centery-10))
           
               
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
       
        
    def update(self, rocks:list[Enemy]):
        # Movimentando e desenhando jogador(nave).        
        self.move()
        self.draw(self.display.window)                        
                
        self.components.update(self.display)
        self.rockets.update(self.display)
                
        # Checando se jogador ou algum rocket colidiu com algum rock.
        for rock in rocks:
            jogadorColidiu = False
            if self.objRect.colliderect(rock.objRect):
                offset = (rock.objRect.x - self.objRect.x, rock.objRect.y - self.objRect.y)
                jogadorColidiu = self.mask.overlap(rock.mask, offset)
            if jogadorColidiu:            
                return False
            rocket:Rocket
            for rocket in self.rockets:
                rocketColidiu = rocket.objRect.colliderect(rock.objRect)
                if rocketColidiu:
                    self.rockets.remove(rocket)
                    rocks.remove(rock)
        return True
    
         
    def new_rocket(self, rockets):
        rocket = Rocket(self.surf_rocket, self.sounds, self.objRect.centerx, self.objRect.top)                    
        self.rockets.add(rocket)
        rocket.shoot()