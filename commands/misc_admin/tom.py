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
        user_ids = re.findall(r"(?:<@)?(\d+|[A-Z0-9]+)(?:>)?", args)
        if not user_ids:
            say("Ingen användare angiven")
            say(f"Användning: {self._usage()}")
            return

        res = []
        for uid in user_ids:
            db_user = self.db.get_user(uid)
            if db_user and db_user[0] is not None:
                res.append((db_user[0], uid))
                continue
            if all([c.isdigit() for c in uid]):
                res.append((int(uid), None))
                continue
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
        if slack_id is None:
            slack_id = user_id
        debt = self.db.get_debt(user_id)
        if debt is None:
            say(f"<@{slack_id}> har ingen skuld")
            return
        if debt <= 0:
            say(f"Du var skyldig <@{user_id}> pengar. \nDu ska swisha dom {debt}.")
        changes = self.db.purchase(user_id, None, -debt, paid=True)
        if changes <= 0:
            say(f"Något gick fel när skulden för <@{slack_id}> skulle nollställas")
            return
        say(f"Skulden för <@{slack_id}> har nollställts ({debt} kr)")
        if slack_id == user_id:
            say(f"{user_id} verkar inte vara kopplad till slack, så kan inte berätta för hen att skulden nollställts")
            return
        send_dm(self.slack_client, slack_id, f"Din skuld har nollställts av <@{self._ADMIN}>.\n"\
            f"Du hade en skuld på {debt}")



    def execute(self, _, args: str, say):
        user_ids = self._get_users(args, say)
        if not user_ids:
            return
        for user in user_ids:
            self.clear_debt(user[0], user[1], say)

    def _usage(self):
        return f"`{self.__cmd__()} [@user | databasid]`"

    def help(self):
        return "Används för att nollställa en persons skuld\n"\
                f"Använding: {self._usage()}\n"\
                    "Kan även göras på flera personer samtidigt"\
                    f"e.g. `{self.__cmd__()} @user1 @user2 databasid1`"
    
    def description(self):
        return "Nollställ en persons skuld"
    
    def __cmd__(self):
        return "töm"
