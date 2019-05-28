from flask import Flask, request
from pymessenger import Bot

import datetime

from constants import VERIFICATION_TOKEN, PAGE_ACCESS_TOKEN, HELP_TEXT
from analysis import tone_analysing, generate_response
from database import insert_update_msg_details


bot = Bot(PAGE_ACCESS_TOKEN)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    """Handles GET request sent by Facebook to verify token sent for callback URL Verification"""
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if not request.args.get('hub.verify_token') == VERIFICATION_TOKEN:
            return 'Verification Token incorrect', 403
        return request.args['hub.challenge'], 200
    return 'EmotiBot is Live!', 200


@app.route('/', methods=['POST'])
def webhook():
    """Handles POST request sent by facebook webhook, receives messages and handles them"""
    data = request.get_json()
    if data['object'] == 'page':
        for entry in data['entry']:
            for message in entry['messaging']:
                # extract sender_id from the message sent
                sender_id = message['sender']['id']
                # extract timestamp from the message sent and store in datetime UTC format
                timestamp = datetime.datetime.utcfromtimestamp(message['timestamp']/1000.0)
                if message.get('message'):
                    if 'text' in message['message']:
                        # check if text attribute is present in message
                        text_msg = message['message']['text']
                        if text_msg == 'help' or text_msg == 'Help':
                            # send help text
                            bot.send_text_message(sender_id, HELP_TEXT)
                            break
                        if text_msg == 'mood' or text_msg == 'Mood':
                            # if the sender asks for the bots mood,
                            #  check the current weighted_ratio and send the current mood
                            response = generate_response(sender_id)
                            bot.send_text_message(sender_id, response['mood'])
                            break
                    else:
                        text_msg = 'no text sent'
                    # analyse the sentence sent with the help of IBM Watson
                    mood = tone_analysing(text_msg)
                    # insert or update the message sent to the sender_id object
                    insert_update_msg_details(sender_id, timestamp, mood[0], mood[1])
                    # generate the appropriate response for the text_msg
                    response = generate_response(sender_id)
                    # send the response generated to the sender
                    bot.send_text_message(sender_id, response['response_text'])

    return 'ok', 200


if __name__ == '__main__':
    app.run(debug=True, port=8000)
