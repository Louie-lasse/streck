from .strekca import Strecka

class Cider(Strecka):

    def __init__(self):
        super().__init__(31)

    def help(self):
        return (
            ":rotating_light: "*3 + "BAAARRSTOOOOOPPPP" + ":rotating_light: "*3 +
            "\nKlarar du inte att sträcka själv får du inget"
        )
    
    def description(self):
        return "Det här kommandet kan du använda för att köpa cider... OM VI HADE NÅGON"
    
    def __cmd__(self):
        return "cider"
