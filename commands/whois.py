import re
from . import Command

class Who_Is(Command):

    def execute(self, user_ids: dict[str, str], args: str, say):
        if args.lower() == "admin":
            say(f"<@{self._ADMIN}>: {self._ADMIN}")
            return

        match = re.match(r"<@([A-Z0-9]+)>", args)
        res = match.group(1) if match else None

        if res:
            say(res)
        else:
            say(f"Lyckades inte få ut användarid från '{args}'\n"+
                f"Korrekt användning är: {self._usage()}")
            
    def _usage(self):
        return "`whois @user`"
    
    def help(self):
        return (
            "Skriver ut en användares slack_id." +
            "Behövs bara om man ska ändra admin (görs i filen `.env`)" +
            f"Användning: {self._usage}"
        )
    
    def __str__(self):
        return "whois (admin): Kolla en användares slack_id"