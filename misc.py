def strecka(user_id, product, say):
    """
    """
    connection = sqlite3.connect("streck/streck.db")
    cursor = connection.cursor()
    price = 0
    
    try:
        cursor.execute("Select price from products where id = ?", (product,))
        price = cursor.fetchall()[0][0]
    except sqlite3.Error as e:
        print(f"Error fetching price of {product} for {user_id}")
        print(e)
        say("Hmm, not gick fel. Pröva igen eller prata med IT-ansvarig")
    finally:
        cursor.close()
        connection.close()

    if price == 0:
        say("Hmm, not gick fel. Pröva igen eller prata med IT-ansvarig")
        return

    connection = sqlite3.connect("streck/streck.db")
    cursor = connection.cursor()    
    try:
        cursor.execute('Insert into transactionsets values (null, datetime("now", "-1 day"), ?, ?, ?, ?)', [known_users[user_id], product, price, ''])
        connection.commit()
        say("Har streckat :crown:")
    except sqlite3.Error as e:
        print(f"Error fetching price of {product} for {user_id}")
        print(e)
        say("Hmm, not gick fel. Pröva igen eller prata med IT-ansvarig")
    finally:
        cursor.close()
        connection.close()

@app.event("message")
def handle_message(event, say, _):
    if event["channel_type"] != "im":
        return
    user_id = event["user"]
    message = event["text"].lower()
    if user_id not in known_users:
        say(f"Hmm, du verkar inte vara inlagd. Skriv till <@{admin}> om du borde vara det")
        return
    if message == "öl":
        strecka(user_id, 30, say)
        return
    if message == "cider":
        strecka(user_id, 31, say)
        return
    if message == "läsk":
        strecka(user_id, 40, say)
        return
    if user_id == admin and "<@" in message:
        say(re.sub(r'<@([^>]+)>',r'\1',message))
        return
    say("Är du full eller? Förstår inte vad du säger, kan bara öl, cider, och läsk")

known_users = {
    "U069MKSRMQB" : 61,#Bärra
    "U081RUT1Y73" : 65, #pALLE
    "U0322K3C0CC" : 19,
    "U053HQP630D" : 59,
    "U04C67D9WS1" : 45,
    "U06LPUKE5J7" : 63,
    "U04R26B8VKR" : 56,
    "U06LHCZFBGE" : 62,
    "U011Z5DCBHC" : 5,
    "UHK8VNCS2"   : 6,
    "UTH3XVCSV"   : 2,
    "U02BKRVBHG9" : 4,
    "U02B46WJD7F" : 3,
    "U07207WSM7G" : 64,
    "UEJJT8Q84"   : 13
}