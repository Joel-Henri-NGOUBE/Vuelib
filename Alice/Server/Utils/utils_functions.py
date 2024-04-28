import hashlib
from flask import render_template

def values(dictionnary: dict):
    return tuple(dictionnary.values())

def render_error_login(error):
    return render_template("login.html.jinja", error = error)

def render_error_signup(error):
    return render_template("signup.html.jinja", error = error)

def render_success_signup(message):
    return render_template("signup.html.jinja", message = message)

def render_success_favorites(message):
    return {"Status": "success", "Message": message}

def render_error_favorites(error):
    return {"Status": "failure", "Message": error}

def hashing(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def filtering(lamba_function, to_filter: list):
    return list(filter(lamba_function, to_filter))

def mapping(lamba_function, to_filter: list):
    return list(map(lamba_function, to_filter))

def add_title(station):
    station[f"{station["station_code"]}"] = station["title"]
    return station