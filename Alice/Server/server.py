from flask import Flask, request, render_template, url_for, redirect
from Classes.Database.database import Database
from Classes.Session.session import Session
from Classes.Request.Cookies.cookies import Cookies
from Classes.ErrorInterface.Execution.execution import ExecutionError as Error
from .Utils.utils_functions import values, success, failure
import hashlib

app = Flask("Alice")

app.secret_key = b"THESECRETKEYOFOURFLASKAPPLICATIONISRIGHTOVERHERE73747875953933263151256734758392927836"

session = Session()

error_identifier = "[ERREUR - SERVEUR]:"

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
    if not session.get("id"):
            label = "LOGIN"
        # try:
            db = Database()
            if request.method == "GET":
                return render_template("login.html.jinja")
            if request.method == "POST":
                mail, password = values(request.form)
                user = db.select("SELECT * FROM users WHERE mail = ?", (mail,))
                try:
                    id, firstname, lastname, mail, real_password = values(user[0])
                except TypeError: 
                    Error.resolve(error_identifier, label, Error.type, "user")    
                if user[0]:
                    try:
                        print(real_password)
                        print(hashlib.sha256(password.encode("utf-8")).hexdigest())
                        if real_password == hashlib.sha256(password.encode("utf-8")).hexdigest():
                            session.set({"id": id, "firstname": firstname, "lastname": lastname, "mail": mail})
                            favorites = db.select_and_close("SELECT * FROM favorites WHERE id_user = ?", (id,))
                            if len(favorites) != 0:
                                station_codes = []
                                for set in favorites:
                                    station_codes.append(set["station_code"])
                                session.set("favorites", station_codes)
                            return redirect(url_for("favorites"))
                        return failure("Le mot de passe renseigné ne correspond pas")
                    except TypeError: 
                        Error.resolve(error_identifier, label, Error.type, "user")    
                    except Exception as err: 
                        Error.resolve(error_identifier, label, Error.exception, f"{err}")    
                db.close()
                return failure("Aucun utilisateur ne possède l'adresse mail renseignée")
        # except Exception as err: 
        #     Error.resolve(error_identifier, label, Error.exception, f"{err}")
    return redirect(url_for("favorites"))
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if not session.get("id"):
        label = "SIGNUP"
        try:
            db = Database()
            if request.method == "GET":
                return render_template("signup.html.jinja")
            if request.method == "POST":
                firstname, lastname, mail, password = values(request.form)
                user = db.select("SELECT * FROM users WHERE mail = ?", (mail,))
                if user:
                    db.close()
                    return failure(["Un utilisateur possède déjà un espace rattaché à cette adresse mail"])
                password = hashlib.sha256(password.encode("utf-8")).hexdigest()
                db.mutate_and_close("INSERT INTO users (firstname, lastname, mail, password) VALUES (?,?,?,?)", (firstname, lastname, mail, password))
                return success("La création de votre compte utilisateur a réussi")
        except Exception as err: 
            Error.resolve(error_identifier, label, Error.exception, f"{err}")
    else: return redirect(url_for("favorites"))
    
@app.route("/logout")
def logout():
    session.clean()
    return redirect(url_for("guest"))
    
@app.route("/")
def landing():
    return redirect(url_for("guest"))

@app.route("/guest")
def guest():
    # if "id" not in session:
    #     return redirect(url_for("login"))
    db = Database()
    print(db.select_and_close("SELECT * FROM users"))
    return "Guest <a href='logout'>Se déconnecter</a>"
    # return render_template("guest.html.jinja")

@app.route("/favorites")
def favorites():
    if session.get("id"):
        return f"Favorites <a href='logout'>Se déconnecter</a> {session.get("favorites")}"
    return redirect(url_for("login"))     
    # return render_template("favorites.html.jinja")
    
