import requests

def get_velib_data():
    try:
        url = 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?where=nom_arrondissement_communes%20%3D%20%22Paris%22&order_by=stationcode&limit=100'
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Erreur lors de la requête :", response.status_code)
            return None
    except Exception as e:
        print("Erreur lors de la requête :", str(e))
        return None

velib_data = get_velib_data()
