import pygame

# Definindo as cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# carregando imagens
imagemTubarao = pygame.image.load('images/shark1.png')
#imagemPeixe = pygame.image.load('images/p1.png')
imagemPeixe1 = pygame.image.load('images/p1.png')
imagemPeixe2 = pygame.image.load('images/p2.png')
imagemPeixe3 = pygame.image.load('images/p3.png')
imagemFundo = pygame.image.load('images/sea.jpg')

# Set the size for the image
PLAYER_SIZE = (200, 100) 
ENEMY_SIZE = (100, 50) 
# Scale the image to your needed size
imagemTubarao = pygame.transform.scale(imagemTubarao, PLAYER_SIZE)
imagemPeixe1 =  pygame.transform.scale(imagemPeixe1, ENEMY_SIZE)
imagemPeixe1 =  pygame.transform.flip(imagemPeixe1, flip_x=True, flip_y=False)
imagemPeixe2 =  pygame.transform.scale(imagemPeixe2, ENEMY_SIZE)
imagemPeixe2 =  pygame.transform.flip(imagemPeixe2, flip_x=True, flip_y=False)
imagemPeixe3 =  pygame.transform.scale(imagemPeixe3, ENEMY_SIZE)
imagemPeixe3 =  pygame.transform.flip(imagemPeixe3, flip_x=True, flip_y=False)

# definindo algumas constantes
LARGURAJANELA = 1000
ALTURAJANELA = 800
LARGURAPEIXE = imagemPeixe1.get_width()
ALTURAPEIXE = imagemPeixe1.get_height()
LARGURATUBARAO = imagemTubarao.get_width()
ALTURATUBARAO = imagemTubarao.get_height()
VEL = 6
ITERACOES = 50
# determina valores para novas fases
CICLOS = 1000
INTERVAL = 200

# scale background
imagemFundo =  pygame.transform.scale(imagemFundo, (LARGURAJANELA,ALTURAJANELA))

# configurando o som
pygame.mixer.init()
pygame.mixer.music.load('sound/loop.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0)

#somComer = pygame.mixer.Sound('sound/eat.mp3')
somComer1 = pygame.mixer.Sound('sound/eat1.mp3')
somComer2 = pygame.mixer.Sound('sound/eat2.mp3')
somComer3 = pygame.mixer.Sound('sound/eat3.mp3')
somAtivado = True