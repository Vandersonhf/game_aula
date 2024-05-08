from .Settings import *
import pygame
from .Player import Player
from .Enemy import Asteroid, Mob
import random

class Game: 
    def __init__(self, name:str = 'Asteroids', fullscreen:bool = True, fps:int = 60):                
        load_resources(name, fullscreen, fps)
        self.menu() 
            
    def menu(self):        
        pos = disp_size
        offset = font_size
        self.print_text('Asteroides Troianos', (pos[0]/2), (pos[1]/2)-offset, 'center')
        self.print_text('Pressione F1 para começar.', (pos[0]/2),(pos[1]/2)+offset, 'center')
        self.print_text('Pressione ESC para sair.', (pos[0]/2),(pos[1]/2)+offset*2, 'center')    
        pygame.display.update()
        self.__wait_input__()
        
        self.new_game()
        
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
        sound_over.play() 
        pos = disp_size
        offset = font_size
        self.print_text('GAME OVER', (pos[0]/2),(pos[1]/2)-offset, 'center')
        self.print_text('Pressione F1 para começar.', (pos[0]/2), (pos[1]/2)+offset, 'center')
        self.print_text('Pressione ESC para sair.', (pos[0]/2), (pos[1]/2)+offset*2, 'center')               
        
        pygame.display.update()
        # Aguardando entrada por teclado para reiniciar o jogo ou sair.
        self.__wait_input__()
        sound_over.stop()
        
        #limpando os grupos
        self.rocks.empty()
        self.mobs.empty()
    
    def new_game (self):
        global player, running, score, hi_score
       
        while True:                             # laço externo do game over
            # Configurando o começo do jogo.
            self.rocks = pygame.sprite.Group()  # lista com os rocks   
            self.mobs = pygame.sprite.Group()  # lista com as naves inimigas           
            running = True                    # indica se o loop do jogo deve continuar
            score = 0                         # pontuação
            self.counter = 0                    # contador de iterações
            self.counter2 = 0                    # contador de iterações
                   
            pygame.mixer.music.play(-1, 0.0)    # colocando a música de fundo
            
            #create player           
            player = Player()
            pygame.mouse.set_pos(player.pos[0],player.pos[1])     # inicializando mouse posicao player
                                        
            #repetição principal
            self.main_loop()        # inicia novo jogo
                                    
            # Parando o jogo e mostrando a tela final.
            self.__menu_last__()
                        
    
    def load_game (self):
        pass
    
    def save_game (self):
        pass
    
    def game_over (self):
        pass
    
    def main_loop (self):
        ''' new game'''
        global high_score
        sound_start.play()
        while self.running:                  
            self.counter += 1
            self.counter2 += 1
            
            # preenchendo o fundo de janela com a sua imagem
            self.draw_background()
            
            #verifica eventos e atualiza em memória       
            running = self.check_events()
                        
            #criar inimigos   
            self.counter = self.populate_asteroid(self.counter)            
            self.counter2 = self.populate_mobs(self.counter2)
            #atualiza inimigos                        
            self.rocks.update()
            self.mobs.update()
                        
            #atualiza jogador   
            player.update()
            running = self.check_collision()
            
            # verifica fim de jogo com recorde
            if not running and score > hi_score:
                hi_score = score   
            
            # mostrando na tela tudo o que foi desenhado
            pygame.display.update()    
                
            # limitando a 60 quadros por segundo
            self.clock.tick(fps)
       
    
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
                    player.teclas['esquerda'] = True
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    player.teclas['direita'] = True
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    player.teclas['cima'] = True
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    player.teclas['baixo'] = True
                if evento.key == pygame.K_SPACE:                                           
                    player.new_rocket(player.rockets)
                            
            # quando uma tecla é solta
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    player.teclas['esquerda'] = False
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    player.teclas['direita'] = False
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    player.teclas['cima'] = False
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    player.teclas['baixo'] = False
            
            # mouse
            if evento.type == pygame.MOUSEMOTION:
                # Se o mouse se move, movimenta jogador para onde o cursor está.
                dx = player.col_rect.centerx
                dy = player.col_rect.centery
                #pygame.mouse.set_pos(dx,dy)
                player.col_rect.move_ip(evento.pos[0] - dx, evento.pos[1] - dy)                
                for comp in player.components:
                    comp.col_rect.move_ip(evento.pos[0] - dx, evento.pos[1] - dy)
                                                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                player.new_rocket()                         
        return True
    
    
    def check_collision (self ):        
        # Checando se jogador ou algum rocket colidiu com algum rock.
        for rock in self.rocks:
            jogadorColidiu = False
            if not rock.dead:
                if self.col_rect.colliderect(rock.col_rect):
                    offset = (rock.col_rect.x - self.col_rect.x, rock.col_rect.y - self.col_rect.y)
                    jogadorColidiu = self.mask.overlap(rock.mask, offset)
                if jogadorColidiu:  
                    sound_player['ship'][0].play()          
                    return False 
            for rocket in player.rockets:
                if not rock.dead:
                    rocketColidiu = rocket.col_rect.colliderect(rock.col_rect)
                    if rocketColidiu:
                        rock.explode()                                   
                        player.rockets.remove(rocket)
                        score = score + 50
        # Checando se jogador ou algum rocket colidiu com algum mob.
        for mob in self.mobs:
            jogadorColidiu = False
            if not mob.dead:
                if self.col_rect.colliderect(mob.col_rect):
                    offset = (mob.col_rect.x - self.col_rect.x, mob.col_rect.y - self.col_rect.y)
                    jogadorColidiu = self.mask.overlap(mob.mask, offset)
                if jogadorColidiu:  
                    sound_player['ship'][0].play()           
                    return False
            for rocket in player.rockets:
                if not mob.dead:
                    rocketColidiu = rocket.col_rect.colliderect(mob.col_rect)
                    if rocketColidiu:
                        mob.explode()                                   
                        player.rockets.remove(rocket)
                        score = score + 100
            for fire in mob.rockets:
                if self.col_rect.colliderect(fire.col_rect):
                    offset = (fire.col_rect.x - self.col_rect.x, fire.col_rect.y - self.col_rect.y)
                    jogadorColidiu = self.mask.overlap(fire.mask, offset)
                if jogadorColidiu:  
                    sound_player['ship'][0].play()        
                    return False  
        return True
    
    def populate_asteroid (self, counter):
        # Adicionando rocks quando indicado.        
        if counter >= ITERACOES:
            counter = 0
            tamAsteroide = random.randint(TAMMINIMO, TAMMAXIMO)
            pos = disp_size
            posX = random.randint(0, pos[0] - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(-1,1)
            vel_y = random.randint(VELMINIMA, VELMAXIMA)
            
            size = [tamAsteroide, tamAsteroide]
            vel = [vel_x, vel_y]                #velocity/speed
            
            rock = Asteroid([posX, posY], size, vel)        #create enemy                   
            self.rocks.add(rock)
        return counter
    
    def populate_mobs (self, counter):
        # Adicionando mobs quando indicado.        
        if counter >= ITERACOES:
            counter = 0
            tamAsteroide = random.randint(TAMMINIMO, TAMMAXIMO)
            pos = disp_size
            posX = random.randint(0, pos[0] - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(-1,1)
            vel_y = random.randint(VELMINIMA, VELMAXIMA)
            size = [TAMMAXIMO, TAMMAXIMO]
            vel = [vel_x, vel_y]                #velocity/speed
            
            mob = Mob([posX, posY], size, vel)        #create enemy 
            self.mobs.add(mob)
        return counter
    
    def print_text(texto, x, y, position):
        ''' Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.'''
        objTexto = font.render(texto, True, COLOR_TEXT)
        rectTexto = objTexto.get_rect()
        if position == 'center':
            rectTexto.center = (x, y)
        elif position == 'topLeft':
            rectTexto.topleft = (x, y)
        window.blit(objTexto, rectTexto)


    def draw_background(self):
        ''' Preenchendo o fundo da janela com a imagem correspondente.'''
        #window.blit(imagemFundo, (0,0))  # old
        
        # movendo o fundo
        for i in range(0, tiles):
            pos_y = i * imagemFundo.get_height() + scroll
            window.blit(imagemFundo, (0,-pos_y))
        
        # update scroll
        scroll -= 1
        if abs(scroll)  > imagemFundo.get_height(): 
            scroll = 0
        
        # Colocando as pontuações.
        self.print_text('Pontuação: ' + str(score), 10, 0, 'topLeft')
        self.print_text('Recorde: ' + str(hi_score), 10, 40, 'topLeft')
        self.print_text('FPS: ' + str(clock.get_fps()), 10, 80, 'topLeft')
    
    
    def open_editor (self ):
        pass
    
    def exit(self):
        # Termina o programa.
        pygame.quit()
        exit()
    