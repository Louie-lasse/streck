from . import Command
from db_handler import DatabaseHandler

class Strecklista(Command):

    def __init__(self) -> None:
        super().__init__()
        self.db = DatabaseHandler()

    def execute(self, user_ids: dict[str, str], args: str, say):
        all = self.db.get_all_debts()
        res = [v for v in
               filter(
                lambda x: int(x[2]) > 0,
                all
            )
        ]
        width = max(len(f"<@{r[1]}>" if r[1] else r[0]) for r in res)
        say(
            '\n'.join([
                (f"<@{r[1]}>" if r[1] else f"{r[0]}").ljust(width)
                + f"\t{int(r[2])}"
                for r in res
            ])
        )

    def help(self):
        return """Skriver ut toplistan av allas skulder just nu. Rensar INTE skulder.
Detta är tänkt att hjälpa kaffekassaansvarig med att kassera ut kaffekassan"""

    def __str__(self):
        return "`strecklista` (admin): Se hur nuvarande strecklistan ser ut"
