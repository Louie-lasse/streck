# asp_subcommands.py
from ..command import Command


class AspList(Command):
    def __init__(self, db):
        self.db = db

    def execute(self, user_ids, args, say):
        asps = self.db.list_asps()
        say("\n".join(f"`{name}` (id {uid})" for name, uid in asps) or "Hittar inga aspar.")

    def help(self):
        return "`asp list`: lista alla aspar."

    def description(self):
        return "Listar alla aspar"

    def __cmd__(self):
        return "list"


class AspAdd(Command):
    def __init__(self, db):
        self.db = db

    def execute(self, user_ids, args, say):
        db_id = args.strip()
        if not db_id:
            say("Användning: `asp add <db_id>`")
            return
        pretty = self.db.add_asp(db_id)
        if not pretty:
            say(f"Användare med id `{db_id}` finns inte eller är redan registrerad som asp.")
            return
        say(f"Registrerade `{pretty}` som asp.")

    def help(self):
        return "`asp add <db_id>`: registrera en användare som asp. db_id fås från `list_users`."

    def description(self):
        return "Registrera en användare som asp"

    def __cmd__(self):
        return "add"


class AspRemove(Command):
    def __init__(self, db):
        self.db = db

    def execute(self, user_ids, args, say):
        asp_id = args.strip()
        if not asp_id:
            say("Användning: `asp remove <db_id>`")
            return
        self.db.remove_asp(asp_id)  # TODO
        say(f"Tog bort `{asp_id}` som asp.")

    def help(self):
        return "`asp remove <asp_id>`: avregistrera en användare som asp."

    def description(self):
        return "Ta bort en asp"

    def __cmd__(self):
        return "remove"


class AspTom(Command):
    def __init__(self, db):
        self.db = db

    def execute(self, user_ids, args, say):
        asp_name = args.strip()
        if not asp_name:
            say("Användning: `asp tom <asp_name>`")
            return
        real_id = self.db.get_asp_user_id(asp_name)
        self.empty_balance(asp_name, real_id)

    def empty_balance(self, name, user_id):
        debt = self.db.get_debt(user_id)
        if debt is None:
            say(f"{name} har ingen skuld")
            return
        if debt <= 0:
            say(f"{name} hade {debt} kr inne. Det ska swishas TILL dem.")
        changes = self.db.purchase(user_id, None, -debt, paid=True)
        if changes <= 0:
            say(f"Något gick fel när skulden för {name} skulle nollställas")
            return
        say(f"Skulden för {name} har nollställts ({debt} kr)")

    def help(self):
        return "`asp tom <asp_name>`: nollställ en asps skuld."

    def description(self):
        return "Töm en asps skuld"

    def __cmd__(self):
        return "töm"
