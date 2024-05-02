import pygame, random
from .Display import Display
from .Events import Events
from .Player import Player
from .Rock import Rock
from .Mob import Mob
from .Surfaces import Surfaces
from .Sounds import Sounds

class JogoNave():
    '''Jogo 2D shooter '''
    def __init__(self, fps:int, fullscreen:bool, name:str):
        # get display with fps and fullscreen
        self.display = Display(fps, fullscreen, name)        
        self.events = Events()
        self.surfaces = Surfaces(self.display.disp_size)
        self.sounds = Sounds()
        
        #player initial position
        pos = self.display.disp_size
        self.player_x = pos[0]*0.5
        self.player_y = pos[1]*0.7     
                                
        # para criar inimigos/outros objetos
        self.TAMMINIMO = 30      # tamanho mínimo do rock
        self.TAMMAXIMO = 60      # tamanho máximo do rock
        self.VELMINIMA = 3       # velocidade mínima do rock
        self.VELMAXIMA = 10       # velocidade máxima do rock
        self.ITERACOES = 60      # número de iterações antes de criar um novo rock  
                                       
        self.clock = pygame.time.Clock()
        self.run()
          
    def run(self):
        # Tela de inicio.self.disp_size
        self.menu_first()
                
        self.high_score = 0                     # recorde
        while True:                             # laço externo do game over
            # Configurando o começo do jogo.
            self.rocks = pygame.sprite.Group()  # lista com os rocks   
            self.mobs = pygame.sprite.Group()  # lista com as naves inimigas           
            self.running = True                 # indica se o loop do jogo deve continuar
            self.score = 0                      # pontuação
            self.counter = 0                    # contador de iterações
            self.counter2 = 0                    # contador de iterações
                   
            pygame.mixer.music.play(-1, 0.0)    # colocando a música de fundo
            
            #create player
            self.player = Player(self.surfaces, self.sounds,
                                 self.player_x, self.player_y, self.display)
            pygame.mouse.set_pos(self.player_x,self.player_y)     # inicializando mouse posicao player
                                        
            #repetição principal
            self.session_max_score = self.main_loop()        # inicia novo jogo
                                    
            # Parando o jogo e mostrando a tela final.
            self.menu_last()
    
    
    def main_loop(self):
        ''' new game'''
        self.sounds.somStart.play()
        while self.running:
            #self.score += 1        
            self.counter += 1
            self.counter2 += 1
            
            # preenchendo o fundo de janela com a sua imagem
            self.display.draw_background(self.score, self.high_score, int(self.clock.get_fps()))
            
            #verifica eventos e atualiza em memória       
            self.running = self.events.checker(self.player)
                        
            #criar inimigos   
            self.counter = self.set_enemies(self.rocks, self.counter)
            self.counter2 = self.set_mobs(self.mobs, self.counter2)
            #atualiza inimigos                        
            self.rocks.update(self.display)
            self.mobs.update(self.display)
                        
            #atualiza jogador   
            self.running, self.score = self.player.update(self.rocks, self.mobs, self.score)
            
            # verifica fim de jogo com recorde
            if not self.running and self.score > self.high_score:
                self.high_score = self.score        
                #self.sounds.somRecorde.play()
            
            # mostrando na tela tudo o que foi desenhado
            pygame.display.update()        
            # limitando a 60 quadros por segundo
            self.clock.tick(self.display.fps)
        return self.high_score   
    
    
    def set_enemies(self, rocks, counter:int):    
        # Adicionando rocks quando indicado.        
        if counter >= self.ITERACOES:
            counter = 0
            tamAsteroide = random.randint(self.TAMMINIMO, self.TAMMAXIMO)
            pos = self.display.disp_size
            posX = random.randint(0, pos[0] - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(-1,1)
            vel_y = random.randint(self.VELMINIMA, self.VELMAXIMA)
            
            size = (tamAsteroide, tamAsteroide)
            vel = (vel_x, vel_y)                #velocity/speed
            
            rock = Rock(self.surfaces, self.sounds, posX, posY, size, vel)        #create enemy  
            #rock = Enemy(self.surfaces.surf_exploded, posX, posY, size, vel)      
            rocks.add(rock)
        return counter
    
    def set_mobs(self, mobs, counter:int):    
        # Adicionando mobs quando indicado.        
        if counter >= self.ITERACOES:
            counter = 0
            tamAsteroide = random.randint(self.TAMMINIMO, self.TAMMAXIMO)
            pos = self.display.disp_size
            posX = random.randint(0, pos[0] - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(-1,1)
            vel_y = random.randint(self.VELMINIMA, self.VELMAXIMA)
            size = (self.TAMMAXIMO, self.TAMMAXIMO)
            vel = (vel_x, vel_y)                #velocity/speed
            
            mob = Mob(self.surfaces, self.sounds, posX, posY, size, vel, self.display)        #create enemy 
            mobs.add(mob)
        return counter
    
    
    def menu_first(self):
        pos = self.display.disp_size
        offset = self.display.font_size
        self.display.print('Asteroides Troianos', (pos[0]/2), (pos[1]/2)-offset, 'center')
        self.display.print('Pressione F1 para começar.', (pos[0]/2),(pos[1]/2)+offset, 'center')
        self.display.print('Pressione ESC para sair.', (pos[0]/2),(pos[1]/2)+offset*2, 'center')    
        pygame.display.update()
        self.events.aguardarEntrada()
    
    
    def menu_last(self):
        pygame.mixer.music.stop()
        self.sounds.somFinal.play() 
        pos = self.display.disp_size
        offset = self.display.font_size
        self.display.print('GAME OVER', (pos[0]/2),(pos[1]/2)-offset, 'center')
        self.display.print('Pressione F1 para começar.', (pos[0]/2), (pos[1]/2)+offset, 'center')
        self.display.print('Pressione ESC para sair.', (pos[0]/2), (pos[1]/2)+offset*2, 'center')               
        
        pygame.display.update()
        # Aguardando entrada por teclado para reiniciar o jogo ou sair.
        self.events.aguardarEntrada()
        self.sounds.somFinal.stop()
        
        #limpando os grupos
        #self.player.empty()
        self.rocks.empty()
        self.mobs.empty()
        
        