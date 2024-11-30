
from . import Command

class Whoami(Command):

    def execute(self, user_ids, args: str, say):
        say(f"{user_ids['slack_id']}")
    
    def help(self):
        return "Skriver ut dit slack_id. Änvänds bara vid byte av IT-ansvarig"
    
    def __str__(self):
        return "`whoami`: Skriver ut dit slack_id. Änvänds bara vid byte av IT-ansvarig"