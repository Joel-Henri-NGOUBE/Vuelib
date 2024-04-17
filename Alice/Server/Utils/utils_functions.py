import hashlib

def values(dictionnary: dict):
    return tuple(dictionnary.values())

def success(message):
    return {"Status": "success", "Message": message}

def failure(message):
    return {"Status": "failure", "Message": message}

def hashing(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()