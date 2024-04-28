# A développer pour aller plus loin.

class Verificator:
    # Renvoie soit True soit les erreurs
    def __init__(self, form: dict):
        if isinstance(form, dict):
            self.form = form
        else: raise TypeError
        
    def _inspect_keys(self):
        if "firstname" in self.form:
            pass
            
            
    def _inspect_name(name, type_of_name):
        if name:
            if len(name) < 3:
                # formError.add(type_of_name, "length")
                return True
        return False
    
    
                
            