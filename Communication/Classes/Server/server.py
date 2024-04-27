import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Connection.primary_socket import PrimarySocket

class Server(PrimarySocket):
    
    def __init__(self):
        super().__init__()
        self._socket.bind(self._get_config_params())
        self._socket.listen(5)
  
        
    def wait_connection(self):
        self.client, self.adress = self._socket.accept()
        
    def dispatch(self, message: str):
        self.client.send(message.encode())
        self.client.close()
        