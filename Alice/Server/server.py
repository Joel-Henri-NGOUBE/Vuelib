import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, render_template, url_for, redirect, abort
from Classes.Database.database import Database
from Classes.Database.Requests.requests import Requests as Req
from Classes.Session.session import Session
from Classes.Request.Cookies.cookies import Cookies
from Classes.ErrorInterface.Execution.execution import ExecutionError as Error
from Utils.utils_functions import values, hashing, render_error_login, render_error_signup, render_success_signup, render_success_favorites, render_error_favorites, filtering, mapping, add_title
import json
from Client.client import retrieve_stations

app = Flask("Alice")

app.secret_key = b"THESECRETKEYOFOURFLASKAPPLICATIONISRIGHTOVERHERE94246789963736"

session = Session()

error_identifier = "[ERREUR - SERVEUR]:"

dark_mode = True

@app.route("/login", methods=["GET", "POST"])
def login():
    if not session.get("id"):
        label = "LOGIN"
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
            # Récupérer les données de formulaire
            try:
                if form_length == 3:
                    mail, password, remember = values(form)
                elif form_length == 2:
                    mail, password = values(form)
                else:
                    abort(400)
            except IndexError:
                Error.resolve(error_identifier, label, Error.index, "form")
            except Exception:
                Error.resolve(error_identifier, label, Error.exception, f"{err}")    
            if mail and password:
                user = db.select("SELECT * FROM users WHERE mail = ?", (mail,))   
                if len(user):
                    try:
                        id, firstname, lastname, mail, real_password = values(user[0])
                        if real_password == hashing(password):
                            # Récupérer les favoris associés à l'utilisateur et lui créer une session
                            session.set({"id": id, "firstname": firstname, "lastname": lastname, "mail": mail})
                            favorites = db.select_and_close("SELECT * FROM favorites WHERE id_user = ?", (id,))
                            station_codes = []
                            if len(favorites):
                                for set in favorites:
                                    station_codes.append(set["station_code"])
                            # Ajouter les favoris dans la session
                            session.set("favorites", station_codes)
                            res = redirect(url_for("profile"))
                            # Identifier le thème actuel et le mail de l'utilisateur
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
            cookies = Cookies(request)
            if request.method == "GET":
                return render_template("signup.html.jinja", theme = cookies.get("theme"))
            
            if request.method == "POST":
                # Récupérer les données de formulaires
                form = request.form
                form_length = len(form)
                try:
                    if form_length == 4:
                        firstname, lastname, mail, password = values(form)
                    else:
                        abort(400)
                except IndexError:
                    Error.resolve(error_identifier, label, Error.index, "form")
                except Exception:
                    Error.resolve(error_identifier, label, Error.exception, f"{err}")
                if firstname and mail and password:
                    user = db.select("SELECT * FROM users WHERE mail = ?", (mail,))
                    if len(user):
                        db.close()
                        return render_error_signup("Un utilisateur possède déjà un espace rattaché à cette adresse mail")
                    password = hashing(password)
                    # Créer un nouvel utilisateur
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
    cookies = Cookies(request)
    label = "GUEST"
    try:
        # Récupérer les données de l'API
        donnee, data_string = retrieve_stations()
        arguments = {
            "donnee": donnee,
            "data_string": data_string,
            "max_number_stations": len(donnee["results"]),
            "theme": cookies.get("theme"),
            "dark_theme_url": url_for("static", filename="/CSS/dark.css"),
            "light_theme_url": url_for("static", filename="/CSS/light.css"),
            "theme_setter_url": url_for("static", filename="/JavaScript/setTheme.js")        
            }
        if session.get("id"):
            favorites = session.get("favorites")
            # Ajouter une clé qui permet d'identifier les favoris
            arguments["donnee"]["results"] = mapping(lambda s: {**s, "favorite": True} if int(s["stationcode"]) in tuple(favorites) else {**s, "favorite": False}, donnee["results"])
            return render_template("guest.html.jinja", **arguments , logged_in = True)
        return render_template("guest.html.jinja", **arguments , logged_in = False)
    
    except Exception as e:
        Error.resolve(error_identifier, label, Error.exception, f"{e}")


@app.route("/profile")

def profile():
    label = "PROFILE"
    try:
        id = session.get("id")
        cookies = Cookies(request)
        if id:
            # Récupérer les données de l'API
            donnee, _ = retrieve_stations()
            station_codes = session.get("favorites")
            # Ne garder que les stations favorites sur le profil
            favorite_stations = filtering(lambda s: int(s["stationcode"]) in tuple(station_codes), donnee["results"])
            favorites = Req.get_favorite_station(id)
            # Ajouter le titre de la station si elle en a un à la variable qui contient les stations favorites
            favorites = mapping(lambda s: add_title(s), favorites)
            for station in favorite_stations:
                for favorite in favorites:
                    if int(station["stationcode"]) == int(favorite["station_code"]):
                        station["title"] = favorite[f"{favorite["station_code"]}"]
                        print(f"{station["title"]} = {favorite[f"{favorite["station_code"]}"]}")
            arguments = {
                "firstname": session.get("firstname"),
                "lastname": session.get("lastname"),
                "mail": session.get("mail"),
                "favorite_stations": favorite_stations,
                "theme": cookies.get("theme"),
                "dark_theme_url": url_for("static", filename="/CSS/dark.css"),
                "light_theme_url": url_for("static", filename="/CSS/light.css"),
                "theme_setter_url": url_for("static", filename="/JavaScript/setTheme.js")
            }
            return render_template("profile.html.jinja", **arguments)
        return redirect(url_for("login"))
    except Exception as e:
        Error.resolve(error_identifier, label, Error.exception, f"{e}")
    
@app.post("/favorites")
def favorites():
    label = "FAVORITES"
    id = session.get("id")
    if id:
        favorites: list = session.get("favorites")
        print(request.content_type)
        try:
            # Identifier le type du contenu de la requête
            if request.content_type == "application/json":
                payload = request.json
                payload_length = len(payload)
                print(payload_length)
                if payload_length:
                    if payload_length == 2:
                        action, station_code = values(payload)
                else: abort(400)
            if request.content_type == "application/x-www-form-urlencoded":
                form = request.form
                form_length = len(form)
                print(form_length)
                if form_length:
                    if form_length == 2:
                        title, station_code = values(form)
                        action = ""
                else: abort(400)
            else: abort(405)   

            if station_code:
                station_code = int(station_code)
                # Effectuer la bonne action en fonctionde l'action du payload
                if action == "add":
                    Req.add_favorite_station(id, station_code)
                    favorites.append(station_code)
                    session.set("favorites", favorites)
                    print(session.get("favorites"))
                    return render_success_favorites("Favorite successfully added")
                if action == "remove":
                    Req.remove_favorite_station(id, station_code)
                    session.set("favorites", filtering(lambda sc: sc != station_code, favorites))
                    return render_success_favorites("Favorite successfully removed")
                # Ajouter le titre s'il s'agit d'un formulaire
                Req.update_favorite_station(title, id, station_code)
                return redirect(url_for("profile"))
        except Exception as e:
            Error.resolve(error_identifier, label, Error.exception, f"{e}")
    return redirect(url_for("login"))
        
