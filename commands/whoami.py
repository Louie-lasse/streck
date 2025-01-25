
from . import Command

class Whoami(Command):

    def execute(self, user_ids, args: str, say):
        say(f"{user_ids['slack_id']}")
    
    def help(self):
        return "Skriver ut dit slack_id. Änvänds vid byte av IT-ansvarig"
    
    def description(self):
        return self.help()
    
    def __cmd__(self):
        return "whoami"
