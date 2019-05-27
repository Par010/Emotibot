from flask import Flask

from .constants import VERIFICATION_TOKEN

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
