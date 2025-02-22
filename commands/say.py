from . import Command
from slack_helper import send_message, block_of

class Say(Command):

    def __init__(self, slack_client, channel):
        super().__init__()
        self._client = slack_client
        self.channel = channel
        self.bot_id = self._get_bot_id()  # Retrieve bot ID

    def _get_bot_id(self):
        bot_info = self._client.api_call("auth.test")
        return bot_info.get("user_id")

    def execute(self, user_ids, args: str, say):
        if args == "":
            say(self._usage() + f" to post in <#{self.channel}>")
            return
        
        send_message(
            self._client,
            self.channel,
            message=block_of(args)
        )
        say(f"Sent the message in <#{self.channel}>")

    def help(self):
        return f"Makes <@{self.bot_id}> send a message in <#{self.channel}>.\n" + self._usage()
    
    def _usage(self):
        return "Usage: `say <message>`"
    
    def description(self):
        return f"Sends a message as <@{self.bot_id}> in <#{self.channel}>"
    
    def __cmd__(self):
        return "say"
