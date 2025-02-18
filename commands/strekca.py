from abc import abstractmethod
import re
from db_handler import DatabaseHandler
from . import Command

A_LOT = 12

class Strecka(Command):
    """
    Command for buying an item, specified in the constructor
    """

    def __init__(self, product_id) -> None:
        self.product = product_id
        super().__init__()
        self.db = DatabaseHandler()

    def execute(self, user_ids, args : str, say):

        pattern = r'^(\d+)?(!)?$'
        match = re.match(pattern, args)
        if not match:
            say("\n".join([ f"Fattar inte helt `{args}`. Kör",
                           f"`{self.usage()}` eller bara {self.__cmd__()} för att strecka"
                           ]))
            return
        try:
            amount = int(match.group(1)) if match.group(1) else 1
        except ValueError:
            say(f"Hmmm... `{match.group(1)}` verkar inte vara ett antal")
            return
        important = bool(match.group(2))

        if amount < 1:
            say(f"Vafan menar du? Du kan ju inte sträcka {amount}")

        if amount > A_LOT and not important:
            say(f"Är du säker på att du vill sträcka {amount} st?! Kör `{self.__cmd__()} {amount}!` för att bekräfta")

        price = self.db.get_price(self.product)
        if price <= 0:
            say(f"Hmmm. Något gick fel. Kontakta <@{self._ADMIN}> om saker inte verkar funka")
            return
        for i in range(amount):
            changes = self.db.purchase(user_ids["db_id"], self.product, price)
            
            if not changes:
                say(f"Hmmm. Något gick fel. Kontakta <@{self._ADMIN}> om saker inte verkar funka"
                    + (f"\nSträckade {i} gånger iallafall" if i else ""))
                return
        say("Har streckat " + (f"{amount} st" if amount > 1 else "") + " :crown:")

    def usage(self):
        return f"{self.__cmd__()} [<antal>]"
