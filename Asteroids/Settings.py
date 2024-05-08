import pygame
import tkinter as tk

# game globals
score: int = 0
hi_score: int = 0
running: bool = False

# moving background
scroll = 0
tiles = 2 #math.ceil    screen_height / bg_height) +1    #buffer +1

#text in screen
COLOR_TEXT = (255,255,255)   # white

# para criar inimigos/outros objetos
TAMMINIMO = 30      # tamanho mínimo do rock
TAMMAXIMO = 60      # tamanho máximo do rock
VELMINIMA = 3       # velocidade mínima do rock
VELMAXIMA = 10       # velocidade máxima do rock
ITERACOES = 60      # número de iterações antes de criar um novo rock  

global sound_player, sound_enemy
global sound_start, sound_over
global clock, fps, fullscreen, window, font, font_size
global imagemFundo, surf_player, surf_enemy
global disp_size

def load_resources (NAME, FULLSCREEN, FPS):
    '''Load several global vars'''
    global clock, fps, fullscreen, disp_size, window, font, font_size
    
    pygame.init()       # inicializando pygame
    pygame.display.init()
    
    clock = pygame.time.Clock()
    fps = FPS
    fullscreen = FULLSCREEN        
       
    root = tk.Tk()
    disp_size = (root.winfo_screenwidth(), root.winfo_screenheight())
    window = pygame.display.set_mode(disp_size)
    pygame.display.set_caption(NAME)
    
    if fullscreen: pygame.display.toggle_fullscreen()
    else: pass
    
    # Ocultando o cursor 
    pygame.mouse.set_visible(False)
    
    # Configurando a fonte.        
    font_size = 48    
    font = pygame.font.Font(None, font_size)
    
    load_images()
    load_sounds()
    
    

def load_images():
    global imagemFundo, surf_player, surf_enemy
    
    #carregando e redimensionando a imagem de fundo.
    imagemFundo = pygame.image.load('images/space0.png').convert()
    imagemFundo = pygame.transform.scale(imagemFundo, disp_size)
    
    # Carregando as imagens.       
    surf_ship = pygame.image.load('images/ship.png')
    
    # asteroids
    exp_seq = pygame.image.load('sprites/asteroids-arcade.png').convert_alpha()        
    surf_asteroids = get_sub_surfs(exp_seq, 66,194,(58,61),(65,0),3)
    
    surf_fire = exp_seq.subsurface((198,72),(4,8)) 
    surf_fire = pygame.transform.rotozoom(surf_fire,0,3)
        
    surf_rocket = exp_seq.subsurface((173,48),(6,12)) 
    surf_rocket = pygame.transform.rotozoom(surf_rocket,0,3)
    
    surf_jets = get_sub_surfs(exp_seq, 71,15,(18,17),(32,0),4)
    
    sub1 = exp_seq.subsurface((200,5),(16,24)) 
    sub1 = pygame.transform.rotozoom(sub1,180,2)       
    sub2 = exp_seq.subsurface((8,197), (48, 52))
    sub3 = exp_seq.subsurface((207,144),(36,35))
    sub4 = exp_seq.subsurface((151,151), (17,18))
    sub5 = exp_seq.subsurface((92,156),(8,8))        
    surf_enemy1 = [sub1,sub2,sub3,sub4,sub5]
    
    surf_asteroids.insert(1,sub2)
    
    surf_player = {'ship':[surf_ship], 'jets':surf_jets, 'rocket':[surf_rocket]}
    surf_enemy = {'asteroid':surf_asteroids, 'enemy1':surf_enemy1, 'rocket1':[surf_fire]}
   
    
   
def get_sub_surfs(surf, top, left, width_height, offset_next, times):
    list = []
    for i in range(times):
        #print(top, left, width_height)
        list.append(surf.subsurface((top,left), width_height))
        top = top + offset_next[0]
        left = left + offset_next[1]
    return list
    

def load_sounds():
    global sound_player, sound_enemy
    global sound_start, sound_over
    
    # Configurando o som.
    sound_over = pygame.mixer.Sound('sound/Raycast_lose.wav')
    sound_over.set_volume(0.3)
    
    sound_start = pygame.mixer.Sound('sound/Raycast_start.wav')
    
    somTiro = pygame.mixer.Sound('sound/laser1.mp3')
    somTiro.set_volume(0.2)
    
    pygame.mixer.music.load('sound/space.mp3')
    
    somExplosao = pygame.mixer.Sound('sound/explode2.mp3')
    somExplosao.set_volume(0.6)
    
    somExplosao_nave = pygame.mixer.Sound('sound/explode0.mp3')
    somExplosao_nave.set_volume(0.6)
    
    somExplosao_player = pygame.mixer.Sound('sound/explode1.mp3')
    somExplosao_player.set_volume(0.6)
    
    somFire = pygame.mixer.Sound('sound/fire0.mp3')
    somFire.set_volume(0.2)
    
    sound_player = {'ship':[somExplosao_player], 'jets':[], 'rocket':[somTiro]}
    sound_enemy = {'asteroid':[somExplosao], 'enemy1':[somExplosao_nave], 'rocket1':[somFire]}
   