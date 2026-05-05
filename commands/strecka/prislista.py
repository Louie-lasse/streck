from ..command import Command

class Prislista(Command):

    _products = {}

    @staticmethod
    def add_product(product):
        Prislista._products[product.__cmd__()] = product

    def execute(self, user_ids, args: str, say):
        if not Prislista._products:
            say("Det finns inga produkter i prislistan.")
            return
        product_list = "\n".join(
            f"{product.__cmd__()}: {product.description()} - {product.get_price()} kr"
            for product in Prislista._products.values()
        )
        say(f"Prislista:\n{product_list}")

    def help(self):
        return "Visa prislista för alla inlagda produkter."

    def description(self):
        return "Visa prislista"

    def __cmd__(self):
        return "prislista"
