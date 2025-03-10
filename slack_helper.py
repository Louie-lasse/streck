import cv2



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

def capture_image(save_path="webcam_image.jpg", max_camera_range=2):
    """ Tries different camera indices and returns the first working one. """
    for i in range(max_camera_range):
        cap = cv2.VideoCapture(i)
        print(f"Checking {i}")
        if cap.isOpened():
            ret, frame = cap.read()  # Capture frame
            if ret:
                cv2.imwrite(save_path, frame)  # Save the image
            cap.release()
            return save_path if ret else None  # Return the working index
    return None  # No camera found

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
