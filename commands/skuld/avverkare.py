from ..command import Command
from db_handler import DatabaseHandler
from ..strecka.buy_beer import Beer
from ..strecka.buy_cider import Cider

import re

class Avverkare(Command):
    
    def __init__(self):
        super().__init__()
        self.default_days = 90
        self.db = DatabaseHandler()
        self.ids = [Beer.product_id, Cider.product_id]
    
    def execute(self, user_ids, args, say):
        """
        Return by user the total amount of beer/cider consumed in the last N days
        """
        pattern = r'^(\d+)?$'
        match = re.match(pattern, args)
        if not match:
            days = self.default_days
        else:
            try:
                days = int(match.group(1)) if match.group(1) else int(365/4)
            except ValueError:
                say(f"Hmmm... `{match.group(1)}` verkar inte vara ett antal dagar")
                return
        if days < 1:
            say("Antal dagar måste vara minst 1")
            return
        results = self.db.get_recent_transactions(self.ids, days)
        if not results:
            say("Lyckades inte hämta ut datan.")
            return
        lines = [f"De som avverkat mest de senaste {days} dagarna:"]
        for name, amount in results:
            lines.append(f"- {name}: {amount} st")
        say("\n".join(lines))

    def help(self):
        return "\n".join([
            "Används för att kolla hur mycket folk druckit",
            f"Användning: {self._usage()}",
            f"Eller bara {self.__cmd__()} för att kolla de senaste {self.default_days} dagarna"
        ])

    def _usage(self):
        return f"{self.__cmd__()} <antal dagar>"

    def description(self):
        return "Berätta hur många enheter folk har avverkat på sistonde"

    def __cmd__(self):
        return "avverkare"