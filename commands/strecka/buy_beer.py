from .base_strecka import Strecka


class Beer(Strecka):

    product_id = 30

    def __init__(self):
        super().__init__(Beer.product_id)

    def help(self):
        return "DU! Om du inte klarar av att sträcka själv får du fan inget"

    def description(self):
        return "HUhmbrbrbrbbrbr... BÄRS!!!"

    def __cmd__(self):
        return "öl"
