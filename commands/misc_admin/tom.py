from commands.command import Command
from db_handler import DatabaseHandler
from slack_helper import send_dm

import re

class Tom(Command):
    """
    Tömmer en persons skuld
    """

    def __init__(self, slack_client):
        super().__init__()
        self.slack_client = slack_client
        self.db = DatabaseHandler()

    def _get_users(self, args: str, say):
        user_ids = re.findall(r"<@([A-Z0-9]+)>", args)
        if not user_ids:
            say("Ingen användare angiven")
            say(f"Användning: {self._usage()}")
            return

        res = []
        for uid in user_ids:
            db_user = self.db.get_user(uid)
            if db_user and db_user[0] is not None:
                res.append((db_user[0], uid))
            else:
                say(f"<@{uid}> är inte kopplad till något konto")

        if not res:
            say("Inga giltiga användare angivna")
            say(f"Användning: {self._usage()}")
            return
        return res

    def clear_debt(self, user_id, slack_id, say):
        """
        Clears the debt of a user
        """
        debt = self.db.get_debt(user_id)
        if debt is None or debt <= 0:
            say(f"<@{slack_id}> har ingen skuld")
            return
        changes = self.db.purchase(user_id, None, -debt, paid=True)
        if changes <= 0:
            say(f"Något gick fel när skulden för <@{slack_id}> skulle nollställas")
            return
        say(f"Skulden för <@{slack_id}> har nollställts ({debt} kr)")
        send_dm(self.slack_client, slack_id, f"Din skuld har nollställts av <@{self._ADMIN}>.\n"\
            f"Du hade en skuld på {debt}")



    def execute(self, _, args: str, say):
        if not args:
            say(self._usage())
            return
        user_ids = self._get_users(args, say)
        if not user_ids:
            return
        for user in user_ids:
            self.clear_debt(user[0], user[1], say)

    def _usage(self):
        return f"`{self.__cmd__()} @user`"

    def help(self):
        return "Används för att nollställa en persons skuld\n"\
                f"Använding: {self._usage()}\n"\
                    "Kan även göras på flera personer samtidigt"
    
    def description(self):
        return "Nollställ en persons skuld"
    
    def __cmd__(self):
        return "töm"
