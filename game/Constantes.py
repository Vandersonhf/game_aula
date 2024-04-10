import pygame
import tkinter as tk

root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# disp_size = (1920, 1080)
# disp_size = (1280, 720)
# disp_size = (720, 400)
# disp_size = (640, 360)

# Carregando as imagens.
imagemNave = pygame.image.load('images/nave.png')
imagemAsteroide = pygame.image.load('images/asteroid.png')
imagemRaio = pygame.image.load('images/missil.png')
imagemFundo = pygame.image.load('images/space.jpg')
 
LARGURAJANELA = screen_width # largura da janela
ALTURAJANELA = screen_height # altura da janela
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
font_size = 48
fonte = pygame.font.Font(None, font_size)

# Configurando o som.
somFinal = pygame.mixer.Sound('sound/Raycast_lose.wav')
somRecorde = pygame.mixer.Sound('sound/Raycast_start.wav')
somTiro = pygame.mixer.Sound('sound/missile.wav')
somTiro.set_volume(0.3)
somFinal.set_volume(0.3)
pygame.mixer.music.load('sound/space.mp3')