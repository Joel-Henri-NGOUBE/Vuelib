from flask import Flask, request, render_template, url_for, redirect, abort,jsonify
from Classes.Database.database import Database
from Classes.Database.Requests.requests import Requests as Req
from Classes.Session.session import Session
from Classes.Request.Cookies.cookies import Cookies
from Classes.ErrorInterface.Execution.execution import ExecutionError as Error
from .Utils.utils_functions import values, hashing, render_error_login, render_error_signup, render_success_signup
import json

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


@app.route("/profile")
def profile():
    if session.get("id"):
        user_data = {
            "id": session.get("id"),
            "firstname": session.get("firstname"),
            "lastname": session.get("lastname"),
            "mail": session.get("mail")
        }
        return render_template("profile.html.jinja", user=user_data)
    return redirect(url_for("login"))

# @app.route("/favorites")
# def favorites():
#     if session.get("id"):
#         return f"Favorites <a href='logout'>Se déconnecter</a>"
#     return redirect(url_for("login"))     
#     # return render_template("favorites.html.jinja")

    
@app.route("/favorites")
def favorites():
    if session.get("id"):
       data= '''
{

    "total_count":1468,
    "results":[
        {
            "stationcode":"31104",
            "name":"Mairie de Rosny-sous-Bois",
            "is_installed":"OUI",
            "capacity":30,
            "numdocksavailable":13,
            "numbikesavailable":17,
            "mechanical":5,
            "ebike":12,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:23:33+00:00",
            "coordonnees_geo":{
                "lon":2.4865807592869,
                "lat":48.871256519012
            }
            ,
            "nom_arrondissement_communes":"Rosny-sous-Bois",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"9020",
            "name":"Toudouze - Clauzel",
            "is_installed":"OUI",
            "capacity":21,
            "numdocksavailable":17,
            "numbikesavailable":3,
            "mechanical":0,
            "ebike":3,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:28:58+00:00",
            "coordonnees_geo":{
                "lon":2.3373600840568547,
                "lat":48.87929591733507
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"12109",
            "name":"Mairie du 12ème",
            "is_installed":"OUI",
            "capacity":30,
            "numdocksavailable":23,
            "numbikesavailable":6,
            "mechanical":4,
            "ebike":2,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:28:29+00:00",
            "coordonnees_geo":{
                "lon":2.3875549435616,
                "lat":48.840855311763
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"14014",
            "name":"Jourdan - Stade Charléty",
            "is_installed":"OUI",
            "capacity":60,
            "numdocksavailable":53,
            "numbikesavailable":4,
            "mechanical":1,
            "ebike":3,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:27:23+00:00",
            "coordonnees_geo":{
                "lon":2.3433353751898,
                "lat":48.819428333369
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"32017",
            "name":"Basilique",
            "is_installed":"OUI",
            "capacity":22,
            "numdocksavailable":19,
            "numbikesavailable":2,
            "mechanical":1,
            "ebike":1,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:24:07+00:00",
            "coordonnees_geo":{
                "lon":2.3588666820200914,
                "lat":48.93626891059109
            }
            ,
            "nom_arrondissement_communes":"Saint-Denis",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"11104",
            "name":"Charonne - Robert et Sonia Delaunay",
            "is_installed":"OUI",
            "capacity":20,
            "numdocksavailable":20,
            "numbikesavailable":0,
            "mechanical":0,
            "ebike":0,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:26:59+00:00",
            "coordonnees_geo":{
                "lon":2.3925706744194,
                "lat":48.855907555969
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"6003",
            "name":"Saint-Sulpice",
            "is_installed":"OUI",
            "capacity":21,
            "numdocksavailable":3,
            "numbikesavailable":18,
            "mechanical":9,
            "ebike":9,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:26:26+00:00",
            "coordonnees_geo":{
                "lon":2.3308077827095985,
                "lat":48.85165383178419
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"5110",
            "name":"Lacépède - Monge",
            "is_installed":"OUI",
            "capacity":23,
            "numdocksavailable":0,
            "numbikesavailable":23,
            "mechanical":13,
            "ebike":10,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:26:57+00:00",
            "coordonnees_geo":{
                "lon":2.3519663885235786,
                "lat":48.84389286531899
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"33006",
            "name":"André Karman - République",
            "is_installed":"OUI",
            "capacity":31,
            "numdocksavailable":26,
            "numbikesavailable":3,
            "mechanical":2,
            "ebike":1,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:27:33+00:00",
            "coordonnees_geo":{
                "lon":2.3851355910301213,
                "lat":48.91039875761846
            }
            ,
            "nom_arrondissement_communes":"Aubervilliers",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"42016",
            "name":"Pierre et Marie Curie - Maurice Thorez",
            "is_installed":"OUI",
            "capacity":27,
            "numdocksavailable":26,
            "numbikesavailable":1,
            "mechanical":0,
            "ebike":1,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:19:39+00:00",
            "coordonnees_geo":{
                "lon":2.376804985105991,
                "lat":48.81580226360801
            }
            ,
            "nom_arrondissement_communes":"Ivry-sur-Seine",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"6021",
            "name":"Beaux-Arts - Bonaparte",
            "is_installed":"OUI",
            "capacity":20,
            "numdocksavailable":2,
            "numbikesavailable":18,
            "mechanical":15,
            "ebike":3,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:25:39+00:00",
            "coordonnees_geo":{
                "lon":2.334851883351803,
                "lat":48.856451985395786
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"17038",
            "name":"Grande Armée - Brunel",
            "is_installed":"OUI",
            "capacity":62,
            "numdocksavailable":36,
            "numbikesavailable":24,
            "mechanical":0,
            "ebike":24,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:29:02+00:00",
            "coordonnees_geo":{
                "lon":2.288124,
                "lat":48.876116
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"17026",
            "name":"Jouffroy d'Abbans - Wagram",
            "is_installed":"OUI",
            "capacity":40,
            "numdocksavailable":35,
            "numbikesavailable":3,
            "mechanical":0,
            "ebike":3,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:21:33+00:00",
            "coordonnees_geo":{
                "lon":2.301132157445,
                "lat":48.881973298352
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"5016",
            "name":"Thouin - Cardinal Lemoine",
            "is_installed":"OUI",
            "capacity":17,
            "numdocksavailable":0,
            "numbikesavailable":15,
            "mechanical":0,
            "ebike":15,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:28:41+00:00",
            "coordonnees_geo":{
                "lon":2.3494647851273465,
                "lat":48.84504716661511
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"11025",
            "name":"Froment - Bréguet",
            "is_installed":"OUI",
            "capacity":43,
            "numdocksavailable":3,
            "numbikesavailable":39,
            "mechanical":30,
            "ebike":9,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:27:28+00:00",
            "coordonnees_geo":{
                "lon":2.37289470306807,
                "lat":48.8570414504784
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"15047",
            "name":"Morillons - Dantzig",
            "is_installed":"OUI",
            "capacity":52,
            "numdocksavailable":47,
            "numbikesavailable":5,
            "mechanical":3,
            "ebike":2,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:28:14+00:00",
            "coordonnees_geo":{
                "lon":2.299380004405976,
                "lat":48.83310149953933
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
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
            "duedate":"2024-04-22T14:27:23+00:00",
            "coordonnees_geo":{
                "lon":2.446748,
                "lat":48.86785
            }
            ,
            "nom_arrondissement_communes":"Montreuil",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"17044",
            "name":"Porte de Saint-Ouen - Bessières",
            "is_installed":"OUI",
            "capacity":42,
            "numdocksavailable":27,
            "numbikesavailable":2,
            "mechanical":1,
            "ebike":1,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:28:10+00:00",
            "coordonnees_geo":{
                "lon":2.32851451022192,
                "lat":48.89792240854517
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"17025",
            "name":"Chazelles - Courcelles",
            "is_installed":"OUI",
            "capacity":35,
            "numdocksavailable":34,
            "numbikesavailable":1,
            "mechanical":1,
            "ebike":0,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:27:59+00:00",
            "coordonnees_geo":{
                "lon":2.3034455627202988,
                "lat":48.879406604954
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
        ,
        {
            "stationcode":"20143",
            "name":"Ramponeau - Belleville",
            "is_installed":"OUI",
            "capacity":44,
            "numdocksavailable":43,
            "numbikesavailable":0,
            "mechanical":0,
            "ebike":0,
            "is_renting":"OUI",
            "is_returning":"OUI",
            "duedate":"2024-04-22T14:27:35+00:00",
            "coordonnees_geo":{
                "lon":2.379056852114,
                "lat":48.871031137596
            }
            ,
            "nom_arrondissement_communes":"Paris",
            "code_insee_commune":null
        }
    ]

}

'''
       data = json.loads(data)
       favorite_stations = Req.get_favorite_stations(session.get("id"))
       return render_template('favorites.html.jinja', favorite_stations=favorite_stations,data= data)
    return redirect(url_for("login"))


# Création d'une station favorite
@app.route('/favorites', methods=['POST'])
def add_favorite():
    data = request.json
    favorite_stations = Req.get_favorite_stations(session.get("id"))  
    favorite_stations.append(data)  
    # return jsonify({'message': 'Station favorite ajoutée avec succès'}), 201
    return redirect(url_for('favoris'))

# Page d'affichage des favoris
@app.route('/favoris')
def favoris():
    return render_template('favoris.html.jinja')

# Modification d'une station favorite
@app.route('/favorites/<int:station_id>', methods=['PUT'])
def update_favorite(station_id):
    data = request.json
    favorite_stations = Req.get_favorite_stations(session.get("id"))
    for station in favorite_stations:
        if station.get('stationcode') == station_id:
            station.update(data) 
            return jsonify({'message': 'Station favorite mise à jour avec succès'}), 200
    return jsonify({'error': 'Station favorite non trouvée'}), 404

# Suppression d'une station favorite
@app.route('/favorites/<int:station_id>', methods=['DELETE'])
def delete_favorite(station_id):
    favorite_stations = Req.get_favorite_stations(session.get("id"))
    for station in favorite_stations:
        if station.get('stationcode') == station_id:
            favorite_stations.remove(station)  
            return jsonify({'message': 'Station favorite supprimée avec succès'}), 200
    return jsonify({'error': 'Station favorite non trouvée'}), 404
