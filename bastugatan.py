from pynput import keyboard
import threading
import time
import sqlite3
from datetime import datetime, timedelta
import random
import os
import re

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient

from dotenv import load_dotenv

DEV = False

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

slack_client = WebClient(token=SLACK_BOT_TOKEN)
app = App(token=SLACK_BOT_TOKEN)

LAST_TRIGGER = None
pressed = set()

admin = os.getenv("ADMIN")


CHANNEL = os.getenv("DEV_CHANNEL") if DEV else os.getenv("DEV_CHANNEL")

keys = {keyboard.Key.ctrl_l, keyboard.Key.f8}

### GENERAL HELPER FUNCTIONS ###

def list_users(u: list[str]) -> str:
    """
    Given a list of users, return a formated string containing those users
    """
    return (random.choice(u) if len(u)==1
               else ", ".join(u[:-1]) + " och " + u[-1])

def deltagare(users: list[str]) -> str:
    """
    Given a list of users, return a formated string containing those users
    """
    return "" if len(users) == 0 else ("Deltagare: "+list_users(users))


def block_of(text: str) -> dict[str, any]:
    """
    Given a message, generate a `block` in accordance with SLACK BOT API
    """
    return {
        "type": "section",
        "text": {
        "type": "plain_text",
            "text": text
        }
    }

def get_message(users: list[str]) -> str:
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

def get_users() -> list[str]:
    """
    Get recently active users from the database
    """
    connection = sqlite3.connect("streck/streck.db")
    cursor = connection.cursor()

    try:
        thirty_minutes_ago = datetime.now() - timedelta(minutes=180) # 60 minutes + that sql is one hour behind python
        # added 60 extra making 180 due to summer time. Temp fix
        thirty_minutes_ago_str = thirty_minutes_ago.strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("SELECT name FROM Transactions JOIN Users U on user=U.id WHERE added >= ? GROUP BY name", (thirty_minutes_ago_str,))

        rows = cursor.fetchall()

        return [row[0] for row in rows if row[0] != "djinn"]

    except sqlite3.Error:
        print("Error fetching data from Users table:")
        return []

    finally:
        cursor.close()
        connection.close()


def send_message(message) -> None:
    """
    Post a given message to slack using the slack client
    """
    if isinstance(message, list):
        blocks = message
    else:
        blocks = [message]
    slack_client.chat_postMessage(channel=CHANNEL, blocks=blocks)

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
    users = get_users()
    print(users)
    if users == []:
        return
    reset_timer()
    text = get_message(users)
    send_message(text)

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
    print(pressed)
    if keys.issubset(pressed):
        pressed = set()
        on_click()

def on_release(key):
    """
    Listener function for keyboard key release
    """
    if key in pressed:
        pressed.remove(key)

##################################

### SLACK CONNECTION FUNCTIONS ###

@app.event("app_mention")
def handle_mention(*_):
    """
    Function to handle when the bot is mentioned @bastugatan
    """
    users = get_users()
    if users == []:
        send_message(block_of(b'Verkar inte va n\xc3\xa5n h\xc3\xa4r, men va fan vet jag'.decode('utf-8')))
    else:
        send_message(block_of(os.linesep.join([
            b'Bastugatan \xc3\xa4r \xc3\xb6ppen!'.decode('utf-8'),
            deltagare(users)
        ])))

@app.event("message")
def handle_message(event, say, _):
    pass

############

### MAIN ###

if __name__ == "__main__":
    keyboard_thread = threading.Thread(target=run_keyboard_listener)
    keyboard_thread.start()
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
