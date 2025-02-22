from .strekca import Strecka

class Beer(Strecka):

    def __init__(self):
        super().__init__(30)

    def help(self):
        return "DU! Om du inte klarar av att sträcka själv får du fan inget"
    
    def description(self):
        return "HUhmbrbrbrbbrbr... BÄRS!!!"
    
    def __cmd__(self):
        return "öl"