import pygame

class Sounds():
    def __init__(self):
        # Configurando o som.
        self.somFinal = pygame.mixer.Sound('sound/Raycast_lose.wav')
        self.somStart = pygame.mixer.Sound('sound/Raycast_start.wav')
        self.somTiro = pygame.mixer.Sound('sound/laser1.mp3')
        self.somTiro.set_volume(0.2)
        self.somFinal.set_volume(0.3)
        pygame.mixer.music.load('sound/space.mp3')
        #self.somExplosao = pygame.mixer.Sound('sound/boom.wav')
        self.somExplosao = pygame.mixer.Sound('sound/explode2.mp3')
        self.somExplosao.set_volume(0.6)
        self.somExplosao_nave = pygame.mixer.Sound('sound/explode0.mp3')
        self.somExplosao_nave.set_volume(0.6)
        self.somExplosao_player = pygame.mixer.Sound('sound/explode1.mp3')
        self.somExplosao_player.set_volume(0.6)
        
        self.somFire = pygame.mixer.Sound('sound/fire0.mp3')
        self.somFire.set_volume(0.2)