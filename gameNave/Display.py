import pygame
import tkinter as tk

class Display():
    def __init__(self, FPS:int, Fullscreen:bool, nome:str):
        self.fps = FPS
        self.fullscreen = Fullscreen
        self.nome = nome
        # screen info
        root = tk.Tk()
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        if Fullscreen:
            self.disp_size = (self.screen_width, self.screen_height)
        else:
            self.disp_size = (1280, 720)
        # disp_size = (1920, 1080) # disp_size = (1280, 720)  # disp_size = (720, 400)  # disp_size = (640, 360)
        
        self._setup_display()        
    
    def _setup_display(self):
        pygame.init()       # inicializando pygame
        pygame.display.init()
                
        self.window = pygame.display.set_mode(self.disp_size)
        pygame.display.set_caption(self.nome)
        
        if self.fullscreen:
            self.toggle_fullscreen()
            
        self.imagemFundo = pygame.image.load('images/space.jpg').convert_alpha()        
        #redimensionando a imagem de fundo.
        #self.imagemFundo = pygame.transform.scale(self.imagemFundo, self.disp_size)
        
        # Configurando a fonte.        
        self.font_size = 48
        self.fonte = pygame.font.Font(None, self.font_size)
        self.CORTEXTO = (255, 255, 255) # cor do texto (branca)
        
        # Ocultando o cursor 
        pygame.mouse.set_visible(False)
      
      
    def toggle_fullscreen(self):
        ''' toggle between fullscreen and windowed mode.'''
        pygame.display.toggle_fullscreen()


    def print(self, texto, x, y, position):
        ''' Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.'''
        objTexto = self.fonte.render(texto, True, self.CORTEXTO)
        rectTexto = objTexto.get_rect()
        if position == 'center':
            rectTexto.center = (x, y)
        elif position == 'topLeft':
            rectTexto.topleft = (x, y)
        self.window.blit(objTexto, rectTexto)


    def draw_background(self, pontuacao, recorde):
        ''' Preenchendo o fundo da janela com a imagem correspondente.'''
        self.window.blit(self.imagemFundo, (0,0))
        # Colocando as pontuações.
        self.print('Pontuação: ' + str(pontuacao), 10, 0, 'topLeft')
        self.print('Recorde: ' + str(recorde), 10, 40, 'topLeft')
    