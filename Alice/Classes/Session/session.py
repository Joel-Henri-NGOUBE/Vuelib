from flask import session
from ..ErrorInterface.Execution.execution import ExecutionError as Error

class Session:
    
    def __init__(self):
        self._session = session
        self._error_identifier = "[ERREUR - CLASSE_SESSION]:"
       
    def get(self, key: str):
        label = "GET"
        try:
            if isinstance(key, str): 
                if key in self._session:
                    return self._session[key]
                return False
            else: raise TypeError
        except TypeError:
            Error.resolve(self._error_identifier, label, Error.type, 'key')
        except KeyError:
            Error.resolve(self._error_identifier, label, Error.key, 'key')
        
    def set(self, key: str|dict, value = None):
        label = "SET"
        try:
            if isinstance(key, dict):
                for a_key in key:
                    self._session[a_key] = key[a_key]
            if isinstance(key, str):  self._session[key] = value
        except Exception as err:
            Error.resolve(self._error_identifier, label, Error.exception, f"{err}")
            
    def pop(self, key: str):
        label = "POP"
        try:
            if isinstance(key, str): self._session.pop(key, None)
            else: raise TypeError
        except TypeError:
            Error.resolve(self._error_identifier, label, Error.type, 'key')
        except KeyError:
            Error.resolve(self._error_identifier, label, Error.key, 'key')
            
    def clean(self):
        self._session.clear()




        
        
    