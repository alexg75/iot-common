import logger
import json

ACCESS_TOKEN = "access_token"
REFRESH_TOKEN = "refresh_token"
TOKEN_FILE = "./token.json"
TOPIC_NAME = 'slack-token'

log = logger.setup_logger("iot-common")

def load_stored_token():
    token_dict = {}
    try:        
        json_file = open(TOKEN_FILE, "r")        
        token_dict = json.load(json_file)
        log.info(f"TOKEN LOADED: {token_dict}")
    except Exception as e:
        log.error("Could not load stored token")
        log.error(e)
    return token_dict

def save_tokens(token_dict):
    try:
        with open(TOKEN_FILE, "w") as outfile:
            json.dump(token_dict, outfile)
    except:
        log.error("Could not save token")