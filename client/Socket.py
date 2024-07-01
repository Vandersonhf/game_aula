import socket 
from .Settings import settings
import pygame
'''
class Socket_server:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP 
        self.host = host
        self.port = port
        
    def receive_buffer_size(self):
        self.socket.bind((self.host, self.port+1))
        self.socket.listen(1)
        print('Server up! SIZE BUFFER')  
        self.conn, addr = self.socket.accept()
        print(f'received connection from {addr}  SIZE BUFFER ') 
        with self.conn:        
            data = self.conn.recv(128)
            size = int(data.decode())
            settings.TCP_buffer = size
            print(f'GOT SIZE {size}')
    
    def receive_frame_TCP(self): 
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)  #TCP
        #print('Server up! TCP frame')   
        self.conn, addr = self.socket.accept()     #TCP
        #print(f'received connection from {addr}')
        settings.open_connection2 = True    
        
        with self.conn:           
            while settings.open_connection2: 
                sum = 0
                received = []                
                if settings.TCP_buffer and len(settings.frame_list) < settings.max_buffer:
                    while sum < settings.TCP_buffer:
                        if settings.TCP_buffer > sum:
                            if settings.TCP_buffer < (sum + settings.frame_segment):
                                recvd_data = self.conn.recv(settings.TCP_buffer - sum)
                            else: 
                                recvd_data = self.conn.recv(settings.frame_segment)
                            sum += len(recvd_data)
                            received.append(recvd_data)
                            #print(f'buffer {sum} and {settings.TCP_buffer}')  
                    if sum == settings.TCP_buffer:
                        dataset = bytes().join(received)
                        settings.frame = pygame.image.fromstring(dataset,settings.disp_size,"RGB")                               
                        settings.frame_list.append(settings.frame)
'''                    
                                                  
    
class Socket_client():
    def __init__(self, host, port):
        self.socket = socket.socket()    
        self.host = host
        self.port = port
    
    def send(self, message):    
        #print(f'sending to {self.host}:{self.port}')
        self.socket.connect((self.host, self.port))
        with self.socket: 
            data_string = message.encode()
            self.socket.send(data_string)
     
'''     
class Socket_client_controls():
    def __init__(self, host, port):
        self.socket = socket.socket()    
        self.host = host
        self.port = port 
        self.socket.connect((self.host, self.port))
    
    def send(self, message):  
        data_string = message.encode()
        self.socket.send(data_string)
'''        
        
class Socket_client_message():
    def __init__(self, host, port):
        self.socket = socket.socket()
        self.socket.connect((host, port))
                   
    def send_message(self, message):    
       data_string = message.encode()
       self.socket.send(data_string)
       

class Socket_server_message:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.socket.bind((host, port))
        self.socket.listen(1)
        print('Server up!')   
        self.conn, addr = self.socket.accept()
        settings.open_connection = True 
    
    def receive_messages(self):
        with self.conn: 
            while settings.open_connection: 
                data = self.conn.recv(64)
                message = data.decode()  
                if len(settings.buffer_message) < settings.max_buffer:
                    settings.buffer_message.append(message) 