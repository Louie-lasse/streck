import re

from db_handler import DatabaseHandler
from .command import Command
from .connect import Connect

class Add(Command):
    def __init__(self, slack_client):
        super().__init__()
        self.db = DatabaseHandler()
        self.client = slack_client
        self.connector = Connect(slack_client)

    def execute(self, user_ids, args: str, say):
        args = args.split(" ")
        if len(args) != 3:
            return say(self._usage())
        name, barcode, user = args
        match = re.match(r"<@([A-Z0-9]+)>", user)
        slack_id = match.group(1) if match else None

        if not slack_id:
            return say(f"Kunde inte hitta användaren {user}.\n"+
                       f"Korrekt användning: {self._usage()}")
        
        res = self.db.add_user(barcode, name)

        if not res:
            return say(f"Kunde inte lägga till användaren {name} med streckkod {barcode}.\n"+
                       "Pröva `list_users` för att se om användaren redan finns.")
        
        db_id = self.db.get_user_by_barcode(barcode)[0]
        print(f"{db_id} <@{slack_id}>")

        self.connector.execute(user_ids, f"{db_id} <@{slack_id}>", say)


    def _usage(self):
        return (f"Användning: `{self.__cmd__()} <namn> <sträckkod> <@person>\n`"+
                "Exempel: `add Bärra barra @Bärra`\n"+
                "WARN! Barcode skannern är kinkig med ÅÄÖ osv. Använd enbart siffror och bokstäver uröver ÅÄÖ."+
                "Barcodes är lite godtyckliga, bara de stämmer överens med den barcode du genererar")

    def help(self):
        return ("Lägger till en ny användare till streck-appen. Kopplar dem även till bastugatan.\n"+
        self._usage())
    
    def description(self):
        return "Lägger till en ny användare"
    
    def __cmd__(self):
        return "add"
