import http.client
import json

def get_results():
    
    connection = http.client.HTTPSConnection('opendata.paris.fr')

    connection.request("GET", "/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?select=*&where=nom_arrondissement_communes=%22Paris%22&order_by=stationcode&limit=100")

    response = connection.getresponse()

    results = json.dumps(response.read().decode())

    connection.close()
    
    return results
    
