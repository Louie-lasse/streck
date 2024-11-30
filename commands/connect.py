from . import Command
import re
from db_handler import DatabaseHandler
from slack_helper import send_dm
from .update import Update

class Connect(Command):

    def __init__(self, slack_client) -> None:
        super().__init__()
        self.db = DatabaseHandler()
        self.client = slack_client
        self.updator = Update(slack_client)

    def execute(self, user_ids, args: str, say):
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

        old = self.db.get_user(slack_id)
        if not old:
            if self.db.remove_slack(old[0]):
                say(
                    f"Disconnected the user previously associated with <@{slack_id}>" +
                    f"Old user: {old[1]}"
                    )
            else:
                say(f"Something went wrong. A user is already connected to <@{slack_id}>, but was unable to remove them")
                return

        res = self.db.connect_user(db_id, slack_id)
        if res:
            say(f"Användaren <@{slack_id}> är nu kopplad till db_id {db_id} ({res[0]}).")
            send_dm(
                self.client,
                slack_id,
                f"Du har blivit kopplad till Bastugatan av <@{self._ADMIN}>!"
            )
            self.updator.execute(slack_id, "", say)
        else:
            say(f"Kunde inte koppla användaren. Kontrollera att db_id {db_id} är giltigt.")

    def help(self):
        return f"""Connect a slack user to a db entry using db_id.
Usage: `connect <db_id> @<user>`
The `db_id` can be obained using `list_users`.
The `user` above is a regular slack mention, like <@{self._ADMIN}>"""
    
    def __str__(self):
        return "`connect` (admin): Connects a slack user to a db entry."