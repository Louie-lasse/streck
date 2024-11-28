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