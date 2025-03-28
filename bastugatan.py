import threading
import time
import random
import os
import re

from pynput import keyboard

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient

from dotenv import load_dotenv

load_dotenv()

from db_handler import DatabaseHandler
from commands import *
from slack_helper import send_dm, send_message, block_of, send_webcam_image

DEV = bool(os.getenv("DEV"))

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

slack_client = WebClient(token=SLACK_BOT_TOKEN)
app = App(token=SLACK_BOT_TOKEN)

LAST_TRIGGER = None
pressed = set()

ADMIN = os.getenv("ADMIN")


CHANNEL = os.getenv("DEV_CHANNEL") if DEV else os.getenv("PROD_CHANNEL")

keys = {keyboard.Key.ctrl_l, keyboard.Key.f8}

db = DatabaseHandler()

### GENERAL HELPER FUNCTIONS ###

def list_users(u):
    """
    Given a list of users, return a formated string containing those users
    """
    return (random.choice(u) if len(u)==1
               else ", ".join(u[:-1]) + " och " + u[-1])

def deltagare(users):
    """
    Given a list of users, return a formated string containing those users
    """
    return "" if len(users) == 0 else ("Deltagare: "+list_users(users))

def get_message(users):
    """
    Given a list of users, generate a random message
    """
    nullary = [
        lambda users : block_of(os.linesep.join([
            b'Sjukt drag p\xc3\xa5 rummet, skit i plugget och kom hit o \xc3\xb6la!'.decode('utf-8'),
            deltagare(users)])
        ),
        lambda users : [
            block_of(os.linesep.join(["Kom hit!",
                                        deltagare(users)
            ])),
            {
                "type": "image",
                "title": {
                    "type": "plain_text",
                    "text": b'Kr\xc3\xb6k! H\xc3\xa4r!'.decode('utf-8')
                },
                "image_url": "https://files.slack.com/files-pri/T1B9F6UJJ-F06L3D7P547/krok_har.gif",
                "alt_text": "RandomGif alt text"
            }
        ],
        lambda users : block_of(os.linesep.join([
            b'Kr\xc3\xb6kdags!'.decode('utf-8'),
            deltagare(users)])
        ),
    ]
    nary = [
        lambda users : block_of(os.linesep.join([
                    "Come to rummet, we've got:",
                    b'Kr\xc3\xb6k :sunglasses:'.decode('utf-8'),
                    list_users(users) + " :avverka:",
                    b'Mer kr\xc3\xb6k :skull:'.decode('utf-8')
                ])
        ),
        lambda users : block_of(b'Kr\xc3\xb6ka p\xc3\xa5 rummet med '.decode('utf-8')
                        + list_users(users)
                        + b'. Det blir en kv\xc3\xa4ll att (f\xc3\xb6rs\xc3\xb6ka) minnas!'.decode('utf-8')
        ),
    ]
    if users == []:
        return random.choice(nullary)([])
    return random.choice(nullary + nary)(users)

############################

### KEY/BUTTON FUNCTIONS ###

def reset_timer():
    """
    Helper function for resetting the `last_trigger` global timer
    """
    global LAST_TRIGGER
    LAST_TRIGGER = time.time()

def trigger_web_hook():
    """
    Function for sending formated list of acive members on slack
    """
    users = db.get_recent_users()
    if users == []:
        return
    users = [u[0] for u in users]
    print(users)
    
    reset_timer()
    text = get_message(users)
    send_message(slack_client, CHANNEL, text)
    send_webcam_image(slack_client, CHANNEL)

def on_click():
    """
    Function for handeling when the correct key-combination is pressed.
    """
    if DEV or LAST_TRIGGER is None or (time.time() - LAST_TRIGGER) / 60 >= 30:
        trigger_web_hook()

def run_keyboard_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def on_press(key):
    """
    Listener function for keyboard presses
    """
    global pressed
    pressed.add(key)
    if keys.issubset(pressed):
        pressed = set()
        on_click()

def on_release(key):
    """
    Listener function for keyboard key release
    """
    if key in pressed:
        pressed.remove(key)

#####################

### CLI FUNCTIONS ###

user_command_registry = Command_registry()
user_command_registry.add(Beer())
user_command_registry.add(Cider())
user_command_registry.add(Soda())
user_command_registry.add(Update(slack_client))
user_command_registry.add(Skuld())
user_command_registry.add(Whoami())
user_command_registry.add(Request(slack_client))

admin_command_registry = Command_registry()
admin_command_registry.add(List_Users())
admin_command_registry.add(Connect(slack_client))
admin_command_registry.add(Disconnect(slack_client))
admin_command_registry.add(Strecklista(slack_client))
admin_command_registry.add(Who_Is())
admin_command_registry.add(Say(slack_client, CHANNEL))
admin_command_registry.add(Where_Is())
admin_command_registry.add(Add(slack_client))
admin_command_registry.add(TaskKill())

all_commands = user_command_registry.merge(admin_command_registry)

def handle_help(command_registry, arg: str, say):
    """
    Provide `help` info to the user
    """
    if len(arg) < 1:
        say(f"""
Självklart! Här kommer en lista av saker du kan göra.
Du kan också skriva `help <command>` för mer info om ett kommand:
{command_registry}
"""
        )
        return

    if arg in command_registry:
        say(command_registry[arg].help())
    else:
        say(f"Fattar inte vad du menar med {arg}?!\nPröva `help` om du behöver")

def user_not_connected(say, command, user_id):
    """
    Handles the case where a user is not connected.
    The execution should halt after this as most commands depend on this feature.
    """
    if command == "connect_me":
        say(f"Gott. Har skickat ett medelande till <@{ADMIN}> och bett dom lägga till dig")
        send_dm(
            slack_client,
            ADMIN,
            f"User <@{user_id}> wants to connect to slack. Do so using the `connect` command. Type `help` or `help connect` for more info"
        )
    elif command=="whoami":
        say(user_id)
    else:
        say("Du verkar inte vara uppkopplad till slack. För att koppla upp dig, skicka `connect_me`")
    return

##################################

### SLACK CONNECTION FUNCTIONS ###

@app.event("app_mention")
def handle_mention(event, say, *_):
    """
    Function to handle when the bot is mentioned @bastugatan
    """
    if event["channel"] != CHANNEL:
        say(f"Jag svarar tyvärr bara i <#{CHANNEL}>")
        return
    users = db.get_recent_users()
    users = [u[0] for u in users]
    if users == []:
        send_message(
            slack_client,
            CHANNEL,
            block_of(b'Verkar inte va n\xc3\xa5n h\xc3\xa4r, men va fan vet jag'.decode('utf-8'))
            )
    else:
        send_message(
            slack_client,
            CHANNEL,
            block_of(os.linesep.join([
                b'Bastugatan \xc3\xa4r \xc3\xb6ppen!'.decode('utf-8'),
                deltagare(users)
        ])))

@app.event("message")
def handle_message(event, say, *_):
    """Main function to handle incoming Slack messages."""

    user_id = event["user"]
    db_id, name = db.get_user(user_id)
    user_input = event["text"].strip()

    parts = user_input.split(" ", 1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if event["channel_type"] != "im":
        # ignore messages not in DM
        if event["channel"] == CHANNEL:
            if command == "öl":
                u_message = "Ruffe ditt fyllo! " if user_id=="U04R26B8VKR" else ""
                say(f"{u_message}Vi tar det i DM :kissing_heart:")
        return

    if db_id is None:
        user_not_connected(say, command, user_id)
        return

    command_registry = (
        all_commands
        if user_id == ADMIN
        else user_command_registry
    )

    if command == "help":
        handle_help(command_registry, args, say)
        return
    if command in command_registry:
        command_registry[command].execute({
            "slack_id": user_id,
            "db_id": db_id,
            "name": name
        }, args, say)
    else:
        say("Fattar inte vad du menar. Kan fixa öl, cider och läsk, annars kan du ju skriva `help` om det behövs")

############

### MAIN ###

if __name__ == "__main__":
    keyboard_thread = threading.Thread(target=run_keyboard_listener)
    keyboard_thread.start()
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
