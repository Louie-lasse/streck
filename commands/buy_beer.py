from .strekca import Strecka

class Beer(Strecka):

    def __init__(self) -> None:
        super().__init__(30)

    def help(self):
        return "DU! Om du inte klarar av att beställa själv får du fan inget"
    
    def __str__(self):
        return "`öl`: HUhmbrbrbrbbrbr... BÄRS!!!"