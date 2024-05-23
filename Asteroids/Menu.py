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

    img = Image.open('images/ship.png')
    b1 = CTkButton(master=frame, text=lab2, corner_radius=30, fg_color='transparent',
                border_width=2, image=CTkImage(dark_image=img, light_image=img), command=back_bt)
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

    img = Image.open('images/ship.png')
    b1 = CTkButton(master=frame, text='START', corner_radius=30, fg_color='transparent',
                hover_color='#666666', border_width=2, bg_color='transparent',
                image=CTkImage(dark_image=img, light_image=img), command=back_bt)
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