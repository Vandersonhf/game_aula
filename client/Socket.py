import socket 
from .Settings import settings
import pygame

class Socket_server:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP 
        self.host = host
        self.port = port
    
    def receive_frame_TCP(self): 
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)  #TCP
        print('Server up!')   
        settings.open_connection2 = True            
        
        while settings.open_connection2: 
            self.conn, addr = self.socket.accept()     #TCP
            #print(f'received connection from {addr}') 
            with self.conn:        
                received = []
                # loop .recv, it returns empty string when done, then transmitted data is completely received
                while True:
                    recvd_data = self.conn.recv(262144) # chunks of 262,144
                    if not recvd_data:
                        break
                    else:
                        received.append(recvd_data)
                                
                dataset = bytes().join(received)
                
                #print(f'getting bytes {len(dataset)} and {settings.disp_size}')
                settings.frame = pygame.image.fromstring(dataset,settings.disp_size,"RGB")
                #print(f'client size {settings.frame.get_size()}')
                
                if len(settings.frame_list) < settings.max_buffer:
                    settings.frame_list.append(settings.frame)
                   
    
class Socket_client():
    def __init__(self, host, port):
        self.socket = socket.socket()    
        self.host = host
        self.port = port
    
    def send(self, message):    
        print(f'sending to {self.host}:{self.port}')
        self.socket.connect((self.host, self.port))
        with self.socket: 
            data_string = message.encode()
            self.socket.send(data_string)
     
