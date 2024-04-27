
from ..database import Database

class Requests :
        # pour gerer l'operation CRUD
    @classmethod
    def get_favorite_station(cls,user_id):
        #  pour voir et recuperer les station favori
        db = Database()
        sql="SELECT * FROM favorites WHERE id_user = %s" # subtitution
        params= (user_id,)
        return db.select_and_close(sql,params)
    
    @classmethod
    def add_favorite_station(cls,user_id, station_code):
        # pour creer une nouvelles station favori
        db = Database()
        sql = "INSERT INTO favorites(id_user,station_code) VALUES (%s,%s)"
        params= (user_id,station_code)
        db.mutate_and_close(sql,params)

    @classmethod
    def update_favorite_station(cls,user_id, old_station_code, new_station_code):
        # pour modifier une station favori
        db = Database()
        sql = "UPDATE favorites SET station_code = %s WHERE id_user = %s AND station_code = %s"
        params = (new_station_code, user_id, old_station_code)
        db.mutate_and_close(sql, params)

    @classmethod   
    def remove_favorite_station(cls, user_id, station_code):
        # pour supprimer une station favori
        db = Database()
        sql = "DELETE FROM favorites WHERE id_user = %s AND station_code = %s"
        params = (user_id, station_code)
        db.mutate_and_close(sql, params)

