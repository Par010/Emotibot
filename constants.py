from env_vars import VERIFICATION_TOKEN_DEFAULT, IBM_WATSON_APIKEY_DEFAULT, DATABASE_URL_DEFAULT, \
    PAGE_ACCESS_TOKEN_DEFAULT
from helpers import get_env_variable


VERIFICATION_TOKEN = get_env_variable('VERIFICATION_TOKEN', VERIFICATION_TOKEN_DEFAULT)
IBM_WATSON_VERSION = '2016-05-19'
IBM_WATSON_URL = 'https://gateway.watsonplatform.net/tone-analyzer/api'
IBM_WATSON_APIKEY = get_env_variable('IBM_WATSON_APIKEY', IBM_WATSON_APIKEY_DEFAULT)
DATABASE_URL = get_env_variable('DATABASE_URL', DATABASE_URL_DEFAULT)
# Number of minutes a message should remain relevant
MINUTES_FOR_A_CHAT_SESSION = 60
PAGE_ACCESS_TOKEN = get_env_variable('PAGE_ACCESS_TOKEN', PAGE_ACCESS_TOKEN_DEFAULT)
HELP_TEXT = "Hi there! I'm an emotion bot, whatever you say makes me feel things " \
            "and changes my mood, I'm here for you, talk to me as long as you want." \
            " You can \n\n 1. Vent as much you want! \n 2. Type 'mood' to check my mood"
SCHEDULED_HOURS = 2
