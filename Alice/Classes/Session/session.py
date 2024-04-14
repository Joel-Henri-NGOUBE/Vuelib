from flask import session
from ..ErrorInterface.interface import ErrorInterface as Error

class Session:
    
    def __init__(self):
        self.session = session
        self._error_identifier = "[ERREUR - CLASSE_SESSION]:"
        # self.__secret = ""
       
    def get(self, key: str):
        label = "GET"
        try:
            if isinstance(key, str): return self.session[key]
            else: raise TypeError
        except TypeError:
            Error.resolve(self._error_identifier, label, Error.type, 'key')
        except KeyError:
            Error.resolve(self._error_identifier, label, Error.key, 'key')
        
    def set(self, key: str, value):
        label = "SET"
        try:
            if isinstance(key, str):  self.session[key] = value
            else: raise TypeError
        except TypeError:
            Error.resolve(self._error_identifier, label, Error.type, 'key')
        # Techniquement inatteignable
        except KeyError:
            Error.resolve(self._error_identifier, label, Error.key, 'key')
            
    def pop(self, key: str):
        label = "POP"
        try:
            if isinstance(key, str): self.session.pop(key, None)
            else: raise TypeError
        except TypeError:
            Error.resolve(self._error_identifier, label, Error.type, 'key')
        except KeyError:
            Error.resolve(self._error_identifier, label, Error.key, 'key')




        
        
    