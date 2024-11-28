from db_handler import DatabaseHandler
from . import Command
import os

class Strecka(Command):
    """
    Command for buying an item, specified in the constructor
    """

    def __init__(self, product_id) -> None:
        self.product = product_id
        super().__init__()
        self.db = DatabaseHandler()
        self._ADMIN = os.getenv("ADMIN")

    def execute(self, user : dict[str,str], args : str, say):
        price = self.db.get_price(self.product)
        if price <= 0:
            say(f"Hmmm. Något gick fel. Kontakta <@{self._ADMIN}> om saker inte verkar funka")
            return
        
        changes = self.db.purchase(user["db_id"], self.product, price)
        
        if not changes:
            say(f"Hmmm. Något gick fel. Kontakta <@{self._ADMIN}> om saker inte verkar funka")
            return
        say("Har streckat :crown:")
