class ExecutionError:
    
    # Les labels d'erreurs: Chaîne de caractère permettant à l'application de reconnaître une erreur
    class_error_identifier = "[ERREUR CLASSE_ERROR_INTERFACE]"
    type = "TYPE"
    key = "KEY"
    index = "INDEX"
    zero = "ZERO"
    
    @classmethod
    def resolve(cls, identifier: str, label: str, message: str = "", variable: str = "") -> str:
        """
            Méthode de classe d'identification d'erreur
        """
        labelResolve = "RESOLVE"
        try:
            if isinstance(identifier, str) and isinstance(label, str) and isinstance(message, str) and isinstance(variable, str):    
                if variable:
                    variable += " "
                print(f"{identifier} {label} - {cls._get_error(message, variable)}")
            else: raise TypeError
        except TypeError:
            cls.resolve(cls.class_error_identifier, labelResolve, cls.type)
    
    def _get_error(message, variable):
        match message:
            case ExecutionError.type:
                return f"Paramètre {variable}de mauvais type"
            case ExecutionError.key:
                return f"Clé {variable}introuvable dans la collection"
            case ExecutionError.index:
                return f"Index {variable}introuvable dans la séquence"
            case ExecutionError.zero:
                return f"Aucun nombre n'est divisible par 0."
            case _:
                return "Erreur non identifiée"
            
# print(ExecutionError.resolve("[ERREUR CLASSE_ERROR_INTERFACE]", "RESOLVE", "TYPE"))