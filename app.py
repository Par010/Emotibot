import sys
from flask import Flask, request

from constants import VERIFICATION_TOKEN

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
    return 'ok', 200


def log(message):
    # check the message JSON on terminal
    print(message)
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True, port=8000)
