from .Player import Player, Rocket, ShieldUP, PowerUP
from .Enemy import Asteroid, Mob, Boss
from .Settings import settings
from .Menu import *
from .SQL import *
from .Socket import *
import pygame
import random
import threading

class Game: 
    def __init__(self):
        settings.load_resources()
            
    def run(self):                
        menu = Basic_menu()
        select = menu.run()
        
        if select == 1:            
            menu_login()
            self.new_game()
        elif select == 2: 
            settings.multiplayer = True            
            menu_login()
            threading.Thread(target=self.get_message).start() 
            menu_online()
            self.client_message = Socket_client_message(settings.client, 4031)  
            self.new_game_P2()                           
        elif select == 3:
            run_menu()
            if not settings.running:
               self.new_game() 
        elif select == 4:
            self.exit()
    
    def get_message(self):         
        self.server_message = Socket_server_message('0.0.0.0', 4032)
        self.server_message.receive_messages()
    
    def new_game_P2 (self):
        while True:                             # laço externo do game over
            # Configurando o começo do jogo.
            self.asteroids = pygame.sprite.Group()  # lista com os asteroids   
            self.mobs = pygame.sprite.Group()  # lista com as naves inimigas    
            self.pows = pygame.sprite.Group()  # lista com os power ups  
            self.shields = pygame.sprite.Group()  # lista com os shields para life          
            self.boss = None
            settings.running = True                    # indica se o loop do jogo deve continuar            
            self.counter = 0                    # contador de iterações
            self.counter2 = 0                    # contador de iterações
            self.level_counter=120              # countdown para mostrar novo level
            self.level = 0                      # fator para velocidade aumentar
            self.level_check = False            # veficia nova atualização da velocidade
                       
            settings.hi_score = sql_request()
            settings.name = str(sql_name().upper())
                   
            pygame.mixer.music.play(-1, 0.0)    # colocando a música de fundo
            
            #create player           
            self.player = Player(type=2)
            #pygame.mouse.set_pos(self.player.pos[0],self.player.pos[1])     # inicializando mouse posicao player
            
            #create player 2
            if settings.multiplayer: self.player2 = Player(type=1)
                                        
            #repetição principal
            self.main_loop_P2()        # inicia novo jogo
           
            # Parando o jogo e mostrando a tela final.
            if self.boss != None and self.boss.dead: self.__menu_win__()        
            else: self.__menu_last__()
    
    
    def main_loop_P2 (self):
        ''' new game'''
        while settings.running:
            settings.time += 1
                        
            #verifica eventos e atualiza em memória       
            settings.running = self.check_events()
                                  
            # preenchendo o fundo de janela com a sua imagem
            self.draw_background()
            
            #atualiza inimigos       
            self.parse_message()    # socket receive                                 
            self.asteroids.update()
            self.mobs.update()                  
            self.pows.update()
            self.shields.update()
            if self.boss != None:
                self.boss.update()
                self.boss.move(self.player.col_rect.centerx)
            
             #atualiza jogador   
            if (self.player.life > 0):
                self.player.update()
                
                #send p1 to client
                X = self.player.col_rect.x
                Y = self.player.col_rect.y
                if settings.multiplayer:
                    message = 'update_'+'player'+'_'+str(X)+'_'+str(Y)+'_'
                    while len(message) < 64: message += '0'
                    self.client_message.send_message(message)                
            else: self.player.kill()
            
            #online
            if settings.multiplayer:
                if (self.player2.life > 0):
                    self.player2.update(player1=False)                    
                else: self.player2.kill()
                if (self.player.life == 0) and (self.player2.life == 0): settings.running = False
            
            #derrotou o boss
            if self.boss != None and self.boss.dead \
                    and self.boss.idx_ani >= len(self.boss.list_surf)-1 \
                    and self.boss.delay > self.boss.delay_ani-1:
                settings.running = False
            
            # verifica fim de jogo com recorde
            if not settings.running and self.player.score > settings.hi_score:
                settings.hi_score = self.player.score
                sql_update(settings.hi_score)             
            if settings.multiplayer:                
                if not settings.running and self.player2.score > settings.hi_score:
                    settings.hi_score = self.player2.score
                    sql_update(settings.hi_score)            
            
            # verifica nivel game
            self.check_level()
            
            # mostrando na tela tudo o que foi desenhado
            pygame.display.flip()
            #pygame.display.update()    
                
            # limitando a 60 quadros por segundo
            settings.clock.tick(settings.fps)
    
    
    def parse_message(self):
        while(len(settings.buffer_message) > 0):   # get and parse message
            message:str = str(settings.buffer_message.pop(0))
            commands = message.split('_')
            if(commands[0] == 'asteroid'):
                ID = int(commands[1])
                posX = int(commands[2])
                posY = int(commands[3])
                size = [int(commands[4]), int(commands[5])]
                vel = [int(commands[6]), int(commands[7])]
                rock = Asteroid(ID, [posX, posY], size, vel)        #create enemy 
                self.asteroids.add(rock)
            elif (commands[0] == 'mob'):
                ID = int(commands[1])
                posX = int(commands[2])
                posY = int(commands[3])
                size = [int(commands[4]), int(commands[5])]
                vel = [int(commands[6]), int(commands[7])]
                mob_surf = str(commands[8])
                mob_fire_delay = int(commands[9])
                type = int(commands[10])
                mob = Mob(ID, [posX, posY], size, vel, mob_surf, mob_fire_delay, type)
                self.mobs.add(mob)
            elif (commands[0] == 'update'):
                if (commands[1] == 'player'):
                    posX = int(commands[2])
                    posY = int(commands[3])
                    dx = self.player2.col_rect.x - posX
                    dy = self.player2.col_rect.y - posY
                    self.player2.col_rect.x = posX
                    self.player2.col_rect.y = posY
                    for comp in self.player2.components:
                        comp.col_rect.x -= dx
                        comp.col_rect.y -= dy
            elif (commands[0] == 'rocket'):                
                ID = int(commands[1])
                pos = [int(commands[2]),int(commands[3])]
                size = [int(commands[4]),int(commands[5])]
                speed = [int(commands[6]),int(commands[7])]
                rotate = int(commands[8])                
                rocket = Rocket(ID, pos, size, speed, rotate)
                rocket.col_rect.center = pos                  
                self.player2.rockets.add(rocket)    
            elif (commands[0] == 'up'):
                ups = int(commands[2])
                if (commands[1] == 'player2'): self.player.ups = ups                    
                elif (commands[1] == 'player1'): self.player2.ups = ups  
                ID = int(commands[3])
                #print(f'POW ID {commands}')
                for pow in self.pows:   
                    #print(f'POW ID {pow.ID} and {ID}')                        
                    if pow.ID == ID: pow.kill()                     
            elif (commands[0] == 'life'):
                life = int(commands[2])
                if (commands[1] == 'player2'): self.player.life = life                    
                elif (commands[1] == 'player1'): self.player2.life = life
                ID = int(commands[3])
                for shield in self.shields:                           
                    if shield.ID == ID: shield.kill()
            elif (commands[0] == 'dead'):
                if (commands[1] == 'rock'):                    
                    if (commands[2] == 'score'):
                        add_score = int(commands[4])
                        ID = int(commands[5])
                        for rock in self.asteroids:                           
                            if rock.ID == ID: rock.explode()
                        if (commands[3] == 'player2'): 
                            self.player.score += add_score                           
                            if (commands[6] == 'rocket'):
                                rocket_ID = int(commands[7])
                                remove = None
                                for rocket in self.player.rockets:
                                    if rocket.ID == rocket_ID: 
                                        remove = rocket
                                        break
                                if remove: self.player.rockets.remove(rocket)                                        
                        elif (commands[3] == 'player1'):
                            self.player2.score += add_score
                            if (commands[6] == 'rocket'):
                                rocket_ID = int(commands[7])
                                remove = None
                                for rocket in self.player2.rockets:
                                    if rocket.ID == rocket_ID: 
                                        remove = rocket
                                        break
                                if remove: self.player2.rockets.remove(rocket)
                if (commands[1] == 'mob'):
                    if (commands[2] == 'score'):
                        add_score = int(commands[4])
                        ID = int(commands[5])
                        for mob in self.mobs:
                            if mob.ID == ID: mob.explode()
                        if (commands[3] == 'player2'): 
                            self.player.score += add_score                           
                            if (commands[6] == 'rocket'):
                                rocket_ID = int(commands[7])
                                remove = None
                                for rocket in self.player.rockets:
                                    if rocket.ID == rocket_ID: 
                                        remove = rocket
                                        break
                                if remove: self.player.rockets.remove(rocket)                                        
                        elif (commands[3] == 'player1'):
                            self.player2.score += add_score
                            if (commands[6] == 'rocket'):
                                rocket_ID = int(commands[7])
                                remove = None
                                for rocket in self.player2.rockets:
                                    if rocket.ID == rocket_ID: 
                                        remove = rocket
                                        break
                                if remove: self.player2.rockets.remove(rocket)
                if (commands[1] == 'boss'):
                    if (commands[2] == 'score'):
                        add_score = int(commands[4])
                        self.boss.explode()
                        if (commands[3] == 'player2'): 
                            self.player.score += add_score                           
                            if (commands[5] == 'rocket'):
                                rocket_ID = int(commands[6])
                                remove = None
                                for rocket in self.player.rockets:
                                    if rocket.ID == rocket_ID: 
                                        remove = rocket
                                        break
                                if remove: self.player.rockets.remove(rocket)                                        
                        elif (commands[3] == 'player1'):
                            self.player2.score += add_score
                            if (commands[5] == 'rocket'):
                                rocket_ID = int(commands[6])
                                remove = None
                                for rocket in self.player2.rockets:
                                    if rocket.ID == rocket_ID: 
                                        remove = rocket
                                        break
                                if remove: self.player2.rockets.remove(rocket)
            elif (commands[0] == 'shield'):
                ID = int(commands[1])
                pos = [int(commands[2]),int(commands[3])]
                size = [int(commands[4]),int(commands[5])]
                shield = ShieldUP(ID, pos, size)                               
                self.shields.add(shield)   
            elif (commands[0] == 'pow'):
                ID = int(commands[1])
                pos = [int(commands[2]),int(commands[3])]
                size = [int(commands[4]),int(commands[5])]
                pow = PowerUP(ID, pos, size)                               
                self.pows.add(pow) 
            elif (commands[0] == 'hurt'):
                #print(f'hurt mob...')                      
                if (commands[1] == 'mob'):
                    ID = int(commands[3])    
                    for mob in self.mobs:
                        #print(f'hurt mob {ID} and {mob.ID}')
                        if mob.ID == ID: mob.life -= 1
                    if (commands[2] == 'player2'):
                        if (commands[4] == 'rocket'):
                            rocket_ID = int(commands[5])
                            remove = None
                            for rocket in self.player.rockets:
                                if rocket.ID == rocket_ID: 
                                    remove = rocket
                                    break
                            if remove: self.player.rockets.remove(rocket)  
                        else: self.player.life -= 1                                    
                    elif (commands[2] == 'player1'):
                        if (commands[4] == 'rocket'):
                            rocket_ID = int(commands[5])
                            remove = None
                            for rocket in self.player2.rockets:
                                if rocket.ID == rocket_ID: 
                                    remove = rocket
                                    break
                            if remove: self.player2.rockets.remove(rocket)
                        else: self.player2.life -= 1         
                if (commands[1] == 'boss'):
                    self.boss.life -= 1
                    if (commands[2] == 'player2'):
                        if (commands[3] == 'rocket'):
                            rocket_ID = int(commands[4])
                            remove = None
                            for rocket in self.player.rockets:
                                if rocket.ID == rocket_ID: 
                                    remove = rocket
                                    break
                            if remove: self.player.rockets.remove(rocket)  
                        else: self.player.life -= 1                                    
                    elif (commands[2] == 'player1'):
                        if (commands[3] == 'rocket'):
                            rocket_ID = int(commands[4])
                            remove = None
                            for rocket in self.player2.rockets:
                                if rocket.ID == rocket_ID: 
                                    remove = rocket
                                    break
                            if remove: self.player2.rockets.remove(rocket)
                        else: self.player2.life -= 1
                    
    
    def check_level(self):
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
            if settings.multiplayer: self.player2 = Player()
                                        
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
            #for mob in self.mobs:
            #    mob.move(self.player.col_rect.centerx)
            self.pows.update()
            self.shields.update()
            if self.boss != None:
                self.boss.update()
                self.boss.move(self.player.col_rect.centerx)
                        
            #atualiza jogador   
            self.player.update()            
            settings.running = self.player.check_collision(self.asteroids, self.mobs, self.pows,
                                                       self.shields, self.boss)
                    
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
                    if settings.multiplayer:
                        self.player.new_rocket(self.client_message)
                    else: self.player.new_rocket()
                            
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
        return True
        
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
                rock = Asteroid(1, [posX, posY], size, vel)        #create enemy                   
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
                mob_surf = 'subboss'
                mob_fire_delay = 40            
            #add boss
            if self.level == 6 and self.boss == None:
                self.boss = Boss([pos[0]/2, 50], (300,300), (0,0), 'boss', 40)                
                #counter = 0
            
            # not spawn mobs in intermission
            if self.level_counter == 120: 
                if eval(settings.hack['easy']):
                       mob_fire_delay = mob_fire_delay*3
                mob = Mob(1, [posX, posY], size, vel, mob_surf, mob_fire_delay, type)        #create enemy
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
        elif position == 'topRight':
            rectTexto.topright = (x, y)
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
        self.print_text('' + str(self.player.score), 10, 40, 'topLeft')
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
        if self.player.life == 3:
            settings.window.blit(settings.surf_player['life'][0], (150,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][0], (220,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][0], (290,settings.disp_size[1]-offset))
        elif self.player.life == 2:
            settings.window.blit(settings.surf_player['life'][0], (150,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][0], (220,settings.disp_size[1]-offset))
            settings.window.blit(settings.surf_player['life'][1], (290,settings.disp_size[1]-offset))
        elif self.player.life == 1:
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
        settings.window.blit(settings.surf_player['ups'][self.player.ups-1], (200,settings.disp_size[1]-offset))
        
        #player 2
        if settings.multiplayer: 
             # Colocando as pontuações.
            self.print_text(settings.name, settings.disp_size[0]-10, 0, 'topRight')
            self.print_text('' + str(self.player2.score), settings.disp_size[0]-10, 40, 'topRight')
                        
            #desenhando a vida da nave
            offset = 120
            x = settings.disp_size[0]
            y = settings.disp_size[1]-offset
            #self.print_text('SHIELD', 10, settings.disp_size[1]-(offset-30), 'topLeft')
            if self.player2.life == 3:
                settings.window.blit(settings.surf_player['life'][0], (x-70,y))
                settings.window.blit(settings.surf_player['life'][0], (x-140,y))
                settings.window.blit(settings.surf_player['life'][0], (x-210,y))
            elif self.player2.life == 2:
                settings.window.blit(settings.surf_player['life'][0], (x-70,y))
                settings.window.blit(settings.surf_player['life'][0], (x-140,y))
                settings.window.blit(settings.surf_player['life'][1], (x-210,y))
            elif self.player2.life == 1:
                settings.window.blit(settings.surf_player['life'][0], (x-70,y))
                settings.window.blit(settings.surf_player['life'][1], (x-140,y))
                settings.window.blit(settings.surf_player['life'][1], (x-210,y))
            else: 
                settings.window.blit(settings.surf_player['life'][1], (x-70,y))
                settings.window.blit(settings.surf_player['life'][1], (x-140,y))
                settings.window.blit(settings.surf_player['life'][1], (x-210,y))
            
            #desenhando os power ups
            offset = 40
            #self.print_text('POWER UP', 10, settings.disp_size[1]-offset, 'topLeft')
            settings.window.blit(settings.surf_player['ups'][self.player2.ups-1], (x-160,settings.disp_size[1]-offset))
    
        
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
    
    def exit(self):
        # Termina o programa.
        pygame.quit()
        exit()
    