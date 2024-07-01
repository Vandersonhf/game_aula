import pygame
from customtkinter import *
#from screeninfo import get_monitors
import os

class Settings:        
    def __init__(self):
        '''Load several global vars'''
        name:str = 'Asteroids'
        self.fullscreen:bool = False
        self.fps:int = 60

        #set window           
        self.menu = CTk()  
        #self.menu.resizable(width=False, height=False)   
        self.screen = (self.menu.winfo_screenwidth(), self.menu.winfo_screenheight())        
        self.disp_size = (int(self.screen[0]/2), int(self.screen[1]/2))
        
        # Get the bounds of the users monitors, and select the first one
        #monitors = get_monitors() # Get the resolution of all of the users monitors
        #screen_width = monitors[0].width # Get width of first monitor found
        #screen_height = monitors[0].height # Get height of first monitor found

        # Set the x and y coordinates of the pygame window in relation to the monitor's resolution 
        # (I wanted my pygame window to be located in the bottom-right of the monitor)
        pos_x = self.screen[0] - self.disp_size[0] # Calculate the x-location
        pos_y = self.screen[1] - self.disp_size[1] - 50 # Calculate the y-location
        os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (pos_x,pos_y) # Set pygame window location

        
        #client frame
        self.hosts = ['192.168.0.107']
        self.client = '192.168.0.107'
        self.frame = None
        self.frame_list = []
        self.max_buffer = 30
        self.frame_segment = 1024 #262144   #131072
        self.host = None
        self.port = None
        self.TCP_buffer = None

        pygame.init()       # inicializando pygame
        pygame.display.init()        
        self.clock = pygame.time.Clock() 

        # Ocultando o cursor 
        pygame.mouse.set_visible(False)             
            
        #set window           
        self.window = pygame.display.set_mode(self.disp_size)
        pygame.display.set_caption(name)

        if self.fullscreen: pygame.display.toggle_fullscreen()
        
        # Configurando a fonte.        
        self.font_size = 48 
        self.font = pygame.font.Font(None, self.font_size)

        # online globals
        self.multiplayer = False
        self.server = None
        self.port = 4040
        self.port2 = 4041
        self.open_connection = False
        self.open_connection2 = False
        self.last_message = None
        self.last_obj = None      
        self.buffer_message = []          
        self.ID = 1
        
        # game globals
        self.score: int = 0
        self.score2: int = 0
        self.hi_score: int = 0
        self.life = 3
        self.life2 = 3
        self.ups = 1
        self.ups2 = 1
        self.running: bool = False
        self.level_points = 2000
        self.time = 0
        self.time_level = 2_000
        self.luck = 10
        self.name = ''
        self.pwd = ''

        # moving background
        self.scroll = 0
        self.tiles = 2 #math.ceil    screen_height / bg_height) +1    #buffer +1

        #text in screen
        self.COLOR_TEXT = (255,255,255)   # white

        # para criar inimigos/outros objetos
        self.TAMMINIMO = 40      # tamanho mínimo do rock
        self.TAMMAXIMO = 70      # tamanho máximo do rock
        self.VELMINIMA = 2       # velocidade mínima do rock
        self.VELMAXIMA = 3       # velocidade máxima do rock
        self.ITERACOES = 200      # número de iterações antes de criar um novo rock  
        
        #hacks
        self.hack = {'easy':'False', 'god':'False'}        
        
        
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
        surf_ship2 = pygame.image.load('images/ship2.png')
        surf_ship3 = pygame.image.load('images/ship3.png')
        surf_ship = [surf_ship, surf_ship3, surf_ship2]        
        
        # asteroids sprite map
        original_map = pygame.image.load('sprites/asteroids-arcade.png').convert_alpha()        
        surf_asteroids = Settings.get_sub_surfs(original_map, 66,194,(58,61),(65,0),3)
        
        # enemy rocket        
        surf_fire = original_map.subsurface((198,72),(4,8)) 
        surf_fire = pygame.transform.rotozoom(surf_fire,0,3)
        surf_fire = [surf_fire]
           
        #player rocket    
        surf_rocket = original_map.subsurface((173,48),(6,12)) 
        surf_rocket = pygame.transform.rotozoom(surf_rocket,0,3)
        surf_rocket = [surf_rocket]
        
        #player jet
        surf_jets = Settings.get_sub_surfs(original_map, 71,15,(18,17),(32,0),4)
        
        #player extra ups
        surf_extra = original_map.subsurface((40,33), (16,28))
        surf_extra = pygame.transform.rotozoom(surf_extra,0,0.5)
        surf_extra = [surf_extra] 
        
        # explosion
        sub2 = original_map.subsurface((8,197),(48, 52))
        sub3 = original_map.subsurface((207,144),(36,35))
        sub4 = original_map.subsurface((151,151), (17,18))
        sub5 = original_map.subsurface((92,156),(8,8))
        exp_seq = [sub2, sub3, sub4, sub5]
                
        #enemy 1
        surf_enemy1 = self.enemy_seq(original_map,(200,5),(16,24),180,2, exp_seq, 5)
        
        #asteroids explosion sequence        
        ast_seq = [sub2, surf_asteroids[1], surf_asteroids[2]]      
        surf_asteroids = self.enemy_seq(original_map,(66,194),(58,61),0,2, ast_seq, 15)
       
        #boss
        surf_boss = self.enemy_seq(original_map,(6,68), (48,58),180,1, exp_seq, 5)
        
        # subboss
        surf_sub_boss = self.enemy_seq(original_map,(38,2), (20,28),180,2, exp_seq, 5)
        
        #enemy 2
        surf_enemy2 = self.enemy_seq(original_map,(193,34), (30,24),180,2, exp_seq, 5)
       
        #enemy 3
        surf_enemy3 = self.enemy_seq(original_map,(226, 12), (28,17),180,2, exp_seq, 5)
        
        #enemy 4
        surf_enemy4 = self.enemy_seq(original_map,(232, 38), (16,23),0,2, exp_seq, 5)
        
        #extra maps        
        sprite_map = pygame.image.load('sprites/arcade_sprites_transparent.png').convert_alpha()
        space_map = pygame.image.load('sprites/space_sprites_transparent.png').convert_alpha()
        
        #life images        
        surf_life2 = space_map.subsurface((300, 292), (31,34))
        surf_life1 = space_map.subsurface((217,292), (33,35))        
        surf_life2 = pygame.transform.rotozoom(surf_life2,0,2) 
        surf_life1 = pygame.transform.rotozoom(surf_life1,0,2)        
        surf_lifes = [surf_life1, surf_life2]
        
        #power up levels
        surf_up5 = sprite_map.subsurface((121, 140), (78, 15))
        surf_up4 = sprite_map.subsurface((121, 157), (78, 15))
        surf_up3 = sprite_map.subsurface((121, 175), (78, 15))
        surf_up2 = sprite_map.subsurface((121, 193), (78, 15))
        surf_up1 = sprite_map.subsurface((121, 210), (78, 15))
        surf_up1 = pygame.transform.rotozoom(surf_up1,0,2) 
        surf_up2 = pygame.transform.rotozoom(surf_up2,0,2)
        surf_up3 = pygame.transform.rotozoom(surf_up3,0,2)
        surf_up4 = pygame.transform.rotozoom(surf_up4,0,2)
        surf_up5 = pygame.transform.rotozoom(surf_up5,0,2)
        surf_ups = [surf_up1,surf_up2,surf_up3,surf_up4,surf_up5]
        
        # moreshield        
        surf_shield = space_map.subsurface((598,70), (28,27))
        surf_shield = [surf_shield ]
        
        # power ups        
        surf_pow1 = space_map.subsurface((698, 67), (27, 31))
        surf_pows = [surf_pow1]
        
        #add one more rocket type
        surf_rocket2 = sprite_map.subsurface((512,298), (8, 11))
        surf_rocket.append(surf_rocket2)
        
        self.surf_player = {'ship':surf_ship, 'jets':surf_jets, 'rocket':surf_rocket,
                            'life':surf_lifes, 'ups':surf_ups, 'extra':surf_extra}        
        self.surf_enemy = {'asteroid':surf_asteroids, 'enemy1':surf_enemy1, 'rocket1':surf_fire,
                           'enemy2':surf_enemy2, 'enemy3':surf_enemy3, 'enemy4':surf_enemy4,
                           'subboss':surf_sub_boss, 'boss': surf_boss, 'pows':surf_pows,
                           'shield':surf_shield}
            
    
    def enemy_seq(self, map, pos, size, rotate, scale, seq, times):
        surf = map.subsurface(pos,size)
        surf = pygame.transform.rotozoom(surf,rotate,scale)
        list = [surf]
        for s in seq:
            for i in range(times):
                list.append(s)
        return list        
    
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
        
        self.sound_menu = pygame.mixer.Sound('sound/sinking2.ogg')
        self.sound_menu.set_volume(0.3)
        
        self.sound_pow = pygame.mixer.Sound('sound/Raycast_start.wav')
        self.sound_pow.set_volume(0.5)
        
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
        self.sound_enemy = {'asteroid':[somExplosao], 'enemy1':[somExplosao_nave], 'rocket1':[somFire],
                            'pows':[self.sound_pow]}
   
   
   
#group all up
settings = Settings()