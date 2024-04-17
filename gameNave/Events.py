import pygame
from sys import exit
from .Player import Player

class Events():
    def __init__(self):
        pass

    def checker(self, player:Player):
        #print("Tratando...")
        for evento in pygame.event.get():
            # Se for um evento QUIT
            if evento.type == pygame.QUIT:
                self.terminar()  
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.terminar()   
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:                    
                    player.esquerda = True
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    player.direita = True
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    player.cima = True
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    player.baixo = True
                if evento.key == pygame.K_SPACE:                                           
                    player.new_rocket(player.rockets)
                            
            # quando uma tecla é solta
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    player.esquerda = False
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    player.direita = False
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    player.cima = False
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    player.baixo = False
            
            # mouse
            if evento.type == pygame.MOUSEMOTION:
                # Se o mouse se move, movimenta jogador para onde o cursor está.
                dx = player.objRect.centerx
                dy = player.objRect.centery
                #pygame.mouse.set_pos(dx,dy)
                player.objRect.move_ip(evento.pos[0] - dx, evento.pos[1] - dy)                
                for comp in player.components:
                    comp.objRect.move_ip(evento.pos[0] - dx, evento.pos[1] - dy)
                                                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                player.new_rocket(player.rockets)                         
        return True


    def aguardarEntrada(self):
        # Aguarda entrada por teclado ou clique do mouse no “x” da janela.
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.terminar()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.terminar()
                    if evento.key == pygame.K_F1:
                        return
                
    def terminar(self):
        # Termina o programa.
        pygame.quit()
        exit() 