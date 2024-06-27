import socket   
from .Settings import settings
import pygame

class Socket_server:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.host = host
        self.port = port
    
    def receive(self): 
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Server up!')   
        settings.open_connection = True     
        
        while settings.open_connection:             
            self.conn, addr = self.socket.accept()
            print(f'received connection from {addr}') 
            with self.conn:        
                data = self.conn.recv(128)
                message = data.decode()                           
                settings.last_message = message


class Socket_server_controls:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.host = host
        self.port = port
    
    def receive_controls(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Server up! CONTROLS')  
        self.conn, addr = self.socket.accept()
        #print(f'received connection from {addr}  SIZE BUFFER ') 
        with self.conn:     
            while True:               
                data = self.conn.recv(15)
                control = data.decode()                
                if len(settings.buffer_controls) < settings.max_buffer:
                    settings.buffer_controls.append(control)
                   
    
class Socket_client():
    def __init__(self, host, port, size):
        self.socket = socket.socket()    
        self.host = host
        self.port = port    
        with self.socket:
            self.socket.connect((self.host, self.port+1))
            print(f'sending bytes {size}')
            self.socket.send(str(size).encode())
            
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))
                   
    def send_frame_TCP(self, frame):    
        data_string = pygame.image.tostring(frame, "RGB")
        self.socket.send(data_string)
    
    