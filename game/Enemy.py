import pygame

class Enemy():    
    def __init__(self, rect, image, speed):        
        # valor por objeto
        self.speed = speed
        self.image = image
        self.objRect = rect               
        
        
    # definindo a função mover
    def move(self):
        self.objRect.x += self.speed[0]
        self.objRect.y += self.speed[1]
        
    
    def update(self, window, disp_size, rocks):
        # Movimentando e desenhando
        for rock in rocks:
            rock.move()
            window.blit(rock.image, rock.objRect)
            
        # Eliminando os rocks que passam pela base da janela.
        for rock in rocks[:]:
            top_rock = rock.objRect.top
            if top_rock > disp_size[1]:
                rocks.remove(rock)
        return rocks
        
    
    
    
        