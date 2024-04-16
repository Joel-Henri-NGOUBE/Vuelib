from flask import session
from ..ErrorInterface.Execution.execution import ExecutionError as Error

class Session:
    
    def __init__(self):
        self.session = session
        self._error_identifier = "[ERREUR - CLASSE_SESSION]:"
        # self.__secret = ""
       
    def get(self, key: str):
        label = "GET"
        try:
            if isinstance(key, str): 
                if key in self.session:
                    return self.session[key]
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
                # print(key)
                for a_key in key:
                    self.session[a_key] = key[a_key]
            if isinstance(key, str):  self.session[key] = value
            # else: raise Exception
        except Exception as err:
            Error.resolve(self._error_identifier, label, Error.exception, f"{err}")
        # Techniquement inatteignable
        # except KeyError:
        #     Error.resolve(self._error_identifier, label, Error.key, 'key')
            
    def pop(self, key: str):
        label = "POP"
        try:
            if isinstance(key, str): self.session.pop(key, None)
            else: raise TypeError
        except TypeError:
            Error.resolve(self._error_identifier, label, Error.type, 'key')
        except KeyError:
            Error.resolve(self._error_identifier, label, Error.key, 'key')
            
    def clean(self):
        self.session.clear()




        
        
    