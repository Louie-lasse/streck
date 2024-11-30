from slack_helper import send_dm
from . import Command

class Request(Command):

    def __init__(self, slack_client) -> None:
        super().__init__()
        self._client = slack_client

    def execute(self, user_ids, args: str, say):
        if not args:
            say("Skriv `request` följt av vad du vill ha för ny feature.")
            return
        
        if args.lower() in ["öl","cider","läsk"]:
            say(f"Gillar hur du tänker, men tror du borde pröva `{args}` istället")
                
        if send_dm(
                slack_client=self._client,
                user=self._ADMIN,
                message=f"User <@{user_ids["slack_id"]}> is requesting a new feature:\n```\n{args}\n```"
            ):
            say(f"Skickat vidare din förfrågan till <@{self._ADMIN}>")
        else:
            say("Lyckades inte skicka meddelandet :pensive:")

    def help(self):
        return "Skicka ett förlag på en ny feature.\nAnvändning: `request <beskrivning av vad du vill ha>`."
    
    def __str__(self):
        return "`request`: Föreslå en ny feature."
