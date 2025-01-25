import requests

from db_handler import DatabaseHandler
from slack_helper import get_profile_picture
from . import Command

class Update(Command):
    """
    Command for buying an item, specified in the constructor
    """

    def __init__(self, slack_client) -> None:
        super().__init__()
        self.db = DatabaseHandler()
        self.client = slack_client

    def execute(self, user_ids, args : str, say):
        image_url = get_profile_picture(self.client, user_ids["slack_id"])
        if not self._save_image_from_url(image_url, f'streck/pictures/users/{user_ids["name"]}.png'):
            say("Lyckades inte fixa bilden :pensive:")
            return

        self.db.save_image(user_ids["db_id"], f"{user_ids['name']}.png")
        say("Profilbilden borde vara fixad nu!")

    def _save_image_from_url(self, image_url, file_path):
        """Download and save the image from a URL."""
        try:
            response = requests.get(image_url, timeout=3)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
                    return True
        except Exception as e:
            print("Error downloading image:", e)
            return False
        
    def help(self):
        return """Uppdaterar din profilbild på streck appen till din nuvarande slack-profilbild"""
    
    def description(self):
        return "Uppdatera din profilbild"
    
    def __cmd__(self):
        return "update"
