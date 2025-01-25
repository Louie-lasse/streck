from slack_helper import send_dm
from . import Command
from db_handler import DatabaseHandler
import re

class Strecklista(Command):

    def __init__(self, slack_client) -> None:
        super().__init__()
        self.db = DatabaseHandler()
        self._client = slack_client

    def execute(self, user_ids, args: str, say):
        all = self.db.get_all_debts()
        res = [v for v in
               filter(
                lambda x: int(x[2]) > 0,
                all
            )
        ]
        width = max(len(f"<@{r[1]}>" if r[1] else r[0]) for r in res)

        message = '\n'.join([
                (f"<@{r[1]}>" if r[1] else f"{r[0]}").ljust(width)
                + f"\t{int(r[2])}"
                for r in res
            ])
        
        match = re.match(r"<@([A-Z0-9]+)>", args)
        if match:
            send_dm(
                self._client,
                match.group(1),
                message
            )
            message = f"Skickat strecklista till <@{match.group(1)}>"

        say(
            message
        )

    def help(self):
        return """Skriver ut toplistan av allas skulder just nu. Rensar INTE skulder.
Detta är tänkt att hjälpa kaffekassaansvarig med att kassera ut kaffekassan"""

    def description(self):
        return "Se hur nuvarande strecklistan ser ut"
    
    def __cmd__(self):
        return "strecklista"
