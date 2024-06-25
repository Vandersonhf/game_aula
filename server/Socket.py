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
                
    
class Socket_client():
    def __init__(self, host, port):
        self.socket = socket.socket()    
        self.host = host
        self.port = port        
                   
    def send_frame_TCP(self, frame):    
        #print(f'sending to {self.host}:{self.port}')
        self.socket.connect((self.host, self.port))
        with self.socket: 
            data_string = pygame.image.tostring(frame, "RGB")
            #print(f'sending bytes {len(data_string)}')
            self.socket.send(data_string)
    
    