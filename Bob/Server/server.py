import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import time
import threading
from Communication.Classes.Server.server import Server
from Bob.Client.clientHTTP import get_results

server  = Server()

client_number = 0

def wait():
    time.sleep(300)

should_just_redo_and_not_accept = False

while True:
  
    if not should_just_redo_and_not_accept:
        server.wait_connection()
    
    client_number = client_number + 1
    

    if client_number == 1:
        
        results = get_results()
        message = f"{len(results)}\n\n{results}"
        server.dispatch(message)
        
        t = threading.Thread(target = wait)
        t.start()
        should_just_redo_and_not_accept = False
        
    else:
        
        if not t.is_alive():
            client_number = 0
            should_just_redo_and_not_accept = True
            continue
        
        server.dispatch(message)
