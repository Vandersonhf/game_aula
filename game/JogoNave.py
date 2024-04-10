import pygame, random
from .GameDisplay import GameDisplay
from .Images import Images
from .Sounds import Sounds
from .Events import Events
from .Player import Player
from .Enemy import Enemy

class JogoNave():
    '''Jogo 2D shooter '''
    def __init__(self, fps, fullscreen, name):
        # get display with fps and fullscreen
        self.display = GameDisplay(fps, fullscreen, name)
        self.images = Images(self.display.disp_size)
        self.sounds = Sounds()
        self.events = Events()        
                
        self.clock = pygame.time.Clock()
        
        #create player
        self.player = Player(self.display.disp_size, self.images.imagemNave,
                             self.images.LARGURANAVE, self.images.ALTURANAVE)
        
        # para criar inimigos/outros objetos
        self.TAMMINIMO = 10      # tamanho mínimo do rock
        self.TAMMAXIMO = 40      # tamanho máximo do rock
        self.VELMINIMA = 1       # velocidade mínima do rock
        self.VELMAXIMA = 8       # velocidade máxima do rock
        self.ITERACOES = 60      # número de iterações antes de criar um novo rock        
        
          
    def run(self):
        # Tela de inicio.self.disp_size
        self.menu_first()
        
        self.high_score = 0         #recorde
        while True:                 # laço externo do game over
            # Configurando o começo do jogo.
            self.rocks = []         # lista com os rocks
            self.lasers = []         # lista com os lasers
            self.running = True     # indica se o loop do jogo deve continuar
            self.score = 0          # pontuação
            self.counter = 0        # contador de iterações
            
            pygame.mixer.music.play(-1, 0.0) # colocando a música de fundo
                  
            #repetição principal
            self.main_loop()        # inicia novo jogo
            
            # Parando o jogo e mostrando a tela final.
            self.menu_last()
    
    
    def main_loop(self):
        ''' new game'''
        while self.running:
            self.score += 1        
            self.counter += 1
            
            # preenchendo o fundo de janela com a sua imagem
            self.display.draw_background(self.images.imagemFundo, self.score, self.high_score)
            
            #verifica eventos e atualiza em memória       
            self.running = self.events.checker(self.player,self.lasers,self.images.imagemRaio,
                                               self.sounds.somTiro, 
                                               self.images.LARGURARAIO, self.images.ALTURARAIO,)
                        
            #criar inimigos                    
            self.counter = self.set_enemies(self.rocks, self.counter)
            #atualiza inimigos
            self.update_enemies(self.rocks, self.lasers) 
            
            #atualiza jogador   
            self.running = self.player.update(self.display.window, self.rocks, self.lasers)
            if not self.running and self.score > self.high_score:
                self.high_score = self.score        
                self.sounds.somRecorde.play()
            
            # mostrando na tela tudo o que foi desenhado
            pygame.display.update()        
            # limitando a 60 quadros por segundo
            self.clock.tick(self.display.fps)
        return self.high_score   
    
    
    def update_enemies(self, rocks, lasers):
        '''atualizando asteroides e laser/missil'''
        if len(rocks) > 0:
            self.rocks = rocks[0].update(self.display.window,
                                         self.display.disp_size, self.rocks)
        if len(lasers) > 0:
            self.lasers = lasers[0].update(self.display.window, self.lasers)
            
    
    def set_enemies(self, rocks, counter):    
        # Adicionando rocks quando indicado.        
        if counter >= self.ITERACOES:
            counter = 0
            tamAsteroide = random.randint(self.TAMMINIMO, self.TAMMAXIMO)
            posX = random.randint(0, self.display.disp_size[0] - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(-1,1)
            vel_y = random.randint(self.VELMINIMA, self.VELMAXIMA)
            
            rect = pygame.Rect(posX, posY, tamAsteroide, tamAsteroide)
            img = pygame.transform.scale(self.images.imagemAsteroide, (tamAsteroide, tamAsteroide))
            vel = (vel_x, vel_y)                #velocity/speed
            
            rock = Enemy(rect, img, vel)        #create enemy        
            rocks.append(rock)
        return counter
    
    
    def menu_first(self):
        self.display.print('Asteroides Troianos', (self.display.disp_size[0]/2),
                    (self.display.disp_size[1]/2)-self.display.font_size, 'center')
        self.display.print('Pressione F1 para começar.', (self.display.disp_size[0]/2),
                    (self.display.disp_size[1]/2)+self.display.font_size, 'center')
        self.display.print('Pressione ESC para sair.', (self.display.disp_size[0]/2),
                    (self.display.disp_size[1]/2)+self.display.font_size*2, 'center')    
        pygame.display.update()
        self.events.aguardarEntrada()
    
    
    def menu_last(self):
        pygame.mixer.music.stop()
        self.sounds.somFinal.play() 
        self.display.print('GAME OVER', (self.display.disp_size[0]/2),
                (self.display.disp_size[1]/2)-self.display.font_size, 'center')
        self.display.print('Pressione F1 para começar.', (self.display.disp_size[0]/2),
                (self.display.disp_size[1]/2)+self.display.font_size, 'center')
        self.display.print('Pressione ESC para sair.', (self.display.disp_size[0]/2),
                (self.display.disp_size[1]/2)+self.display.font_size*2, 'center')               
        
        pygame.display.update()
        # Aguardando entrada por teclado para reiniciar o jogo ou sair.
        self.events.aguardarEntrada()
        self.sounds.somFinal.stop()