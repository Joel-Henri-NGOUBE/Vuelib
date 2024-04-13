from flask import make_response

class Cookies:
    
    def __init__(self, request):
        self.request = request
        
    def get(self, key: str):
        return self.request.cookies.get(key)
    
    def make(self, key: str, value):
        res = make_response("Cookie")
        res.set_cookie(key, value)
        return res
    
    def pop(self, key: str):
        res = make_response("not_Cookie")
        res.delete_cookie(key)
        return res