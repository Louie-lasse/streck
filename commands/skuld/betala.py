from ..command import Command
from db_handler import DatabaseHandler
from slack_helper import send_dm

import re

class Betala(Command):

    def __init__(self, slack_client):
        super().__init__()
        self._client = slack_client
        self.db = DatabaseHandler()

    def execute(self, user_ids, args: str, say):
        pattern = r'^<@([A-Z0-9]+)> (\d+) ?(!)?$'
        match = re.match(pattern, args)
        if not match:
            say("\n".join([f"Fattar inte helt `{args}`. Kör",
                           f"`{self.usage()}`"
                           ]))
            return

        skuld = None
        try:
            slack_id = match.group(1)
            db_id = self.db.get_user(slack_id)[0]
            skuld = self.db.get_debt(db_id)
        except Exception:
            pass
        if skuld is None:
            say(f"Något gick fel :pensive:. Är du säker på att <@{match.group(1)}> är inlaggd?")
            return

        try:
            amount = int(match.group(2))
        except ValueError:
            say(f"Hmmm... `{match.group(2)}` verkar inte vara ett heltalsvärde")
            return

        important = bool(match.group(3))

        if amount > skuld:
            if not important:
                say(f"Om du betalar ut {amount} får personen ett positivt saldo. Om du är säker, kör `{self.usage()} !`")
                return

        self.db.purchase(db_id, None, -amount, paid=True)
        say(f"Ändrat skulden för <@{slack_id}> med {amount} kr. De är nu skylldiga {skuld - amount} kr.")

        send_dm(
            self._client,
            slack_id,
            f"Din skuld har minskats med {amount} kr av <@{user_ids['slack_id']}>. Du är nu skylldig {skuld - amount} kr."
        )

    def usage(self):
        return f"{self.__cmd__()} <@user> <belopp>"

    def help(self):
        return "\n".join([
            f"`{self.__cmd__()} <@user> <belopp>`",
            "Betalar ut x kr till någon för inköp eller dylikt.",
            "Exempel:",
            f"betala <@{self._ADMIN}> 150"
        ])
    
    def description(self):
        return "Betala någon för inlagda pengar (alt inköp)"
    
    def __cmd__(self):
        return "betala"
