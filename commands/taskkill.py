import signal
from commands.command import Command
import time
import os

class TaskKill(Command):
    """
    Kills the `bastugatan` script
    """

    def execute(self, user_ids, args : str, say):

        if args != "!":
            say("Vill du verkligen stänga bastugatan? Kör `taskkill !` för att bekräfta")
            return

        say("STAAAAD")
        time.sleep(0.5)
        say("IIIIII")
        time.sleep(0.5)
        say("LJUUUUUUUS")
        time.sleep(2)

        say("Tack för denna gången, vi ses och hörs :crown:")

        print("-"*8+"\nClosing Bastugatan by order of admin\n"+"-"*8)
        os.kill(os.getpgrp(), signal.SIGTERM)

    def help(self):
        return "Stänger av bastugatan från remote. Används e.x. om du vill testa att köra koden lokalt"

    def description(self):
        return "Stänger bastugatan från remote"

    def __cmd__(self):
        return "taskkill"
