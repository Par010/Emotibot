import os
from env_vars import VERIFICATION_TOKEN_DEFAULT, IBM_WATSON_APIKEY_DEFAULT, DATABASE_URL_DEFAULT, \
    PAGE_ACCESS_TOKEN_DEFAULT


def get_env_variable(var_name, default=None):
    """Check if the var_name is in virtual environment or pass a default"""
    if var_name not in os.environ:
        os.environ[var_name] = default
    return os.environ[var_name]

VERIFICATION_TOKEN = get_env_variable('VERIFICATION_TOKEN', VERIFICATION_TOKEN_DEFAULT)
IBM_WATSON_VERSION = '2016-05-19'
IBM_WATSON_URL = 'https://gateway.watsonplatform.net/tone-analyzer/api'
IBM_WATSON_APIKEY = get_env_variable('IBM_WATSON_APIKEY', IBM_WATSON_APIKEY_DEFAULT)
DATABASE_URL = get_env_variable('DATABASE_URL', DATABASE_URL_DEFAULT)
# Number of minutes a message should remain relevant
MINUTES_FOR_A_CHAT_SESSION = 60
PAGE_ACCESS_TOKEN = get_env_variable('PAGE_ACCESS_TOKEN', PAGE_ACCESS_TOKEN_DEFAULT)
