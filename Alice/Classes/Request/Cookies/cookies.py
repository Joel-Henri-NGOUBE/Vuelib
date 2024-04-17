from flask import make_response, Response
# import flask.Response as Response
from ...ErrorInterface.Execution.execution import ExecutionError as Error

class Cookies:
    
    def __init__(self, request):
        self.request = request
        self.error_identifier = "[ERREUR - CLASSE_COOKIES]:"
        
    def get(self, key: str):
        label = "GET"
        try:
            if isinstance(key, str): return self.request.cookies.get(key)
            else: raise TypeError
        except TypeError:
            Error.resolve(self.error_identifier, label, Error.type, "key")
        except:
            Error.resolve(self.error_identifier, label)
    
    def make(self, key: str, value, response: Response|bool = False) -> Response:
        label = "MAKE"
        if response:
            res = response
        else: 
            res = make_response("Cookie")
        
        try:
            if isinstance(value, int):
                value = str(value)
            if isinstance(key, str): 
                res.set_cookie(key, value)
                return res
            else: raise TypeError
        except TypeError:
            Error.resolve(self.error_identifier, label, Error.type, "key")
    
    def pop(self, key: str):
        label = "POP"
        res = make_response("not_Cookie")
        try:
            if isinstance(key, str): 
                res.delete_cookie(key)
                return res
            else: raise TypeError
        except TypeError:
            Error.resolve(self.error_identifier, label, Error.type, "key")
        except:
            Error.resolve(self.error_identifier, label)
            