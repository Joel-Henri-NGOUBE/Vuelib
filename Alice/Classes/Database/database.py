import mariadb
from ..ErrorInterface.Execution.execution import ExecutionError as Error

config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "vuelib"
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
    
    # def _dictify(a, self,data, dataCell):
    #     i = 0
    #     # print(a_result)
    #     for index in self._curseur.description:
    #         # print(i)
    #         dataCell[str(index[0])] = a[i]
    #         i += 1
    #     data.append(dataCell)
    #     return data
    
    def _get_data(self, sql_request: str, params: tuple|None = None):
        self._check_params(sql_request, params)
        result = self._curseur.fetchall()
        description = self._curseur.description
        headers = list(map(lambda h: h[0], description))
        data = list(map(lambda d: dict(zip(headers, d)), result))
        return data
        
    def select(self, sql_request: str, params: tuple|None = None):
        """
            Select must be used to retrieve some data from the database.    
        """
        label = "SELECT"
        try:
            return self._get_data(sql_request, params)
        except Exception as err:
            Error.resolve(self._error_identifier, label, Error.exception, f"{err}")
            
    
    def select_and_close(self, sql_request: str, params: tuple|None = None):
        """
            Select_and_close must be used to retrieve some data from the database and closes the connexion to it.   
        """
        label = "SELECT_AND_CLOSE"
        try:
            result = self._get_data(sql_request, params)
            self._close_connection()
            return result
        except Exception as err:
            Error.resolve(self._error_identifier, label, Error.exception, f"{err}")

    
    def mutate(self, sql_request: str, params: tuple|None = None):
        """
            Mutate must be used to do operations such as updations, insertions or deletions on the database.       
        """
        label = "MUTATE"
        try:
            self._check_params(sql_request, params) 
            self._connexion.commit()
        except Exception as err: 
            Error.resolve(self._error_identifier, label, Error.exception, f"{err}")
        
    def mutate_and_close(self, sql_request: str, params: tuple|None = None):
        """
            Mutate_and_close must be used to do operations such as updations, insertions or deletions on the database and closes the connexion to it.     
        """
        label = "MUTATE_AND_CLOSE"
        try:
            self.mutate(sql_request, params)
            self._close_connection()
        except: Error.resolve(self._error_identifier, label)
        
    def close(self):
        self._close_connection()
        
    # def old_function():
        # data = list()
        # dataCell = dict()
        # # for a_result in result:
        # #     i = 0
        # #     print(a_result)
        # #     for index in self._curseur.description:
        # #         # print(i)
        # #         dataCell[str(index[0])] = a_result[i]
        # #         i += 1
        # #     data.append(dataCell)
        # data2 = map(self._dictify(a,self, data, dataCell), result)



