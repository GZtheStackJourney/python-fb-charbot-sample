import os
import sys
import json
import random
from utils import wit_response
from getmsg import get_message
from method import *
from datetime import datetime

import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        set_get_started_button_payload("get started")

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                
                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    
                    if messaging_event['message'].get('text'):
                        message_text = messaging_event["message"]["text"]  # the message's text
                        sample_reply = get_message(message_text) # sends the message's text to function to find
                        send_quick_replies(sender_id, sample_reply, [QuickReply("Type A", "Q1 A"), QuickReply("Type B", "Q1 B")])    
                    if messaging_event['message'].get('sticker_id'):
                        send_message(sender_id, "Hi I am a bot!")
                    if messaging_event['message'].get('attachments'):
                        send_message(sender_id, "Hi I am a bot!")
                        
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]

                    if messaging_event['postback'].get('payload'):
                        payload_text = messaging_event["postback"]["payload"]
                        if payload_text == "get started":
                            set_greeting_text(sender_id, "Welcome to my page, to begin reply play.")

    return "ok", 200
 



def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)
