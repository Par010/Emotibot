import sys
from flask import Flask, request

import datetime


from constants import VERIFICATION_TOKEN
from analysis import tone_analysing
from database import insert_update_msg_details

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
    log(data)
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
                    else:
                        text_msg = 'no text sent'
                    mood = tone_analysing(text_msg)
                    print(sender_id, timestamp, mood)
                    insert_update_msg_details(sender_id, timestamp, mood[0], mood[1])

    return 'ok', 200


def log(message):
    # check the message JSON on terminal
    print(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True, port=8000)
