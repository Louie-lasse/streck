from bastugatan import ADMIN
from db_handler import DatabaseHandler
from . import Command

class Strecka(Command):
    """
    Command for buying an item, specified in the constructor
    """

    def __init__(self, product_id) -> None:
        self.product = product_id
        super().__init__()
        self.db = DatabaseHandler()

    def execute(self, user_ids : tuple[str,str], args : str, say):
        price = self.db.get_price(self.product)
        if price <= 0:
            say(f"Hmmm. Något gick fel. Kontakta <@{ADMIN}> om saker inte verkar funka")
            return
        
        changes = self.db.purchase(user_ids[1], self.product, price)
        
        if not changes:
            say(f"Hmmm. Något gick fel. Kontakta <@{ADMIN}> om saker inte verkar funka")
            return
        say("Har streckat :crown:")
