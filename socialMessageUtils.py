import json

SLACK_CHANNEL_KEY = "slack_channel"

def addSlackChannel(slack_channel, message):    
    message[SLACK_CHANNEL_KEY] = slack_channel
    return message

def removeSlackChannel(message):    
    del message[SLACK_CHANNEL_KEY]
    return message

# def main():    
#     message = addSlackChannel("Roma Channel", {"temperature":"12.1"})
#     print(message)
#     message = removeSlackChannel(message)
#     print(message)
# main()