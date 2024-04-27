import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket

class PrimarySocket:
    
    def __init__(self):
        self._socket = socket.socket()
        self.__hostname = socket.gethostname()
        self.__port = 3450
        
    def _get_config_params(self):
        return (self.__hostname, self.__port)
    
        
    
    