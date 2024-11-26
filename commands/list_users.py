from .command import Command
from db_handler import DatabaseHandler

class List_Users(Command):

    def __init__(self) -> None:
        super().__init__()
        self.db = DatabaseHandler()

    def execute(self, _, arg: str, say):
        if len(arg) > 0:
            if not arg.isnumeric() or int(arg) != float(arg):
                say("Please provide an integer value, or nothing to get the default `10`")
                return
            n = int(arg)
        else:
            n = 10
        users = self.db.list_users(n)
        say('\n'.join(users))

    def help(self):
        return """Admin command for listing recently added users. To be used in combination with `connect`.
        When used on its own, 10 users will be provided (`database_id` and `name`). This number can be specified with each request.
        Usage:
        * `list_users`
        * `list_users 15`
        """
        
    def __str__(self):
        return "Gets basic information of users, like `database_id`"
