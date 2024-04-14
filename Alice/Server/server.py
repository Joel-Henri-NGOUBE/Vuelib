from flask import Flask
from Classes.Database.database import Database

app = Flask("Alice")

@app.route("/")
def login():
    db = Database()
    # Exemple utilisation de la base de données
    print(db.select_and_close("SELECT * FROM agence"))
    return "Bonjour"
# class User:
#     def __init__(self, firstname, lastname, mail):
#         self.firstname = firstname
#         self.lastname = lastname
#         self.mail = mail
    
#     def log_in(self, password, id):
#         # comparer le mot de passe et ajouter l'id à la session
#         pass
    
#     def sign_up(self, password):
#         pass