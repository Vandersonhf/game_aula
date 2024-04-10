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
        self.disp_size = disp_size
        self._posX = disp_size[0]/2
        self._posY = disp_size[1]-50
        self.objRect = pygame.Rect(self._posX, self._posY, LARGURANAVE, ALTURANAVE)
        self.imagem = imagem
    
    # definindo a função mover(), que registra a posição de um jogador
    def move(self):
        self.borda_esquerda = 0
        self.borda_superior = 0
        self.borda_direita = self.disp_size[0]
        self.borda_inferior = self.disp_size[1]
        
        if self.esquerda and self.objRect.left > self.borda_esquerda:
            self.objRect.x -= self.speed
        if self.direita and self.objRect.right < self.borda_direita:
            self.objRect.x += self.speed
        if self.cima and self.objRect.top > self.borda_superior:
            self.objRect.y -= self.speed
        if self.baixo and self.objRect.bottom < self.borda_inferior:
            self.objRect.y += self.speed
        
    def update(self, window, rocks, lasers):
        # Movimentando e desenhando jogador(nave).
        self.move()
        window.blit(self.imagem, self.objRect)
        
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
    
    