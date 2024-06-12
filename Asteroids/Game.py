from .Player import Player, Player2
from .Enemy import Asteroid, Mob, Boss, PowerUP, ShieldUP
from .Settings import settings
from .Menu import *
from .SQL import *
from .Socket import *
import pygame
import random

class Game: 
    def __init__(self):
        settings.load_resources()
        
    def run(self):                
        menu = Basic_menu()
        select = menu.run()
        
        if select == 1:
            #self.login()
            menu_login()
            self.new_game()
        elif select == 2: 
            settings.multiplayer = True
            #self.login()
            menu_online()
            if settings.server:
                self.new_game()            
            else:
                # client mode
                #send player pos to server
                #get all lists of other elements
                pass
        elif select == 3:
            run_menu()
            if not settings.running:
               self.new_game() 
        elif select == 4:
            self.exit()
       
    def new_game (self):
        while True:                             # laço externo do game over
            # Configurando o começo do jogo.
            self.asteroids = pygame.sprite.Group()  # lista com os asteroids   
            self.mobs = pygame.sprite.Group()  # lista com as naves inimigas    
            self.pows = pygame.sprite.Group()  # lista com os power ups  
            self.shields = pygame.sprite.Group()  # lista com os shields para life          
            self.boss = None
            settings.running = True                    # indica se o loop do jogo deve continuar
            settings.score = 0                         # pontuação
            settings.life = 3                       # life
            settings.ups = 1                      #power shots
            self.counter = 0                    # contador de iterações
            self.counter2 = 0                    # contador de iterações
            self.level_counter=120              # countdown para mostrar novo level
            self.level = 0                      # fator para velocidade aumentar
            self.level_check = False            # veficia nova atualização da velocidade
            
            hi = sql_request()
            settings.hi_score = hi
            settings.name = str(sql_name().upper())
                   
            pygame.mixer.music.play(-1, 0.0)    # colocando a música de fundo
            
            #create player           
            self.player = Player()
            pygame.mouse.set_pos(self.player.pos[0],self.player.pos[1])     # inicializando mouse posicao player
            
            #create player 2
            if settings.multiplayer: self.player2 = Player2()
                                        
            #repetição principal
            self.main_loop()        # inicia novo jogo
                                    
            # if game over close online connection
            if settings.multiplayer: settings.open_connection = False                        
            
            # Parando o jogo e mostrando a tela final.
            if self.boss != None and self.boss.dead: self.__menu_win__()        
            else: self.__menu_last__()
        
    def main_loop (self):
        ''' new game'''
        while settings.running:                  
            self.counter += 1
            self.counter2 += 1
            settings.time += 1
                        
            #verifica eventos e atualiza em memória       
            settings.running = self.check_events()
                        
            #criar inimigos   
            if self.level <= 5: 
                self.counter = self.populate_asteroid(self.counter)            
            self.counter2 = self.populate_mobs(self.counter2)
            
            # preenchendo o fundo de janela com a sua imagem
            self.draw_background()
            
            #atualiza inimigos                        
            self.asteroids.update()
            self.mobs.update()
            for mob in self.mobs:
                mob.move(self.player.col_rect.centerx)
            self.pows.update()
            self.shields.update()
            if self.boss != None:
                self.boss.update()
                self.boss.move(self.player.col_rect.centerx)
                        
            #atualiza jogador   
            self.player.update()
            settings.running = self.check_collision()
            
            #online
            if settings.multiplayer and settings.server:
                self.player2.update()
            
            #derrotou o boss
            if self.boss != None and self.boss.dead \
                    and self.boss.idx_ani >= len(self.boss.list_surf)-1 \
                    and self.boss.delay > self.boss.delay_ani-1:
                settings.running = False
            
            # verifica fim de jogo com recorde
            if not settings.running and settings.score > settings.hi_score:
                settings.hi_score = settings.score
                sql_update(settings.hi_score)                 
                
            # verifica aumento de velocidade
            #if (self.level==0 or settings.score > self.level * settings.level_points) \
            if (self.level==0 or settings.time > settings.time_level)\
                    and self.level_counter==120:
                self.level_check = True 
                settings.time = 0               
            if self.level_check:                
                if self.level_counter>0:
                    self.level_counter -=1
                    pos = settings.disp_size
                    offset = settings.font_size
                    if self.level>= 0 and self.level<5: 
                        self.print_text('LEVEL '+str(self.level+1), (pos[0]/2),(pos[1]/2)-offset, 'center') 
                    elif self.level == 5: 
                        self.print_text('FINAL STAGE ', (pos[0]/2),(pos[1]/2)-offset, 'center')
                else:    
                    settings.VELMINIMA = settings.VELMINIMA + (self.level)
                    if settings.VELMINIMA > settings.VELMAXIMA: settings.VELMINIMA = settings.VELMAXIMA                    
                    self.level_check = False
                    self.level += 1
                    self.level_counter=120
            
            # mostrando na tela tudo o que foi desenhado
            #pygame.display.flip()
            pygame.display.update()    
                
            # limitando a 60 quadros por segundo
            settings.clock.tick(settings.fps)
       
    
    def check_events(self):
        #print("Tratando...")
        for evento in pygame.event.get():
            # Se for um evento QUIT
            if evento.type == pygame.QUIT:
                #if settings.multiplayer and settings.server: 
                settings.open_connection = False
                pygame.quit()
                self.exit()  
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    run_menu()
                    #self.exit()   
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
            #player colide asteroid
            if not rock.dead:
                if self.player.col_rect.colliderect(rock.col_rect):
                    offset = (rock.col_rect.x - self.player.col_rect.x, rock.col_rect.y - self.player.col_rect.y)
                    jogadorColidiu = self.player.mask.overlap(rock.mask, offset)
                if jogadorColidiu: 
                    rock.dead = True
                    return self.reduce_life()
            #player destroy asteroid
            for rocket in self.player.rockets:
                if not rock.dead:
                    rocketColidiu = rocket.col_rect.colliderect(rock.col_rect)
                    if rocketColidiu:
                        rock.explode()                                   
                        self.player.rockets.remove(rocket)
                        settings.score = settings.score + 50
            if rock.dead and rock.idx_ani >= len(rock.list_surf)-1 and rock.delay > rock.delay_ani-1:                   
                r = random.randint(1,settings.luck)                        
                if r == 1 and settings.life < 3:
                    shield = ShieldUP(rock.col_rect.center, (50,50))                               
                    self.shields.add(shield) 
        # Checando se jogador ou algum rocket colidiu com algum mob.
        for mob in self.mobs:
            jogadorColidiu = False
            # check player colide enemy
            if not mob.dead:
                if self.player.col_rect.colliderect(mob.col_rect):
                    offset = (mob.col_rect.x - self.player.col_rect.x, mob.col_rect.y - self.player.col_rect.y)
                    jogadorColidiu = self.player.mask.overlap(mob.mask, offset)
                if jogadorColidiu: 
                    mob.life -= 1
                    if mob.life == 0: 
                        mob.explode()
                        settings.score = settings.score + 100 
                    else: 
                        mob.sounds[0].play()                    
                    return self.reduce_life()
            # check player destroy enemy
            for rocket in self.player.rockets:
                if not mob.dead:
                    rocketColidiu = rocket.col_rect.colliderect(mob.col_rect)
                    if rocketColidiu:
                        mob.life -= 1
                        if mob.life == 0: 
                            mob.explode()
                            settings.score = settings.score + 100 
                        else: 
                            mob.sounds[0].play()                                                       
                        self.player.rockets.remove(rocket)
            #power up
            if mob.dead and mob.idx_ani >= len(mob.list_surf)-1 and mob.delay > mob.delay_ani-1:                   
                r = random.randint(1,settings.luck)                        
                if r == 1 and settings.ups < 5:
                    pow = PowerUP(mob.col_rect.center, (50,50))                               
                    self.pows.add(pow)                    
            # enemy rockets hit player
            for fire in mob.rockets:
                if self.player.col_rect.colliderect(fire.col_rect):
                    offset = (fire.col_rect.x - self.player.col_rect.x, fire.col_rect.y - self.player.col_rect.y)
                    jogadorColidiu = self.player.mask.overlap(fire.mask, offset)
                if jogadorColidiu: 
                    mob.rockets.remove(fire)
                    return self.reduce_life() 
        # player get powerup
        for pow in self.pows:
            jogadorColidiu = False
            if not pow.dead:
                if self.player.col_rect.colliderect(pow.col_rect):
                    offset = (pow.col_rect.x - self.player.col_rect.x, pow.col_rect.y - self.player.col_rect.y)
                    jogadorColidiu = self.player.mask.overlap(pow.mask, offset)
                if jogadorColidiu:
                    if settings.ups < 5:
                        settings.ups += 1                    
                        pow.get()
                    pow.kill() 
        # player get shield - life
        for shield in self.shields:
            jogadorColidiu = False
            if not shield.dead:
                if self.player.col_rect.colliderect(shield.col_rect):
                    offset = (shield.col_rect.x - self.player.col_rect.x, shield.col_rect.y - self.player.col_rect.y)
                    jogadorColidiu = self.player.mask.overlap(shield.mask, offset)
                if jogadorColidiu:
                    if settings.life < 3:
                        settings.life += 1                    
                        shield.get()
                    shield.kill()    
        # check boss
        jogadorColidiu = False
        if self.boss != None:
            # check player colide boss
            if not self.boss.dead:
                if self.player.col_rect.colliderect(self.boss.col_rect):
                    offset = (self.boss.col_rect.x - self.player.col_rect.x, self.boss.col_rect.y - self.player.col_rect.y)
                    jogadorColidiu = self.player.mask.overlap(self.boss.mask, offset)
                if jogadorColidiu: 
                    self.boss.life -= 1
                    if self.boss.life == 0: 
                        self.boss.explode()
                        settings.score = settings.score + 1000 
                    else: 
                        self.boss.sounds[0].play()
                    return self.reduce_life()
            # check player destroy boss
            for rocket in self.player.rockets:
                if not self.boss.dead:
                    rocketColidiu = rocket.col_rect.colliderect(self.boss.col_rect)
                    if rocketColidiu:
                        self.boss.life -= 1
                        if self.boss.life == 0: 
                            self.boss.explode()
                            settings.score = settings.score + 1000 
                        else: 
                            self.boss.sounds[0].play()
                        self.player.rockets.remove(rocket)                                              
            # enemy rockets hit player
            for fire in self.boss.rockets:
                if self.player.col_rect.colliderect(fire.col_rect):
                    offset = (fire.col_rect.x - self.player.col_rect.x, fire.col_rect.y - self.player.col_rect.y)
                    jogadorColidiu = self.player.mask.overlap(fire.mask, offset)
                if jogadorColidiu: 
                    self.boss.rockets.remove(fire)
                    return self.reduce_life()                    
        return True
    
    def reduce_life(self):
        settings.sound_player['ship'][0].play()
        if settings.life > 1:
            if not eval(settings.hack['god']): settings.life -= 1
            return True
        else:                    
            return False
            
        
    
    def populate_asteroid (self, counter):
        # Adicionando asteroids quando indicado.        
        if counter >= settings.ITERACOES/(self.level+1):
            counter = 0
            tamAsteroide = random.randint(settings.TAMMINIMO, settings.TAMMAXIMO)
            pos = settings.disp_size
            posX = random.randint(0, pos[0] - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(-2,2)
            vel_y = random.randint(settings.VELMINIMA, settings.VELMAXIMA)
            
            size = [tamAsteroide, tamAsteroide]
            vel = [vel_x, vel_y]                #velocity/speed
            
            # not spawn mobs in intermission
            if self.level_counter == 120:
                rock = Asteroid([posX, posY], size, vel)        #create enemy                   
                self.asteroids.add(rock)
        return counter
    
    def populate_mobs (self, counter):
        # Adicionando mobs quando indicado.        
        if counter >= settings.ITERACOES/(self.level+1):
            counter = 0
            tamAsteroide = random.randint(settings.TAMMINIMO, settings.TAMMAXIMO)
            pos = settings.disp_size
            posX = random.randint(0, pos[0] - tamAsteroide)
            posY = - tamAsteroide
            vel_x = random.randint(settings.VELMINIMA, settings.VELMINIMA)
            vel_y = random.randint(settings.VELMAXIMA, settings.VELMAXIMA)
            size = [settings.TAMMAXIMO, settings.TAMMAXIMO]
            if eval(settings.hack['easy']):
                vel_x = int(vel_x/2)
                vel_y = int(vel_y/2)
            vel = [(vel_x*self.level)/2, (vel_y*self.level)/2]                #velocity/speed
            
            # mob configs
            type = 1
            mob_surf = 'enemy1'
            mob_fire_delay = 60
            if self.level == 2: 
                type = 2
                mob_surf = 'enemy2'
                mob_fire_delay = 55
            if self.level == 3: 
                type = 3
                mob_surf = 'enemy3'
                mob_fire_delay = 50
            if self.level == 4: 
                type = 4
                mob_surf = 'enemy4'
                mob_fire_delay = 45
            if self.level == 5: 
                type = 5
                mob_surf = 'sub_boss'
                mob_fire_delay = 40            
            #add boss
            if self.level == 6 and self.boss == None:
                self.boss = Boss([pos[0]/2, 50], (300,300), (0,0), 'boss', 40)                
                #counter = 0
            
            # not spawn mobs in intermission
            if self.level_counter == 120: 
                if eval(settings.hack['easy']):
                       mob_fire_delay = mob_fire_delay*3
                mob = Mob([posX, posY], size, vel, mob_surf, mob_fire_delay, type)        #create enemy
                if self.level >= 5:
                    mob.life = 3
                    mob.maxlife = 3
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
        self.print_text(settings.name, 10, 0, 'topLeft')
        self.print_text('' + str(settings.score), 10, 40, 'topLeft')
        self.print_text('HI SCORE: ' + str(settings.hi_score) +' '+ settings.name,
                        settings.disp_size[0]/2, 20, 'center')
        if self.level == 0: lv=str(self.level+1)
        else: lv= str(self.level)
        if self.level == 6: lv ='FINAL'
        self.print_text(f'LEVEL {lv}', 10, 80, 'topLeft')
        self.print_text('FPS: ' + str(int(settings.clock.get_fps())), 10, 120, 'topLeft')
        
        #desenhando a vida da nave
        offset = 120
        self.print_text('SHIELD', 10, settings.disp_size[1]-(offset-30), 'topLeft')
        if settings.life == 3:
            settings.window.blit(settings.surf_player['life'][0], (150,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][0], (220,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][0], (290,settings.disp_size[1]-offset))
        elif settings.life == 2:
            settings.window.blit(settings.surf_player['life'][0], (150,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][0], (220,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][1], (290,settings.disp_size[1]-offset))
        elif settings.life == 1:
            settings.window.blit(settings.surf_player['life'][0], (150,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][1], (220,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][1], (290,settings.disp_size[1]-offset))
        else: 
            settings.window.blit(settings.surf_player['life'][1], (150,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][1], (220,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][1], (290,settings.disp_size[1]-offset))
        
        #desenhando os power ups
        offset = 40
        self.print_text('POWER UP', 10, settings.disp_size[1]-offset, 'topLeft')
        settings.window.blit(settings.surf_player['ups'][settings.ups-1], (200,settings.disp_size[1]-offset))
    
    
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
        
    def __menu_win__(self):        
        pygame.mixer.music.stop()
        #settings.sound_over.play() 
        
        #limpando os grupos
        self.asteroids.empty()
        self.mobs.empty()
        self.boss = None
        self.player.kill()
        
        self.draw_background()
        
        pos = settings.disp_size
        offset = settings.font_size
        self.print_text('YOU WIN!!!', (pos[0]/2),(pos[1]/2)-offset, 'center')
        self.print_text('Pressione F1 para recomeçar.', (pos[0]/2), (pos[1]/2)+offset, 'center')
        self.print_text('Pressione ESC para sair.', (pos[0]/2), (pos[1]/2)+offset*2, 'center')    
        
        pygame.display.update()
        # Aguardando entrada por teclado para reiniciar o jogo ou sair.
        self.__wait_input__()
        #settings.sound_over.stop()
           
    
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
    