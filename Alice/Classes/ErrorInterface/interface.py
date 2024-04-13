class ErrorInterface:
    
    @classmethod
    def resolve(self, identifier: str, label: str, message: str, variable: str = "") -> str:
        try:
            if isinstance(identifier, str) and isinstance(label, str) and isinstance(message, str) and isinstance(variable, str):    
                if variable:
                    variable += " "
                print(f"{identifier} {label} - {self._get_error(message, variable)}")
            else: raise TypeError
        except TypeError:
            self.resolve("[ERREUR CLASSE_ERROR_INTERFACE]", "RESOLVE", "TYPE")
            
    
    def _get_error(message, variable):
        match message:
            case "TYPE":
                return f"Paramètre {variable}de mauvais type"
            case "KEY":
                return f"Clé {variable}introuvable dans la collection"