from flask import Flask, request, render_template, url_for, redirect, abort
from Classes.Database.database import Database
from Classes.Session.session import Session
from Classes.Request.Cookies.cookies import Cookies
from Classes.ErrorInterface.Execution.execution import ExecutionError as Error
from .Utils.utils_functions import values, hashing, render_error_login, render_error_signup, render_success_signup

app = Flask("Alice")

app.secret_key = b"THESECRETKEYOFOURFLASKAPPLICATIONISRIGHTOVERHERE94246789963759836"

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
        cookies = Cookies(request)
        if request.method == "GET":
            arguments = {
                "mail": cookies.get("mail"),
                "theme": cookies.get("theme"),
                "dark_theme_url": url_for("static", filename="/CSS/dark.css"),
                "light_theme_url": url_for("static", filename="/CSS/light.css"),
                "theme_setter_url": url_for("static", filename="/JavaScript/setTheme.js")
            }
            return render_template("login.html.jinja", **arguments)
        if request.method == "POST":
            form = request.form
            form_length = len(form)
            try:
                if form_length == 3:
                    mail, password, remember = values(form)
                elif form_length == 2:
                    mail, password = values(form)
                else:
                    abort(401)
            except Exception:
                Error.resolve(error_identifier, label, Error.exception, f"{err}")    
            if mail and password:
                user = db.select("SELECT * FROM users WHERE mail = ?", (mail,))
                # try:
                # except TypeError: 
                #     Error.resolve(error_identifier, label, Error.type, "user")    
                if len(user):
                    try:
                        id, firstname, lastname, mail, real_password = values(user[0])
                        if real_password == hashing(password):
                            session.set({"id": id, "firstname": firstname, "lastname": lastname, "mail": mail})
                            favorites = db.select_and_close("SELECT * FROM favorites WHERE id_user = ?", (id,))
                            if len(favorites):
                                station_codes = []
                                for set in favorites:
                                    station_codes.append(set["station_code"])
                                session.set("favorites", station_codes)
                            res = redirect(url_for("favorites"))
                            if not cookies.get("theme"):
                                res = cookies.make("theme", "light", res)
                            if form_length == 3:
                                if remember == "on":
                                    res = cookies.make("mail", str(mail), res)
                            if form_length == 2:
                                if cookies.get("mail"):
                                    cookies.pop("mail", res)
                            return res
                        return render_error_login( "Le mot de passe renseigné ne correspond pas")
                    except Exception as err: 
                        Error.resolve(error_identifier, label, Error.exception, f"{err}")    
                db.close()
                return render_error_login("Aucun utilisateur ne possède l'adresse mail renseignée.")
            return render_error_login("L'un des champs renseignés est vide.")
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
                form = request.form
                form_length = len(form)
                try:
                    if form_length == 4:
                        firstname, lastname, mail, password = values(form)
                    else:
                        abort(401)
                except Exception:
                    Error.resolve(error_identifier, label, Error.exception, f"{err}")
                if firstname and mail and password:
                    user = db.select("SELECT * FROM users WHERE mail = ?", (mail,))
                    if len(user):
                        db.close()
                        return render_error_signup("Un utilisateur possède déjà un espace rattaché à cette adresse mail")
                    password = hashing(password)
                    if not lastname:
                        db.mutate_and_close("INSERT INTO users (firstname, lastname, mail, password) VALUES (?, NULL,?,?)", (firstname, mail, password))
                    else:
                        db.mutate_and_close("INSERT INTO users (firstname, lastname, mail, password) VALUES (?,?,?,?)", (firstname, lastname, mail, password))
                    return render_success_signup("La création de votre compte utilisateur a réussi")
                return render_error_signup("L'un des champs obligatoires est vide")
        except Exception as err: 
            Error.resolve(error_identifier, label, Error.exception, f"{err}")
    return redirect(url_for("favorites"))
    
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
    
