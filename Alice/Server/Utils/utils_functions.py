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

# def success(message):
#     return {"Status": "success", "Message": message}

# def failure(message):
#     return {"Status": "failure", "Message": message}

def hashing(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()