import pygame

class Laser():    
    def __init__(self, rect, image):        
        # valor por objet        
        self.image = image
        self.objRect = rect
        self.speed = (0,-15)   # velocidade do raio              
        
        
    # definindo a função mover
    def move(self):
        self.objRect.x += self.speed[0]
        self.objRect.y += self.speed[1]
        
    
    def update(self, window, lasers):              
        # Movimentando e desenhando os lasers.
        for laser in lasers:
            laser.move()
            window.blit(laser.image, laser.objRect)
                       
        #Eliminando os lasers que passam pelo topo da janela.
        for laser in lasers[:]:
            base_laser = laser.objRect.bottom
            if base_laser < 0:
                lasers.remove(laser)
        return lasers
    
    
    
        