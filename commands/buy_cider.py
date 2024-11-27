from .strekca import Strecka

class Cider(Strecka):

    def __init__(self) -> None:
        super().__init__(31)

    def help(self):
        return ":rotating_light: "*3 + "BAAARRSTOOOOOPPPP" + ":rotating_light: "*3
    
    def __str__(self):
        return "Det här kommandet kan du använda för att köpa cider... OM VI HADE NÅGON"