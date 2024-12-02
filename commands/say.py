from . import Command
from slack_helper import send_message

class Say(Command):

    def __init__(self, slack_client, channel) -> None:
        super().__init__()
        self._client = slack_client
        self.channel = channel

    def execute(self, user_ids, args: str, say):
        if args == "":
            say(self._usage() + " to post in bastugatan")
            return
        
        send_message(
            self._client,
            self.channel,
            message=args
        )
        say(f"Sent the message in #bastugatan")

    def help(self):
        return f"Makes the bot send a message in #bastugatan.\n" + self._usage()
    
    def _usage(self):
        return "Usage: `say <message>`"
    
    def __str__(self):
        return "`say` (admin): send a message as bastugatan"
