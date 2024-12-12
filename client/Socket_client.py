import socket
#from .Game import settings
from .Settings import settings

class AppClient:
    def __init__(self, host, port):        
        self.host = host
        self.port = port    
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
            
    def connect_server(self):     
        try: 
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
            self.socket.connect((self.host, self.port))
            self.conn = self.socket
            settings.client_connected = True
        except Exception as E:
            print("Could not connect to server:", E)
        
    def send_message(self, message):
        data_bytes = message.encode()
        if self.conn: self.conn.send(data_bytes)
    
    def receive_messages(self):        
        with self.conn:
            while True:
                try:
                    #receive data
                    data = self.conn.recv(64)
                    message = data.decode()
                    if len(settings.buffer_message) < settings.max_buffer:
                        settings.buffer_message.append(message)                     
                except: break
                    

