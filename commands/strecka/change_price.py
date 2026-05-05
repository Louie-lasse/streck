from .prislista import Prislista
from ..command import Command
import re

class ChangePrice(Command):

    def execute(self, user_ids, args: str, say):
        pattern = r'^(\w+) (\d+)$'
        match = re.match(pattern, args)
        if not match:
            say("\n".join([f"Fattar inte va du snackar om, formatera korrekt tack!.",
                           f"{self.help()}"
                           ]))
            return
        product, price = match.group(1), match.group(2)

        try:
            price = int(price)
        except ValueError:
            say(f"Hmmm... `{price}` verkar inte vara ett tal")
            return
        
        # kollar att produkten finns
        products = Prislista._products
        if not product in products:
            say(f"'{product}' verkar inte vara nått vi har hemma! Produkten finns inte.")
            return
        
        if price == 0:
            say(f"Vet att alkohol är dyrt men kom igen nu! Priset ska vara >0.")
            return

        success = products[product].change_price(price)

        if success:
            say(f"Löst! Tråkigt med inflation.")
        else:
            say(f"Något gick fel, beklagar!")
    
    def help(self):
        return "Ändrar priset på en produkt!"
    
    def description(self):
        return self.help()
    
    def __cmd__(self):
        return "prisändring"
