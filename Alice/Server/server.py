from flask import Flask, request, render_template, url_for, redirect
from Classes.Database.database import Database
from Classes.Session.session import Session
from Classes.Request.Cookies.cookies import Cookies
from .Utils.utils_functions import values

app = Flask("Alice")

app.secret_key = b"THESECRETKEYOFOURFLASKAPPLICATIONISRIGHTOVERHERE1938734663738292092874"

@app.route("/login", methods=["GET", "POST"])
def login():
    # # Exemple d'instanciaton des classes utiles
    # db = Database()
    # session = Session()
    # cookie = Cookies(request)
    # # Exemple d'utilisation des instances de classe
    # session.set("bonjour", 123)
    # res = cookie.make("bonsoir", 457)
    # # print(res)
    # print(db.select_and_close("SELECT * FROM agence"))
    # print(session.get("bonjour"))
    # print(cookie.get("bonsoir"))
    # return res
    if request.method == "GET":
        return render_template("login.html.jinja")
    if request.method == "POST":
        mail, password = values(request.form)    
        return {"mail": mail, "password": password}
    return "Not a good method"
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html.jinja")
    if request.method == "POST":
        firstname, lastname, mail, password = values(request.form)
        return {"mail": mail, "password": password}
    return "Not a good method"
    
@app.route("/logout")
def logout():
    return 
    
@app.route("/")
def landing():
    return redirect(url_for("login"))
    
