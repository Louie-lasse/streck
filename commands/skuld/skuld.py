from ..command import Command
from db_handler import DatabaseHandler

class Skuld(Command):

    def __init__(self):
        super().__init__()
        self.db = DatabaseHandler()

    def execute(self, user_ids, args: str, say):
        res = self.db.get_debt(user_ids['db_id'])
        if res is None:
            say("Lyckades inte hämta din skuld :pensive:")
            return
        if res == 0:
            say("Du har ingen skuld :tada:")
            return
        if res < 0:
            say(f"Du har ett positivt saldo på {-res} kr :moneybag:")
            return

        say(
            f"Du är skyldig {res} kr" +
            ("\nFy fan" if res > 1000 else "")
        )

    def help(self):
        return str(self)
    
    def description(self):
        return "Se hur mycket skuld du har just nu"
    
    def __cmd__(self):
        return "skuld"
