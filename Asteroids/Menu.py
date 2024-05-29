from customtkinter import *
from PIL import Image, ImageTk
from .Settings import settings
import pygame

def set_tab1(w,h,tab):  
    frame = CTkFrame(master=tab, width=w, height=h, fg_color='#333333', corner_radius=3, border_width=2)
    frame.place(relx=0.5, rely=0.6, anchor='center')
    
    l1 = CTkLabel(master=frame, text='OPTIONS',font=('Arial',40),text_color='#111111')
    l1.place(relx=0.5, rely=0.1, anchor='center')
    
    set_start_exit(frame)
    

def set_tab2(w,h,tab):
    frame = CTkFrame(master=tab, width=w, height=h, fg_color='#333333', corner_radius=3, border_width=2)
    frame.place(relx=0.5, rely=0.6, anchor='center')
    
    set_start_exit(frame)
    

def set_tab3(w,h,tab): 
    frame = CTkFrame(master=tab, width=w, height=h, fg_color='#333333', corner_radius=3, border_width=2)
    frame.place(relx=0.5, rely=0.6, anchor='center')
                  
    l1 = CTkLabel(master=frame, text='Resolution',font=('Arial',20),text_color='#111111')
    l1.place(relx=0.4, rely=0.2, anchor='center')
    
    def set_resolution(value:str):         
        res = value.split('x')
        settings.menu.geometry(f'{res[0]}x{res[1]}')
        
        settings.disp_size = (int(res[0]),int(res[1]))       
        settings.window = pygame.display.set_mode((int(res[0]),int(res[1])))
        if settings.fullscreen: pygame.display.toggle_fullscreen()       

    list = ['1920x1080','1600x1024','1366x768','1280x720','1024x768']
    cbox1 = CTkComboBox(master=frame, values=list, corner_radius=30, 
                border_width=2, command=set_resolution)
    cbox1.place(relx=0.5, rely=0.2, anchor='center')
    
    set_start_exit(frame)


def set_tab4(w,h,tab):
    frame = CTkFrame(master=tab, width=w, height=h, fg_color='#333333', corner_radius=3, border_width=2)
    frame.place(relx=0.5, rely=0.6, anchor='center')
    
    set_start_exit(frame)
    

def set_tab5(w,h,tab):
    frame = CTkFrame(master=tab, width=w, height=h, fg_color='#333333', corner_radius=3, border_width=2)
    frame.place(relx=0.5, rely=0.6, anchor='center')
    
    l1 = CTkLabel(master=frame, text='GAME PAUSED',font=('Arial',30),text_color='#111111')
    l1.place(relx=0.5, rely=0.1, anchor='center')   
        
    def set_easy():
        if cvar.get() == 'True': settings.hack['easy'] = 'True'
        else: settings.hack['easy'] = 'False'
        print(cvar.get())             
    
    cvar = StringVar(value = str(settings.hack['easy']))
    chbox1 = CTkCheckBox(master=frame, text='EasyMode', corner_radius=30, 
                fg_color='#111111', checkbox_height=25, checkbox_width=25,
                onvalue='True', offvalue='False', variable=cvar, command=set_easy)
    chbox1.place(relx=0.3, rely=0.7, anchor='center')
        
    def set_god():
        if gvar.get() == 1: settings.hack['god'] = 'True'
        else: settings.hack['god'] = 'False'
    
    gvar = IntVar(value = 1 if eval(settings.hack['god']) else 0)    
    sw1 = CTkSwitch(master=frame, text='GodMode',
                    onvalue=1, offvalue=0, variable=gvar,
                    command=set_god)
    sw1.place(relx=0.7, rely=0.7, anchor='center')
    
    set_start_exit(frame)

def set_start_exit(frame):
    if settings.running:
        lab1 = 'GAME PAUSED'
        lab2 = 'CONTINUE GAME'
    else:
        lab1 = 'GAME ASTEROIDS'
        lab2 = 'START GAME'
    
    l2 = CTkLabel(master=frame, text=lab1,font=('Arial',30),text_color='#111111')
    l2.place(relx=0.5, rely=0.1, anchor='center')
    
    def back_bt():        
        settings.menu.destroy()
        settings.menu.quit()

    #img = Image.open('images/ship.png')
    b1 = CTkButton(master=frame, text=lab2, corner_radius=30, fg_color='transparent',
                border_width=2, command=back_bt)
    b1.place(relx=0.5, rely=0.7, anchor='center')
    
    def exit_bt(): 
        pygame.quit()       
        exit()
        
    b2 = CTkButton(master=frame, text='EXIT GAME', corner_radius=30, fg_color='transparent',
                border_width=2, command=exit_bt)
    b2.place(relx=0.5, rely=0.8, anchor='center')
    

def run_menu():
    settings.menu = CTk() 
    set_appearance_mode('dark')
    set_default_color_theme('blue')
    w = settings.disp_size[0]
    h = settings.disp_size[1]
        
    if settings.fullscreen:
        settings.menu.attributes("-fullscreen", "True")
        settings.menu.state('zoomed')

    t_view = CTkTabview(master=settings.menu, width=w, height=h)
    t_view.pack(padx=50,pady=50)

    t_view.add('General')
    t_view.add('Control')
    t_view.add('Screen')
    t_view.add('Sounds')
    t_view.add('Hacks')
    
    set_tab1(w,h,t_view.tab('General'))
    set_tab2(w,h,t_view.tab('Control'))
    set_tab3(w,h,t_view.tab('Screen'))
    set_tab4(w,h,t_view.tab('Sounds'))
    set_tab5(w,h,t_view.tab('Hacks'))

    settings.menu.mainloop()
    
    return 0
    

def run_menu2():      
    w = settings.disp_size[0]
    h = settings.disp_size[1]
     
    t_view = CTkTabview(master=settings.menu, width=w, height=h, fg_color='#223344')
    t_view.pack(padx=50,pady=50)

    t_view.add('Control')
    t_view.add('Screen')
    t_view.add('Sounds')
        
    set_tab2(w,h,t_view.tab('Control'))
    set_tab3(w,h,t_view.tab('Screen'))
    set_tab4(w,h,t_view.tab('Sounds'))
    
    def back_bt(): 
        t_view.destroy()
        b2.destroy()
        
    b2 = CTkButton(master=settings.menu, text='< BACK', corner_radius=30, fg_color='#333333',
                bg_color='#333333', border_width=2,
                command=back_bt)
    b2.place(relx=0.1, rely=0.15, anchor='center')


def launcher(w,h):        
    image = Image.open("images/space.jpg")
    background_image = CTkImage(image, size=(w,h))
    
    bg_lbl = CTkLabel(settings.menu, text="", image=background_image)
    bg_lbl.place(x=0, y=0)
        
    frame = CTkFrame(master=settings.menu, width=int(w/4), height=int(h/2),
                     fg_color='#223344', corner_radius=2, border_width=2)
    frame.place(relx=0.5, rely=0.6, anchor='center')
        
    l1 = CTkLabel(master=frame, text='Asteroids',font=('Arial',40),text_color='#666666',
                  fg_color='transparent', bg_color='transparent')
    l1.place(relx=0.5, rely=0.1, anchor='center')
    
    l2 = CTkLabel(master=frame, text='Launcher',font=('Arial',30),text_color='#666666',
                  fg_color='transparent', bg_color='transparent')
    l2.place(relx=0.5, rely=0.2, anchor='center')
    
    def back_bt():        
        settings.menu.destroy()

    #img = Image.open('images/ship.png')
    b1 = CTkButton(master=frame, text='START', corner_radius=30, fg_color='transparent',
                hover_color='#666666', border_width=2, bg_color='transparent',
                #image=CTkImage(dark_image=img, light_image=img), 
                command=back_bt)
    b1.place(relx=0.5, rely=0.4, anchor='center')
            
    def opt_bt(): 
        run_menu2()
        
    b2 = CTkButton(master=frame, text='OPTIONS', corner_radius=30, fg_color='transparent',
                hover_color='#666666', border_width=2, bg_color='transparent',
                command=opt_bt)
    b2.place(relx=0.5, rely=0.5, anchor='center')        
           
    def exit_bt(): 
        pygame.quit()       
        exit()
        
    b3 = CTkButton(master=frame, text='EXIT', corner_radius=30, fg_color='transparent',
                hover_color='#666666', border_width=2, bg_color='transparent',
                command=exit_bt)
    b3.place(relx=0.5, rely=0.6, anchor='center')
  
 
def run_launcher():
    set_appearance_mode('dark')
    set_default_color_theme('blue')
    w = settings.disp_size[0]
    h = settings.disp_size[1]
            
    if settings.fullscreen:
        settings.menu.attributes("-fullscreen", "True")
        settings.menu.state('zoomed')

    launcher(w,h)
    
    settings.menu.mainloop()
    
    
class Basic_menu():
    def __init__(self):
        settings.sound_menu.play()
               
        self.counter = 0        
        pos = [settings.disp_size[0]*0.5-200, settings.disp_size[1]*0.5]
        self.icon1 = Menu_ship(pos)
        pos = [settings.disp_size[0]*0.5+200, settings.disp_size[1]*0.5]
        self.icon2 = Menu_ship(pos)
                
        self.select = 1
        self.select_max = 4
        
    def run(self):    
        while True:    
            select = self.check_keys()
            if select != 0:
                settings.sound_menu.stop() 
                return select
                                     
            self.draw_background_only()
            self.select_com()
            
            self.icon1.update()
            self.icon2.update()
            
            pygame.display.update()    
                
            # limitando a 60 quadros por segundo
            settings.clock.tick(settings.fps)     
        
    def select_com(self):
        pos = settings.disp_size
        offset = settings.font_size
        self.print_text('START GAME', (pos[0]/2),(pos[1]/2), 'center')
        self.print_text('MULTIPLAYER', (pos[0]/2), (pos[1]/2)+offset, 'center')
        self.print_text('OPTIONS', (pos[0]/2), (pos[1]/2)+offset*2, 'center')
        self.print_text('EXIT', (pos[0]/2), (pos[1]/2)+offset*3, 'center')
        
        #draw rect        
        x = settings.disp_size[0]*0.5-150
        y = settings.disp_size[1]*0.5-(int(offset/2))+(offset*(self.select-1))
        sel_rect = pygame.Rect(x,y,300,int(offset))
        pygame.draw.rect(settings.window, 'red', sel_rect, 1)
        
        
    def check_keys(self):
        for evento in pygame.event.get():
            # Se for um evento QUIT
            if evento.type == pygame.QUIT:
                self.exit()  
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.exit()  
                if evento.key == pygame.K_RETURN:
                    return self.select
                if evento.key == pygame.K_DOWN:
                    if self.select < self.select_max:
                        self.select += 1
                        self.icon1.change_pos((self.icon1.getx(),self.icon1.gety()+50))
                        self.icon2.change_pos((self.icon2.getx(),self.icon2.gety()+50))
                if evento.key == pygame.K_UP:
                    if self.select > 1:
                        self.select -= 1
                        self.icon1.change_pos((self.icon1.getx(),self.icon1.gety()-50))
                        self.icon2.change_pos((self.icon2.getx(),self.icon2.gety()-50))
                if evento.key == pygame.K_LEFT:
                    pass
                if evento.key == pygame.K_RIGHT:
                    pass
        return 0
    
    def print_text(self, texto, x, y, position):
        ''' Coloca na posição (x,y) da janela o texto com a fonte passados por argumento.'''
        objTexto = settings.font.render(texto, True, settings.COLOR_TEXT)
        rectTexto = objTexto.get_rect()
        if position == 'center':
            rectTexto.center = (x, y)
        elif position == 'topLeft':
            rectTexto.topleft = (x, y)
        settings.window.blit(objTexto, rectTexto)

    def draw_background_only(self):
        ''' Preenchendo o fundo da janela com a imagem correspondente.'''      
        # movendo o fundo
        for i in range(0, settings.tiles):
            pos_y = i * settings.imagemFundo.get_height() + settings.scroll
            settings.window.blit(settings.imagemFundo, (0,-pos_y))
        
        # update scroll
        settings.scroll -= 1
        if abs(settings.scroll)  > settings.imagemFundo.get_height(): 
            settings.scroll = 0
            
    def exit(self):
        # Termina o programa.
        pygame.quit()
        exit()
    

class Menu_ship():
    def __init__(self,pos:list):
        self.pos = pos
        self.size = (settings.surf_player['ship'][0].get_width()/10, settings.surf_player['ship'][0].get_height()/10)         
                        
        self.image = settings.surf_player['ship'][0]
        self.image = pygame.transform.scale(self.image, self.size)
        # A reference to the original image to preserve the quality.
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=self.pos)
        self.angle = 0

    def update(self):
        self.angle += 2
        self.rotate()
        settings.window.blit(self.image, self.rect)
        #colisao debug
        #pygame.draw.rect(settings.window,settings.COLOR_TEXT,self.rect,2)

    def rotate(self):
        """Rotate the image of the sprite around its center."""
        # `rotozoom` usually looks nicer than `rotate`. Pygame's rotation
        # functions return new images and don't modify the originals.
        self.image = pygame.transform.rotozoom(self.orig_image, self.angle, 1)
        # Create a new rect with the center of the old rect.
        self.rect = self.image.get_rect(center=self.rect.center)
    
    def change_pos(self, pos:list):
        self.pos = pos
        self.rect.center = pos
    
    def getx(self):
        return self.pos[0]
    
    def gety(self):
        return self.pos[1]