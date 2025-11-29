from ..command import Command
import os
import subprocess

class SSH(Command):


    def __init__(self):
        self.ts_url = "https://login.tailscale.com/admin/invite/"
        self.link_key = os.environ.get("TAILSCALE_LINK_ID")
        self.exists = self.link_key is not None and self._tailscale_is_running()

    def _tailscale_is_running(self):
        try:
            result = subprocess.run(
                ["tailscale", "status"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    
    def execute(self, user_ids, args, say):
        if not self.exists:
            say("Något verkar vara fel med tailscale.")
            return
        say("\n".join([
            "För att ansluta till servern via SSH, kör `ssh remote@raspberrypi`",
            "Lösenorder finns på drive."
            f"Om något strular, kör `{self.__cmd__()} help` för mer info."
            f"För att gå med i Tailscale-nätverket, använd länken: {self.ts_url}{self.link_key}"
        ]))
    
    def help(self):
        return "\n".join([
            "Här kan du koppla till bastugatan via SSH, och köra kommandon direkt."
            "Håll inte på här om du inte vet vad du gör!",
            "För att ansluta behöver du först skaffa tailscale, och gå med i nätverket via länken",
            f"{self.ts_url}{self.link_key}",
            "När du är ansluten kan du köra `ssh remote@raspberrypi` för att ansluta till servern.",
            "Lösenord finns på drive.",
            "Väl inne kan du komma åt databasen `sqlite3 adressen/till/databasen.db`",
            "Starta om allt `reboot`",
            "Och lite vad du vill"
        ])
    
    def description(self):
        return "Koppla till bastugatan via SSH."
    
    def __cmd__(self):
        return "ssh"
