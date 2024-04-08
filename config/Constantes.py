import pygame

# Carregando as imagens.
imagemNave = pygame.image.load('images/nave.png')
imagemAsteroide = pygame.image.load('images/asteroid.png')
imagemRaio = pygame.image.load('images/missil.png')
imagemFundo = pygame.image.load('images/space.jpg')
 
LARGURAJANELA = 600 # largura da janela
ALTURAJANELA = 600 # altura da janela
CORTEXTO = (255, 255, 255) # cor do texto (branca)
QPS = 40 # quadros por segundo
TAMMINIMO = 10 # tamanho mínimo do asteroide
TAMMAXIMO = 40 # tamanho máximo do asteroide
VELMINIMA = 1 # velocidade mínima do asteroide
VELMAXIMA = 8 # velocidade máxima do asteroide
ITERACOES = 60 # número de iterações antes de criar um novo asteroide
VELJOGADOR = 5 # velocidade da nave
VELRAIO = (0,-15) # velocidade do raio

LARGURANAVE = imagemNave.get_width()
ALTURANAVE = imagemNave.get_height()
LARGURARAIO = imagemRaio.get_width()
ALTURARAIO = imagemRaio.get_height()

#redimensionando a imagem de fundo.
imagemFundoRedim = pygame.transform.scale(imagemFundo,(LARGURAJANELA, ALTURAJANELA))

# Configurando a fonte.
fonte = pygame.font.Font(None, 48)

# Configurando o som.
somFinal = pygame.mixer.Sound('sound/Raycast_lose.wav')
somRecorde = pygame.mixer.Sound('sound/Raycast_start.wav')
somTiro = pygame.mixer.Sound('sound/missile.wav')
somTiro.set_volume(0.3)
somFinal.set_volume(0.3)
pygame.mixer.music.load('sound/space.mp3')