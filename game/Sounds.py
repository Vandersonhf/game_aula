import pygame

class Sounds():
    def __init__(self):
        # Configurando o som.
        self.somFinal = pygame.mixer.Sound('sound/Raycast_lose.wav')
        self.somRecorde = pygame.mixer.Sound('sound/Raycast_start.wav')
        self.somTiro = pygame.mixer.Sound('sound/missile.wav')
        self.somTiro.set_volume(0.3)
        self.somFinal.set_volume(0.3)
        pygame.mixer.music.load('sound/space.mp3')