import socket, pickle
from .Settings import settings

class Obj:
    def __init__(self, name):
        self.name = name
    def get(self):
        return self.name


class Socket_server:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.host = host
        self.port = port
    
    def receive(self): 
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print('Server up!')        
        
        while settings.open_connection:             
            self.conn, addr = self.socket.accept()
            print(f'received connection from {addr}') 
            with self.conn:        
                data = self.conn.recv(4096)            
                obj = pickle.loads(data)
                print(obj.get())            
                settings.last_message = obj.get()
                settings.last_obj = obj
                
   
    
class Socket_client():
    def __init__(self, host, port):
        self.socket = socket.socket()    
        self.host = host
        self.port = port
                   
    def send_frame(self, frame):    
        print(f'sending to {self.host}:{self.port}')
        self.socket.connect((self.host, self.port))
        with self.socket:            
            #obj = Obj(message)            
            data_string = pickle.dumps(frame)
            self.socket.send(data_string)
    

if __name__ == '__main__':
    s = Socket_server('0.0.0.0', 4040)
    s.receive()
    #s = Socket_client('192.168.0.107', 4040)
    # s.send('hi')
    # s.send('esquerda')
    # s.send('300')
    # s.send('600')
    pass