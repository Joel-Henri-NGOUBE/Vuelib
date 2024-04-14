import mariadb
from ..ErrorInterface.interface import ErrorInterface as Error

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "immobilier"
}

class Database:
    
    def __init__(self):       
        self._connexion = mariadb.connect(**config)
        self._curseur = self._connexion.cursor()
        self._error_identifier = "[ERREUR - CLASSE_DATABASE]:"
    
    def _close_connection(self):
        """
            This method is called to close both the connexion and his cursor.
        """
        self._curseur.close()
        self._connexion.close()
        
    def _check_params(self, sql_request: str, params: tuple|None = None):
        if params is None: self._curseur.execute(sql_request)
        else: self._curseur.execute(sql_request, params)
        
    def select(self, sql_request: str, params: tuple|None = None):
        """
            Select must be used to retrieve some data from the database.    
        """
        label = "SELECT"
        try:
            self._check_params(sql_request, params)
            return self._curseur.fetchall()
        except: Error.resolve(self._error_identifier, label)
            
    
    def select_and_close(self, sql_request: str, params: tuple|None = None):
        """
            Select_and_close must be used to retrieve some data from the database and closes the connexion to it.   
        """
        label = "SELECT_AND_CLOSE"
        try:
            self._check_params(sql_request, params)
            result = self._curseur.fetchall()
            self._close_connection()
            return result
        except: Error.resolve(self._error_identifier, label)
    
    def mutate(self, sql_request: str, params: tuple|None = None):
        """
            Mutate must be used to do operations such as updations, insertions or deletions on the database.       
        """
        label = "MUTATE"
        try:
            self._check_params(sql_request, params) 
            self._connexion.commit()
        except: Error.resolve(self._error_identifier, label)
        
    def mutate_and_close(self, sql_request: str, params: tuple|None = None):
        """
            Mutate_and_close must be used to do operations such as updations, insertions or deletions on the database and closes the connexion to it.     
        """
        label = "MUTATE_AND_CLOSE"
        try:
            self.mutate(sql_request, params)
            self._close_connection()
        except: Error.resolve(self._error_identifier, label)



