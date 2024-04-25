import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, render_template, url_for, redirect, abort
from Classes.Database.database import Database
from Classes.Session.session import Session
from Classes.Request.Cookies.cookies import Cookies
from Classes.ErrorInterface.Execution.execution import ExecutionError as Error
from Utils.utils_functions import values, hashing, render_error_login, render_error_signup, render_success_signup
import json
from Client.client import retrieve_stations

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
    donnee = '''{
"total_count":1468,
"results":[
{
"stationcode":"16107",
"name":"Benjamin Godard - Victor Hugo",
"is_installed":"OUI",
"capacity":35,
"numdocksavailable":31,
"numbikesavailable":4,
"mechanical":0,
"ebike":4,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:24:11+00:00",
"coordonnees_geo":{
"lon":2.275725,
"lat":48.865983
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"31104",
"name":"Mairie de Rosny-sous-Bois",
"is_installed":"OUI",
"capacity":30,
"numdocksavailable":14,
"numbikesavailable":15,
"mechanical":4,
"ebike":11,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:27:21+00:00",
"coordonnees_geo":{
"lon":2.4865807592869,
"lat":48.871256519012
},
"nom_arrondissement_communes":"Rosny-sous-Bois",
"code_insee_commune":null
},
{
"stationcode":"9020",
"name":"Toudouze - Clauzel",
"is_installed":"OUI",
"capacity":21,
"numdocksavailable":17,
"numbikesavailable":3,
"mechanical":1,
"ebike":2,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:27:29+00:00",
"coordonnees_geo":{
"lon":2.3373600840568547,
"lat":48.87929591733507
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"12109",
"name":"Mairie du 12ème",
"is_installed":"OUI",
"capacity":30,
"numdocksavailable":1,
"numbikesavailable":29,
"mechanical":25,
"ebike":4,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:26:41+00:00",
"coordonnees_geo":{
"lon":2.3875549435616,
"lat":48.840855311763
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"11104",
"name":"Charonne - Robert et Sonia Delaunay",
"is_installed":"OUI",
"capacity":20,
"numdocksavailable":15,
"numbikesavailable":4,
"mechanical":3,
"ebike":1,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:24:48+00:00",
"coordonnees_geo":{
"lon":2.3925706744194,
"lat":48.855907555969
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"8026",
"name":"Messine - Place Du Pérou",
"is_installed":"OUI",
"capacity":12,
"numdocksavailable":10,
"numbikesavailable":2,
"mechanical":1,
"ebike":1,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:27:35+00:00",
"coordonnees_geo":{
"lon":2.315508019010038,
"lat":48.875448033960744
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"13007",
"name":"Le Brun - Gobelins",
"is_installed":"OUI",
"capacity":48,
"numdocksavailable":31,
"numbikesavailable":16,
"mechanical":12,
"ebike":4,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:27:29+00:00",
"coordonnees_geo":{
"lon":2.3534681351338,
"lat":48.835092787824
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"7002",
"name":"Vaneau - Sèvres",
"is_installed":"OUI",
"capacity":35,
"numdocksavailable":10,
"numbikesavailable":25,
"mechanical":20,
"ebike":5,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:26:38+00:00",
"coordonnees_geo":{
"lon":2.3204218259346,
"lat":48.848563233059
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"5110",
"name":"Lacépède - Monge",
"is_installed":"OUI",
"capacity":23,
"numdocksavailable":19,
"numbikesavailable":4,
"mechanical":2,
"ebike":2,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:24:20+00:00",
"coordonnees_geo":{
"lon":2.3519663885235786,
"lat":48.84389286531899
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"42016",
"name":"Pierre et Marie Curie - Maurice Thorez",
"is_installed":"OUI",
"capacity":27,
"numdocksavailable":25,
"numbikesavailable":2,
"mechanical":0,
"ebike":2,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:19:33+00:00",
"coordonnees_geo":{
"lon":2.376804985105991,
"lat":48.81580226360801
},
"nom_arrondissement_communes":"Ivry-sur-Seine",
"code_insee_commune":null
},
{
"stationcode":"6021",
"name":"Beaux-Arts - Bonaparte",
"is_installed":"OUI",
"capacity":20,
"numdocksavailable":4,
"numbikesavailable":16,
"mechanical":16,
"ebike":0,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:22:03+00:00",
"coordonnees_geo":{
"lon":2.334851883351803,
"lat":48.856451985395786
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"25006",
"name":"Place Nelson Mandela",
"is_installed":"OUI",
"capacity":22,
"numdocksavailable":21,
"numbikesavailable":1,
"mechanical":0,
"ebike":1,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:22:53+00:00",
"coordonnees_geo":{
"lon":2.1961666225454,
"lat":48.862453313908
},
"nom_arrondissement_communes":"Rueil-Malmaison",
"code_insee_commune":null
},
{
"stationcode":"30002",
"name":"Jean Rostand - Paul Vaillant Couturier",
"is_installed":"OUI",
"capacity":40,
"numdocksavailable":5,
"numbikesavailable":34,
"mechanical":12,
"ebike":22,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:28:02+00:00",
"coordonnees_geo":{
"lon":2.4530601033354,
"lat":48.908168131015
},
"nom_arrondissement_communes":"Bobigny",
"code_insee_commune":null
},
{
"stationcode":"17038",
"name":"Grande Armée - Brunel",
"is_installed":"OUI",
"capacity":62,
"numdocksavailable":56,
"numbikesavailable":4,
"mechanical":0,
"ebike":4,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:27:49+00:00",
"coordonnees_geo":{
"lon":2.288124,
"lat":48.876116
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"7003",
"name":"Square Boucicaut",
"is_installed":"OUI",
"capacity":60,
"numdocksavailable":9,
"numbikesavailable":51,
"mechanical":39,
"ebike":12,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:27:53+00:00",
"coordonnees_geo":{
"lon":2.325061820447445,
"lat":48.851296433665276
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"8050",
"name":"Boétie - Ponthieu",
"is_installed":"OUI",
"capacity":33,
"numdocksavailable":5,
"numbikesavailable":7,
"mechanical":2,
"ebike":5,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:24:23+00:00",
"coordonnees_geo":{
"lon":2.3076787590981,
"lat":48.871417284355
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"14108",
"name":"Le Brix et Mesmin - Jourdan",
"is_installed":"OUI",
"capacity":21,
"numdocksavailable":21,
"numbikesavailable":0,
"mechanical":0,
"ebike":0,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:24:43+00:00",
"coordonnees_geo":{
"lon":2.327861653302471,
"lat":48.82234096593411
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"31024",
"name":"Romainville - Vaillant-Couturier",
"is_installed":"OUI",
"capacity":38,
"numdocksavailable":33,
"numbikesavailable":2,
"mechanical":0,
"ebike":2,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:27:55+00:00",
"coordonnees_geo":{
"lon":2.446748,
"lat":48.86785
},
"nom_arrondissement_communes":"Montreuil",
"code_insee_commune":null
},
{
"stationcode":"2022",
"name":"Saint-Fiacre - Poissonière",
"is_installed":"OUI",
"capacity":35,
"numdocksavailable":28,
"numbikesavailable":7,
"mechanical":4,
"ebike":3,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:27:15+00:00",
"coordonnees_geo":{
"lon":2.3459213599563,
"lat":48.870828911558
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
},
{
"stationcode":"20143",
"name":"Ramponeau - Belleville",
"is_installed":"OUI",
"capacity":44,
"numdocksavailable":35,
"numbikesavailable":8,
"mechanical":4,
"ebike":4,
"is_renting":"OUI",
"is_returning":"OUI",
"duedate":"2024-04-21T17:26:47+00:00",
"coordonnees_geo":{
"lon":2.379056852114,
"lat":48.871031137596
},
"nom_arrondissement_communes":"Paris",
"code_insee_commune":null
}
]
}'''
    donnee_2 = json.loads(donnee)
    # if "id" not in session:
    #     return redirect(url_for("login"))
    db = Database()
    print(db.select_and_close("SELECT * FROM users"))
    # return "Guest <a href='logout'>Se déconnecter</a>"
    if session.get("id"):
        return render_template("guest.html.jinja", donnee = donnee, logged_in = True)
    return render_template("guest.html.jinja", donnee = donnee, logged_in = False)


@app.route("/favorites")
def favorites():
    if session.get("id"):
        return f"Favorites <a href='logout'>Se déconnecter</a> {session.get("favorites")}"
    return redirect(url_for("login"))     
    # return render_template("favorites.html.jinja")
    
# https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?select=*&where=nom_arrondissement_communes=%22Paris%22&order_by=stationcode%20DESC&limit=100
    
