import re

from db_handler import DatabaseHandler
from slack_helper import send_dm
from .command import Command

class Disconnect(Command):
    def __init__(self, slack_client) -> None:
        super().__init__()
        self.db = DatabaseHandler()
        self.client = slack_client

    def execute(self, user_ids, args: str, say):
        if args == "":
            return say(self._usage())
        match = re.match(r"<@([A-Z0-9]+)>", args)
        slack_id = match.group(1) if match else None

        if not slack_id:
            return say(f"Kunde inte hitta användaren {args}.\n"+
                       f"Korrekt användning: {self._usage()}")
        
        res = self.db.disconnect_user(slack_id)
        
        if not res:
            return say("Kunde inte koppla bort användaren. Kontrollera att användaren är kopplad till Bastugatan.")

        say("Användaren har kopplats bort från bastugatan")

        send_dm(
            self.client,
            slack_id,
            f"Du har blivit bortkopplad från Bastugatan. Kontakta <@{self._ADMIN}> om du tror att detta är ett misstag."
        )
        

    def help(self):
        return f"Ta bort en användare som kopplats av misstag\n{self._usage()}"
    
    def _usage(self):
        return f"Usage: {self.__cmd__()} <@person>\nExempel: `disconnect @Bärra"

    def description(self):
        return "Tar bort en användare från bastugatan (inte strecklistan)"

    def __cmd__(self):
        return "disconnect"