import mariadb
from ..ErrorInterface.interface import ErrorInterface as Error

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "vuelib"
}

class Database:
    
    def __init__(self):       
        self.connexion = mariadb.connect(**config)
        self.curseur = self.connexion.cursor()
        self.error_identifier = "[ERREUR - CLASSE_DATABASE]:"
    
    def _close_connection(self):
        """
            This method is called to close both the connexion and his cursor.
        """
        self.curseur.close()
        self.connexion.close()
        
    def _check_params(self, sql_request: str, params: tuple|None = None):
        if params is None: self.curseur.execute(sql_request)
        else: self.curseur.execute(sql_request, params)
        
    def select(self, sql_request: str, params: tuple|None = None):
        """
            Select must be used to retrieve some data from the database.    
        """
        label = "SELECT"
        try:
            self._check_params(sql_request, params)
            return self.curseur.fetchall()
        except: Error.resolve(self.error_identifier, label)
            
    
    def select_and_close(self, sql_request: str, params: tuple|None = None):
        """
            Select must be used to retrieve some data from the database and closes the connexion to it.   
        """
        label = "SELECT_AND_CLOSE"
        try:
            self._check_params(sql_request, params)
            result = self.curseur.fetchall()
            self._close_connection()
            return result
        except: Error.resolve(self.error_identifier, label)
    
    def mutate(self, sql_request: str, params: tuple|None = None):
        """
            Mutate must be used to do operations such as updations, insertions or deletions on the database.       
        """
        label = "MUTATE"
        try:
            self._check_params(sql_request, params) 
            self.connexion.commit()
        except: Error.resolve(self.error_identifier, label)
        
    def mutate_and_close(self, sql_request: str, params: tuple|None = None):
        """
            Mutate must be used to do operations such as updations, insertions or deletions on the database and closes the connexion to it.     
        """
        label = "MUTATE_AND_CLOSE"
        try:
            self.mutate(sql_request, params)
            self._close_connection()
        except: Error.resolve(self.error_identifier, label)



