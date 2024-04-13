from flask import session

class Session:
    
    def __init__(self):
        self.session = session
        self._error_identifier = "[ERREUR - CLASSE_SESSION]:"
        # self.__secret = ""
       
    def get(self, key: str):
        label = "GET"
        try:
            return self.session[key]
        except TypeError:
            print(f"{self._error_identifier} {label} -  Paramètre 'key' de mauvais type")
        except KeyError:
            print(f"{self._error_identifier} {label} -  Paramètre 'key' introuvable dans la session")
        
    def set(self, key: str, value):
        label = "SET"
        try:
            self.session[key] = value
        except TypeError:
            print(f"{self._error_identifier} {label} -  Paramètre 'key' de mauvais type")
        except KeyError:
            print(f"{self._error_identifier} {label} -  Paramètre 'key' introuvable dans la session")
            
    def pop(self, key: str):
        label = "POP"
        try:
            if isinstance(key, str): self.session.pop(key, None)
            else: raise TypeError
        except TypeError:
            print(f"{self._error_identifier} {label} -  Paramètre 'key' de mauvais type")
        except KeyError:
            print(f"{self._error_identifier} {label} -  Paramètre 'key' introuvable dans la session")




        
        
    