import pygame
from .Laser import Laser

class Events():
    def __init__(self):
        pass

    def checker(self, player, lasers, image, fireSound, largura_raio, altura_raio):
        #print("Tratando...")
        for evento in pygame.event.get():
            # Se for um evento QUIT
            if evento.type == pygame.QUIT:
                self.terminar()
            
            # quando uma tecla é pressionada
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
                    rect = pygame.Rect(player.objRect.centerx, player.objRect.top,
                                       largura_raio, altura_raio)                        
                    laser = Laser(rect, image)                    
                    lasers.append(laser)
                    fireSound.play()
                            
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
                centroX_jogador = player.objRect.centerx
                centroY_jogador = player.objRect.centery
                player.objRect.move_ip(evento.pos[0] - centroX_jogador, evento.pos[1] - centroY_jogador)
                
                # jet precisa acompanhar
                centroX_jogador = player.objRect2.centerx
                centroY_jogador = player.objRect2.centery - player.altura/2
                player.objRect2.move_ip(evento.pos[0] - centroX_jogador, evento.pos[1] - centroY_jogador)
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                rect = pygame.Rect(player.objRect.centerx, player.objRect.top,
                                       largura_raio, altura_raio)                        
                laser = Laser(rect, image)                    
                lasers.append(laser)
                fireSound.play()
                                
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