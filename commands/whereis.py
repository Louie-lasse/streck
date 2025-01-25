import re
from . import Command

class Where_Is(Command):

    def execute(self, user_ids, args: str, say):
        match = re.match(r"<#([A-Z0-9]+)|>", args)
        res = match.group(1) if match else None

        if res:
            say(res)
        else:
            say(f"Lyckades inte få ut kannalens id från '{args}'\n"+
                f"Korrekt användning är: {self._usage()}")
            
    def _usage(self):
        return f"`{self.__cmd__()} #channel`"
    
    def help(self):
        return (
            "Skriver ut en kannals id." +
            "Används e.x. om man vill ändra vilka kannaler bastugatan bor i." +
            f"Användning: {self._usage}"
        )
    
    def description(self):
        return "Kolla en kannals id"
    
    def __cmd__(self):
        return "whereis"
