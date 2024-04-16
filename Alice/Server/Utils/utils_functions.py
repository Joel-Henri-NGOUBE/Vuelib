def values(dict: dict):
    return tuple(dict.values())

def success(message):
    return {"Statut": "Succès", "Message": message}

def failure(message):
    return {"Statut": "Echec", "Message": message}