import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Connection.primary_socket import PrimarySocket

class Client(PrimarySocket):
    
    def __init__(self):
        super().__init__()
        self._socket.connect(self._get_config_params())
        self.max_length = 10000
        
    def get_message(self):
        return self._socket.recv(self.max_length).decode()
        
    def get_protocol_modalities(self, message: str):
        length, result = message.split("\n\n", 1)
        return (length, result)
    
    def close(self):
        self._socket.close()