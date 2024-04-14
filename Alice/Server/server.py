from flask import Flask, request
from Classes.Database.database import Database
from Classes.Session.session import Session
from Classes.Request.Cookies.cookies import Cookies

app = Flask("Alice")

app.secret_key = b"THESECRETKEYOFOURFLASKAPPLICATIONISRIGHTOVERHERE1938734663738292092874"

@app.route("/")
def login():
    # Exemple d'instanciaton des classes utiles
    db = Database()
    session = Session()
    cookie = Cookies(request)
    # Exemple d'utilisation des instances de classe
    session.set("bonjour", 123)
    res = cookie.make("bonsoir", 457)
    # print(res)
    print(db.select_and_close("SELECT * FROM agence"))
    print(session.get("bonjour"))
    print(cookie.get("bonsoir"))
    return res
