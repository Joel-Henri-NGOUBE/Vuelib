import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, render_template, url_for, redirect, abort
from Classes.Database.database import Database
from Classes.Database.Requests.requests import Requests as Req
from Classes.Session.session import Session
from Classes.Request.Cookies.cookies import Cookies
from Classes.ErrorInterface.Execution.execution import ExecutionError as Error
from Utils.utils_functions import values, hashing, render_error_login, render_error_signup, render_success_signup, render_success_favorites, render_error_favorites, filtering, mapping
import json
from Client.client import retrieve_stations

app = Flask("Alice")

app.secret_key = b"THESECRETKEYOFOURFLASKAPPLICATIONISRIGHTOVERHERE94246789963736"

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
            except IndexError:
                Error.resolve(error_identifier, label, Error.index, f"{err}")
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
                            station_codes = []
                            if len(favorites):
                                for set in favorites:
                                    station_codes.append(set["station_code"])
                            session.set("favorites", station_codes)
                            print(session.get("favorites"))
                            res = redirect(url_for("profile"))
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
    return redirect(url_for("profile"))
    
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
                except IndexError:
                    Error.resolve(error_identifier, label, Error.index, f"{err}")
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
    return redirect(url_for("profile"))
    
@app.route("/logout")
def logout():
    session.clean()
    return redirect(url_for("guest"))
    
@app.route("/")
def landing():
    return redirect(url_for("guest"))

@app.route("/guest")
def guest():
    donnee, data_string = retrieve_stations()
    # print(donnee["results"][-1])
    arguments = {
        "donnee": donnee,
        "data_string": data_string,
        "max_number_stations": len(donnee["results"])
    }
    # db = Database()
    if session.get("id"):
        favorites = session.get("favorites")
        arguments["donnee"]["results"] = mapping(lambda s: {**s, "favorite": True} if int(s["stationcode"]) in tuple(favorites) else {**s, "favorite": False}, donnee["results"])
        return render_template("guest.html.jinja", **arguments , logged_in = True)
    return render_template("guest.html.jinja", **arguments , logged_in = False)


@app.route("/profile")
def profile():
    id = session.get("id")
    if id:
        donnee, _ = retrieve_stations()
        favorites = session.get("favorites")
        favorite_stations = filtering(lambda s: int(s["stationcode"]) in tuple(favorites), donnee["results"])
        print(favorite_stations)
        arguments = {
            "firstname": session.get("firstname"),
            "lastname": session.get("lastname"),
            "mail": session.get("mail"),
            "favorite_stations": favorite_stations
        }
        # if len(favorites)
        # return f"Favorites <a href='logout'>Se déconnecter</a> {session.get("favorites")}"
        return render_template("profile.html.jinja", **arguments)
    return redirect(url_for("login"))  
    # return render_template("profile.html.jinja")
    
@app.post("/favorites")
def favorites():
    id = session.get("id")
    if id:
        favorites: list = session.get("favorites")
        action, station_code = values(request.json)
        station_code = int(station_code)
        if action == "add":
            Req.add_favorite_station(id, station_code)
            favorites.append(station_code)
            session.set("favorites", favorites)
            print(session.get("favorites"))
            return render_success_favorites("Favorite successfully added")
        if action == "remove":
            Req.remove_favorite_station(id, station_code)
            session.set("favorites", filtering(lambda sc: sc != station_code, favorites))
            return render_success_favorites("Favorite successfully remove")
    return redirect(url_for("login"))
        
