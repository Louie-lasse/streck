# asp.py
from ..command import Command
from ..command_registry import Command_registry
from .asp_commands import AspList, AspAdd, AspRemove, AspTom
from ..strecka.prislista import Prislista
from db_handler import DatabaseHandler

class Asp(Command):
    def __init__(self):
        self.db = DatabaseHandler()
        self.products = Prislista.get_products()
        self._registry = Command_registry()
        db = self.db
        for cmd in (AspList(db), AspAdd(db), AspRemove(db), AspTom(db)):
            self._registry.add(cmd)

    def execute(self, user_ids, args, say):
        if user_ids["slack_id"] != self._ADMIN:
            say("Not authorized.")
            return

        sub, _, rest = args.strip().partition(" ")
        rest = rest.strip()

        if sub in self._registry: # predefined subcommands win over product names
            self._registry[sub].execute(user_ids, rest, say)
        elif sub in self.prislista._products:
            self._buy(user_ids, sub, rest, say)
        else:
            say(f"Unknown asp subcommand or product: `{sub}`")

    def _buy(self, user_ids, product_cmd, rest, say):
        asp_id, _, product_args = rest.partition(" ")
        if not asp_id:
            say("Usage: `asp <product> <asp_id> [args]`")
            return
        real_id = self.db.get_asp_user_id(asp_id)  # TODO
        product = self.prislista._products[product_cmd]
        product.execute(
            {"slack_id": user_ids["slack_id"], "db_id": real_id},
            product_args.strip(),
            say,
        )

    def help(self):
        return (
            "`asp <subcommand>` — manage/act on behalf of asps.\n"
            f"{self._registry}\n" + 
            ("\n").join(["`asp "+product.usage()+"`" for product in self.products])
        )

    def description(self):
        return "Manage and act on behalf of users not on Slack"

    def __cmd__(self):
        return "asp"
