import hashlib

def values(dictionnary: dict):
    return tuple(dictionnary.values())

def success(message):
    return {"Statut": "Succès", "Message": message}

def failure(message):
    return {"Statut": "Echec", "Message": message}

def hashing(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()