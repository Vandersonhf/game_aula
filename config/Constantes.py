import pygame

# carregando imagens
imagemTubarao = pygame.image.load('images/shark1.png')
imagemPeixe = pygame.image.load('images/p1.png')
imagemFundo = pygame.image.load('images/sea.jpg')

# Set the size for the image
PLAYER_SIZE = (200, 100) 
ENEMY_SIZE = (100, 50) 
# Scale the image to your needed size
imagemTubarao = pygame.transform.scale(imagemTubarao, PLAYER_SIZE)
imagemPeixe =  pygame.transform.scale(imagemPeixe, ENEMY_SIZE)
imagemPeixe =  pygame.transform.flip(imagemPeixe, flip_x=True, flip_y=False)

# definindo algumas constantes
LARGURAJANELA = 1000
ALTURAJANELA = 800
LARGURAPEIXE = imagemPeixe.get_width()
ALTURAPEIXE = imagemPeixe.get_height()
LARGURATUBARAO = imagemTubarao.get_width()
ALTURATUBARAO = imagemTubarao.get_height()
VEL = 6
ITERACOES = 30

# scale background
#imagemFundo =  pygame.transform.scale(imagemFundo, (LARGURAJANELA,ALTURAJANELA))

# configurando o som
pygame.mixer.init()
pygame.mixer.music.load('sound/loop.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0)

somComer = pygame.mixer.Sound('sound/eat.mp3')
somAtivado = True