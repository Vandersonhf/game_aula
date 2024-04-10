import pygame

class Player():
    def __init__(self, disp_size, imagem, LARGURANAVE, ALTURANAVE):
        # teclas
        self.esquerda = False
        self.direita = False 
        self.cima = False
        self.baixo = False 
        
        #nave        
        self.speed = 5      # velocidade da nave
        self.largura = LARGURANAVE
        self.altura = ALTURANAVE
        self.disp_size = disp_size
        self._posX = disp_size[0]/2
        self._posY = disp_size[1]-100
        self.objRect = pygame.Rect(self._posX, self._posY, LARGURANAVE, ALTURANAVE)
        self.imagem = imagem
                              
        self.fly_cycle = [pygame.image.load(f"images/jet{i:0>2}.png") for i in range(1,4)]
        self.animation_index = 0
        self.delay = 0
        self.jet_delay = 7
        self.jet = self.fly_cycle[0]
        self.objRect2 = pygame.Rect(self._posX, self._posY-ALTURANAVE,
                                   self.fly_cycle[0].get_width(), self.fly_cycle[0].get_height())
        
        # Incializa movimento.
        centroX_jogador = self.objRect.centerx
        centroY_jogador = self.objRect.centery
        self.objRect.move_ip(self._posX - centroX_jogador, self._posY - centroY_jogador)
        
        # jet precisa acompanhar
        centroX_jogador = self.objRect2.centerx
        centroY_jogador = self.objRect2.centery - self.altura/2
        self.objRect2.move_ip(self._posX - centroX_jogador, self._posY - centroY_jogador)
        
        # criar 3 retangulos de colisão em forma de triangulo
        self.objRect11 = pygame.Rect(self.objRect.centerx-LARGURANAVE/2, 
                                     self.objRect.centery+ALTURANAVE/2, LARGURANAVE, 2)
        self.objRect12 = pygame.Rect(self.objRect.centerx-LARGURANAVE/2, 
                                     self.objRect.centery-ALTURANAVE/2, LARGURANAVE, 2)
        self.objRect13 = pygame.Rect(self.objRect.centerx-LARGURANAVE/2, 
                                     self.objRect.centery-ALTURANAVE/2, 2, ALTURANAVE)
        self.objRect14 = pygame.Rect(self.objRect.centerx+LARGURANAVE/2, 
                                     self.objRect.centery-ALTURANAVE/2, 2, ALTURANAVE)
        
    
    
    # definindo a função mover(), que registra a posição de um jogador
    def move(self):
        self.borda_esquerda = 0
        self.borda_superior = 0
        self.borda_direita = self.disp_size[0]
        self.borda_inferior = self.disp_size[1]
        
        if self.esquerda and self.objRect.left > self.borda_esquerda:
            self.objRect.x -= self.speed
            self.objRect2.x -= self.speed
        if self.direita and self.objRect.right < self.borda_direita:
            self.objRect.x += self.speed
            self.objRect2.x += self.speed
        if self.cima and self.objRect.top > self.borda_superior:
            self.objRect.y -= self.speed
            self.objRect2.y -= self.speed
        if self.baixo and self.objRect.bottom < self.borda_inferior:
            self.objRect.y += self.speed
            self.objRect2.y += self.speed
        
        
    def update(self, window, rocks, lasers):
        # Movimentando e desenhando jogador(nave).
        self.move()
        self.fly_animation()
        window.blit(self.imagem, self.objRect)
        window.blit(self.jet, self.objRect2)
        #pygame.draw.rect(window,(255,255,255),self.objRect11)
        #pygame.draw.rect(window,(255,255,255),self.objRect12)
        #pygame.draw.rect(window,(255,255,255),self.objRect13)
        #pygame.draw.rect(window,(255,255,255),self.objRect14)
        
        # Checando se jogador ou algum laser colidiu com algum rock.
        for rock in rocks[:]:
            jogadorColidiu = self.objRect.colliderect(rock.objRect)
            if jogadorColidiu:            
                return False
            for laser in lasers[:]:
                laserColidiu = laser.objRect.colliderect(rock.objRect)
                if laserColidiu:
                    lasers.remove(laser)
                    rocks.remove(rock)
        return True
    
    
    def fly_animation(self):
        self.jet = self.fly_cycle[self.animation_index]        
        
        if self.animation_index < len(self.fly_cycle)-1:
            self.delay += 1
            if self.delay > self.jet_delay:
                self.animation_index += 1
                self.delay = 0
        else:
            self.animation_index = 0  
    