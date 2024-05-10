import pygame
import tkinter as tk

class Settings:        
    def __init__(self):
        '''Load several global vars'''
        name:str = 'Asteroids'
        self.fullscreen:bool = True
        self.fps:int = 60

        pygame.init()       # inicializando pygame
        pygame.display.init()        
        self.clock = pygame.time.Clock() 

        # Ocultando o cursor 
        pygame.mouse.set_visible(False)             
            
        #set window   
        root = tk.Tk()
        self.disp_size = (root.winfo_screenwidth(), root.winfo_screenheight())
        self.window = pygame.display.set_mode(self.disp_size)
        pygame.display.set_caption(name)

        if self.fullscreen: pygame.display.toggle_fullscreen()
        else: pass

        # Configurando a fonte.        
        self.font_size = 48 
        self.font = pygame.font.Font(None, self.font_size)

        # game globals
        self.score: int = 0
        self.hi_score: int = 0
        self.running: bool = False

        # moving background
        self.scroll = 0
        self.tiles = 2 #math.ceil    screen_height / bg_height) +1    #buffer +1

        #text in screen
        self.COLOR_TEXT = (255,255,255)   # white

        # para criar inimigos/outros objetos
        self.TAMMINIMO = 30      # tamanho mínimo do rock
        self.TAMMAXIMO = 60      # tamanho máximo do rock
        self.VELMINIMA = 3       # velocidade mínima do rock
        self.VELMAXIMA = 10       # velocidade máxima do rock
        self.ITERACOES = 60      # número de iterações antes de criar um novo rock  
        
    def load_resources(self):
        '''load images and sounds'''                       
        self.load_images()
        self.load_sounds() 

    def load_images(self):        
        #carregando e redimensionando a imagem de fundo.
        imagemFundo = pygame.image.load('images/space0.png').convert()
        self.imagemFundo = pygame.transform.scale(imagemFundo, self.disp_size)
        
        # Carregando as imagens.       
        surf_ship = pygame.image.load('images/ship.png')        
        
        # asteroids
        exp_seq = pygame.image.load('sprites/asteroids-arcade.png').convert_alpha()        
        surf_asteroids = Settings.get_sub_surfs(exp_seq, 66,194,(58,61),(65,0),3)
                
        surf_fire = exp_seq.subsurface((198,72),(4,8)) 
        surf_fire = pygame.transform.rotozoom(surf_fire,0,3)
            
        surf_rocket = exp_seq.subsurface((173,48),(6,12)) 
        surf_rocket = pygame.transform.rotozoom(surf_rocket,0,3)
        
        surf_jets = Settings.get_sub_surfs(exp_seq, 71,15,(18,17),(32,0),4)
        
        sub1 = exp_seq.subsurface((200,5),(16,24)) 
        sub1 = pygame.transform.rotozoom(sub1,180,2)       
        sub2 = exp_seq.subsurface((8,197), (48, 52))
        sub3 = exp_seq.subsurface((207,144),(36,35))
        sub4 = exp_seq.subsurface((151,151), (17,18))
        sub5 = exp_seq.subsurface((92,156),(8,8))        
        #surf_enemy1 = [sub1,sub2,sub3,sub4,sub5]
        surf_enemy1 = [sub1]  
        
        self.add_surf(surf_enemy1, sub2, 5)
        self.add_surf(surf_enemy1, sub3, 5)
        self.add_surf(surf_enemy1, sub4, 5)
        self.add_surf(surf_enemy1, sub5, 5)          
        
        list = [surf_asteroids[0]]
        self.add_surf(list, sub2, 5)
        self.add_surf(list, surf_asteroids[1], 7)
        self.add_surf(list, surf_asteroids[2], 10)
        surf_asteroids = list  
        
        self.surf_player = {'ship':[surf_ship], 'jets':surf_jets, 'rocket':[surf_rocket]}
        self.surf_enemy = {'asteroid':surf_asteroids, 'enemy1':surf_enemy1, 'rocket1':[surf_fire]}
            
    
    def add_surf(self, list, surf, times):
        for i in range(times):
            list.append(surf)
    
    def get_sub_surfs(surf, top, left, width_height, offset_next, times):
        list = []
        for i in range(times):
            #print(top, left, width_height)
            list.append(surf.subsurface((top,left), width_height))
            top = top + offset_next[0]
            left = left + offset_next[1]
        return list
        
    def load_sounds(self):        
        # Configurando o som.
        self.sound_over = pygame.mixer.Sound('sound/Raycast_lose.wav')
        self.sound_over.set_volume(0.3)
        
        self.sound_start = pygame.mixer.Sound('sound/Raycast_start.wav')
        
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
        
        self.sound_player = {'ship':[somExplosao_player], 'jets':[], 'rocket':[somTiro]}
        self.sound_enemy = {'asteroid':[somExplosao], 'enemy1':[somExplosao_nave], 'rocket1':[somFire]}
   
   
   
#group all up
settings = Settings()