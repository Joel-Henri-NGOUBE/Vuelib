import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Communication.Classes.Client.client import Client
import json

def retrieve_stations():
    client = Client()

    message = client.get_message()

    length, result = client.get_protocol_modalities(message)

    length = int(length)

    while length > client.max_length:
        result += client.get_message() 
        length = length - client.max_length

    stations = json.loads(json.loads(result))
    # print(stations)
    # print("\n")

    client.close()
    
    return (stations, result)

# retrieve_stations()