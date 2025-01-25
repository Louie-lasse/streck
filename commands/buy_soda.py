from .strekca import Strecka

class Soda(Strecka):

    def __init__(self) -> None:
        super().__init__(40)

    def help(self):
        return """Ska inte du vara ingengör?!
        1. Skriv `läsk`
        2. Ta din läsk
        3. ?
        4. En bra kväll
        """
    
    def description(self):
        return "För att köpa läsk, kort och gott"

    def __cmd__(self):
        return "läsk"
