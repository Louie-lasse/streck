from . import Command
import re
from db_handler import DatabaseHandler

class Connect(Command):

    def __init__(self) -> None:
        super().__init__()
        self.db = DatabaseHandler()

    def execute(self, user_ids: dict[str, str], args: str, say):
        """
        Connects a user by associating a db_id with a Slack ID.
        Args:
            user_ids (dict[str, str]): Contains 'slack_id' and 'db_id' of the current user.
            args (str): Command arguments in the form "{db_id} <@slack_id>".
            say (function): Function to send messages to Slack.
        """

        match = re.match(r"(\d+)\s*<@(\w+)>", args)
        if not match:
            say("Fel format. Använd: `connect {db_id} <@slack_id>`")
            return

        db_id, slack_id = match.groups()

        if not db_id.isnumeric or str(db_id) != float(db_id):
            say("db_id must be an integer")

        res = self.db.connect_user(db_id, slack_id)
        if res:
            say(f"Användaren <@{slack_id}> är nu kopplad till db_id {db_id}.")
            say(
                CHANNEL=slack_id,
                text=f"<@{self._ADMIN}> har lagt kopplat dig till Bastugatan!"
            )
        else:
            say(f"Kunde inte koppla användaren. Kontrollera att db_id {db_id} är giltigt.")

    def help(self):
        return f"""Connect a slack user to a db entry using db_id.
Usage: `connect <db_id> @<user>
The `db_id` can be obained using `list_users`.
The `user` above is a regular slack mention, like <@{self._ADMIN}>"""
    
    def __str__(self):
        return "`connect` (ADMIN): Connects a slack user to a db entry."