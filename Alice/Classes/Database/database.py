import mariadb

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
            
            Parameters
            ----------                      
            sql_request : str
                This is a string    
        """
        self._check_params(sql_request, params)
        return self.curseur.fetchall()
    
    def select_and_close(self, sql_request: str, params: tuple|None = None):
        """
            Select must be used to retrieve some data from the database and closes the connexion to it.
            
            Parameters
            ----------                      
            sql_request : str
                This is a string    
        """
        self._check_params(sql_request, params)
        result = self.curseur.fetchall()
        self._close_connection()
        return result
    
    def mutate(self, sql_request: str, params: tuple|None = None):
        """
            Mutate must be used to do operations such as updations, insertions or deletions on the database.
            
            Parameters
            ----------                      
            sql_request : str
                This is a string
                
            params : int
                This is a tuple        
        """
        self._check_params(sql_request, params) 
        self.connexion.commit()
        
    def mutate_and_close(self, sql_request: str, params: tuple|None = None):
        """
            Mutate must be used to do operations such as updations, insertions or deletions on the database and closes the connexion to it.
            
            Parameters
            ----------                      
            sql_request : str
                This is a string
                
            params : int
                This is a tuple        
        """
        self.mutate(sql_request, params)
        self._close_connection()



