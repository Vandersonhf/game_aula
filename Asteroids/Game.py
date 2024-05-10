from .Player import Player
from .Enemy import Asteroid, Mob
from .Settings import settings
import pygame
import random

class Game: 
    def __init__(self):
        settings.load_resources()
        
    def run(self):        
        self.menu() 
            
    def menu(self):        
        pos = settings.disp_size
        offset = settings.font_size
        self.print_text('Asteroides Troianos', (pos[0]/2), (pos[1]/2)-offset, 'center')
        self.print_text('Pressione F1 para começar.', (pos[0]/2),(pos[1]/2)+offset, 'center')
        self.print_text('Pressione ESC para sair.', (pos[0]/2),(pos[1]/2)+offset*2, 'center')    
        pygame.display.update()
        self.__wait_input__()
        
        self.new_game()    
    
    def new_game (self):
        while True:                             # laço externo do game over
            # Configurando o começo do jogo.
            self.asteroids = pygame.sprite.Group()  # lista com os asteroids   
            self.mobs = pygame.sprite.Group()  # lista com as naves inimigas           
            settings.running = True                    # indica se o loop do jogo deve continuar
            settings.score = 0                         # pontuação
            self.counter = 0                    # contador de iterações
            self.counter2 = 0                    # contador de iterações
                   
            pygame.mixer.music.play(-1, 0.0)    # colocando a música de fundo
            
            #create player           
            self.player = Player()
            pygame.mouse.set_pos(self.player.pos[0],self.player.pos[1])     # inicializando mouse posicao player
                                        
            #repetição principal
            self.main_loop()        # inicia novo jogo
                                    
            # Parando o jogo e mostrando a tela final.
            self.__menu_last__()
        
    def main_loop (self):
        ''' new game'''
        settings.sound_start.play()
        while settings.running:                  
            self.counter += 1
            self.counter2 += 1
            
            # preenchendo o fundo de janela com a sua imagem
            self.draw_background()
            
            #verifica eventos e atualiza em memória       
            settings.running = self.check_events()
                        
            #criar inimigos   
            self.counter = self.populate_asteroid(self.counter)            
            self.counter2 = self.populate_mobs(self.counter2)
            #atualiza inimigos                        
            self.asteroids.update()
            self.mobs.update()
                        
            #atualiza jogador   
            self.player.update()
            settings.running = self.check_collision()
            
            # verifica fim de jogo com recorde
            if not settings.running and settings.score > settings.hi_score:
                settings.hi_score = settings.score   
            
            # mostrando na tela tudo o que foi desenhado
            pygame.display.update()    
                
            # limitando a 60 quadros por segundo
            settings.clock.tick(settings.fps)
       
    
    def check_events(self):
        #print("Tratando...")
        for evento in pygame.event.get():
            # Se for um evento QUIT
            if evento.type == pygame.QUIT:
                self.exit()  
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.exit()   
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:                    
                    self.player.teclas['esquerda'] = True
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    self.player.teclas['direita'] = True
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    self.player.teclas['cima'] = True
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    self.player.teclas['baixo'] = True
                if evento.key == pygame.K_SPACE:                                           
                    self.player.new_rocket()
                            
            # quando uma tecla é solta
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    self.player.teclas['esquerda'] = False
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    self.player.teclas['direita'] = False
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    self.player.teclas['cima'] = False
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    self.player.teclas['baixo'] = False
            
            # mouse
            if evento.type == pygame.MOUSEMOTION:
                # Se o mouse se move, movimenta jogador para onde o cursor está.
                dx = self.player.col_rect.centerx
                dy = self.player.col_rect.centery
                #pygame.mouse.set_pos(dx,dy)
                self.player.col_rect.move_ip(evento.pos[0] - dx, evento.pos[1] - dy)                
                for comp in self.player.components:
                    comp.col_rect.move_ip(evento.pos[0] - dx, evento.pos[1] - dy)
                                                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                self.player.new_rocket()                         
        return True
    
    
    def check_collision (self):        
        # Checando se jogador ou algum rocket colidiu com algum rock.
        for rock in self.asteroids:
            jogadorColidiu = False
            if not rock.dead:
                if self.player.col_rect.colliderect(rock.col_rect):
                    offset = (rock.col_rect.x - self.player.col_rect.x, rock.col_rect.y - self.player.col_rect.y)
                    jogadorColidiu = self.player.mask.overlap(rock.mask, offset)
                if jogadorColidiu:  
                    settings.sound_player['ship'][0].play()          
                    return False 
            for rocket in self.player.rockets:
                if not rock.dead:
                    rocketColidiu = rocket.col_rect.colliderect(rock.col_rect)
                    if rocketColidiu:
                        rock.explode()                                   
                        self.player.rockets.remove(rocket)
                        settings.score = settings.score + 50
        # Checando se jogador ou algum rocket colidiu com algum mob.
        for mob in self.mobs:
            jogadorColidiu = False
            if not mob.dead:
                if self.player.col_rect.colliderect(mob.col_rect):
                    offset = (mob.col_rect.x - self.player.col_rect.x, mob.col_rect.y - self.player.col_rect.y)
                    jogadorColidiu = self.player.mask.overlap(mob.mask, offset)
                if jogadorColidiu:  
                    settings.sound_player['ship'][0].play()           
                    return False
            for rocket in self.player.rockets:
                if not mob.dead:
                    rocketColidiu = rocket.col_rect.colliderect(mob.col_rect)
                    if rocketColidiu:
                        mob.explode()                                   
                        self.player.rockets.remove(rocket)
                        settings.score = settings.score + 100
            for fire in mob.rockets:
                if self.player.col_rect.colliderect(fire.col_rect):
                    offset = (fire.col_rect.x - self.player.col_rect.x, fire.col_rect.y - self.player.col_rect.y)
                    jogadorColidiu = self.player.mask.overlap(fire.mask, offset)
                if jogadorColidiu:  
                    settings.sound_player['ship'][0].play()        
                    return False  
        return True
    
    def populate_asteroid (self, counter):
        # Adicionando asteroids quando indicado.        
        if counter >= settings.ITERACOES:
            counter = 0
            tamAsteroide = random.randint(settings.TAMMINIMO, settings.TAMMAXIMO)
            pos = settings.disp_size
            posX = random.randint(0, pos[0] - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(-1,1)
            vel_y = random.randint(settings.VELMINIMA, settings.VELMAXIMA)
            
            size = [tamAsteroide, tamAsteroide]
            vel = [vel_x, vel_y]                #velocity/speed
            
            rock = Asteroid([posX, posY], size, vel)        #create enemy                   
            self.asteroids.add(rock)
        return counter
    
    def populate_mobs (self, counter):
        # Adicionando mobs quando indicado.        
        if counter >= settings.ITERACOES:
            counter = 0
            tamAsteroide = random.randint(settings.TAMMINIMO, settings.TAMMAXIMO)
            pos = settings.disp_size
            posX = random.randint(0, pos[0] - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(-1,1)
            vel_y = random.randint(settings.VELMINIMA, settings.VELMAXIMA)
            size = [settings.TAMMAXIMO, settings.TAMMAXIMO]
            vel = [vel_x, vel_y]                #velocity/speed
            
            mob = Mob([posX, posY], size, vel)        #create enemy 
            self.mobs.add(mob)
        return counter
    
    def print_text(self, texto, x, y, position):
        ''' Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.'''
        objTexto = settings.font.render(texto, True, settings.COLOR_TEXT)
        rectTexto = objTexto.get_rect()
        if position == 'center':
            rectTexto.center = (x, y)
        elif position == 'topLeft':
            rectTexto.topleft = (x, y)
        settings.window.blit(objTexto, rectTexto)


    def draw_background(self):
        ''' Preenchendo o fundo da janela com a imagem correspondente.'''      
        # movendo o fundo
        for i in range(0, settings.tiles):
            pos_y = i * settings.imagemFundo.get_height() + settings.scroll
            settings.window.blit(settings.imagemFundo, (0,-pos_y))
        
        # update scroll
        settings.scroll -= 1
        if abs(settings.scroll)  > settings.imagemFundo.get_height(): 
            settings.scroll = 0
        
        # Colocando as pontuações.
        self.print_text('Pontuação: ' + str(settings.score), 10, 0, 'topLeft')
        self.print_text('Recorde: ' + str(settings.hi_score), 10, 40, 'topLeft')
        self.print_text('FPS: ' + str(int(settings.clock.get_fps())), 10, 80, 'topLeft')
    
    
    def __wait_input__(self):
         # Aguarda entrada por teclado ou clique do mouse no “x” da janela.
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.exit()
                    if evento.key == pygame.K_F1:
                        return
    
       
    def __menu_last__(self):
        pygame.mixer.music.stop()
        settings.sound_over.play() 
        pos = settings.disp_size
        offset = settings.font_size
        self.print_text('GAME OVER', (pos[0]/2),(pos[1]/2)-offset, 'center')
        self.print_text('Pressione F1 para começar.', (pos[0]/2), (pos[1]/2)+offset, 'center')
        self.print_text('Pressione ESC para sair.', (pos[0]/2), (pos[1]/2)+offset*2, 'center')               
        
        pygame.display.update()
        # Aguardando entrada por teclado para reiniciar o jogo ou sair.
        self.__wait_input__()
        settings.sound_over.stop()
        
        #limpando os grupos
        self.asteroids.empty()
        self.mobs.empty()
    
    def load_game (self):
        pass
    
    def save_game (self):
        pass
    
    def game_over (self):
        pass
        
    def open_editor(self):
        pass
    
    def exit(self):
        # Termina o programa.
        pygame.quit()
        exit()
    