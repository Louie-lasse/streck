import os

import cv2
import tkinter as tk
import numpy as np

CALIBRATED = False

def send_dm(slack_client, user, message):
    """
    Sends a DM to the connected user to notify them of the connection.
    """
    try:
        response = slack_client.conversations_open(users=[user])

        channel_id = response["channel"]["id"]

        slack_client.chat_postMessage(
            channel=channel_id,
            text=message
        )
        return True
    except Exception as e:
        print(f"Failed to send DM to <@{user}>: {e}")
        return False

def get_profile_picture(slack_client, slack_id):
    """Fetch the user's profile picture URL from Slack."""
    response = slack_client.users_info(user=slack_id)
    if response["ok"]:
        profile = response["user"]["profile"]
        return profile.get("image_512")  # Use a medium resolution image
    return None

def send_message(slack_client, channel, message):
    """
    Post a given message to slack using the slack client
    """
    if isinstance(message, list):
        blocks = message
    else:
        blocks = [message]
    slack_client.chat_postMessage(channel=channel, blocks=blocks)

def block_of(text: str):
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

def capture_image(save_path="webcam_image.jpg", max_camera_range=2, countdown_steps=5):
    """ Tries different camera indices and returns the first working one. """
    for i in range(max_camera_range):
        cap = cv2.VideoCapture(i)
        print(f"Checking {i}")
        if cap.isOpened():
            if countdown_steps:
                countdown(countdown_steps)
            for i in range(15):
                ret, frame = cap.read()
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            avg_brightness = np.mean(gray)  # Get the average brightness

            if ret:
                if avg_brightness > 100:
                    frame = adjust_gamma(frame, 0.6)
                cv2.imwrite(save_path, frame)
            cap.release()
            return save_path if ret else None
    return None  # No camera found

def countdown(steps=5):
    """ Creates a floating countdown window using Tkinter. """
    root = tk.Tk()
    root.title("Countdown")
    root.attributes("-topmost", True)
    root.geometry("300x200")
    root.configure(bg="black")

    label = tk.Label(root, text="", font=("Helvetica", 48), fg="white", bg="black")
    label.pack(expand=True)

    def update_countdown(n):
        if n > 0:
            label.config(text=str(n))
            root.after(1000, update_countdown, n - 1)
        else:
            label.config(text="SMILE!")
            root.after(1000, root.destroy)

    update_countdown(steps)
    root.mainloop()

def upload_to_slack(image_path, slack_client, channel):
    response = slack_client.files_upload_v2(
        channels=channel,
        file=image_path,
        title="TKÖK",
    )
    return response

def send_webcam_image(slack_client, channel):
    image_path = capture_image()
    if not image_path:
        print("Failed to capture image")
        return
    upload_response = upload_to_slack(image_path, slack_client, channel)
    if not upload_response.get("ok"):
        print("Upload failed:", upload_response)

def adjust_gamma(image, gamma=0.5):
    """ Apply gamma correction to reduce brightness issues. """
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def calibrate():
    os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"
    cap = cv2.VideoCapture(0)

    for i in range(50):
        ret, frame = cap.read()
    cap.release()
    cv2.destroyAllWindows()

if not CALIBRATED:
    calibrate()
    CALIBRATED = True
