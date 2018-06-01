import os
import sys
import json
import random
from utils import wit_response
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
                        quick_replies(sender_id, sample_reply)    
                    if messaging_event['message'].get('sticker_id'):
                        send_message(sender_id, "Hi I am a bot!")
                    if messaging_event['message'].get('attachments'):
                        send_message(sender_id, "Hi I am a bot!")
                        
                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


# def send_message(recipient_id, message_text):

#     log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

#     params = {
#         "access_token": os.environ["PAGE_ACCESS_TOKEN"]
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "text": message_text
#         }
#     })
#     r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
#     if r.status_code != 200:
#         log(r.status_code)
#         log(r.text)

# def quick_replies(recipient_id, message_text):

#     log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

#     params = {
#         "access_token": os.environ["PAGE_ACCESS_TOKEN"]
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "text": message_text,
#             "quick_replies":[
#               {
#                 "content_type":"text",
#                 "title":"Type A",
#                 "payload":"<POSTBACK_PAYLOAD>",
#                 "image_url":"http://example.com/img/red.png"
#               },
#               {
#                 "content_type":"location"
#               }
#             ]
#         }
#     })

#     r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
#     if r.status_code != 200:
#         log(r.status_code)
#         log(r.text)




def get_message(message_received):
    x = message_received.lower()
    response = None
    entity, value = wit_response(x)

    if entity == 'greetings':
        response = "Hi I'm bot nice to meet you"
    elif entity == 'location':
        response = "I see, I like {0} too".format(str(value))

    if entity == None:
        response = "Sorry, I didnt get that."

    return response
    
##    bot_reply = ["hello, Im bot. to begin reply start", "Good day, Im bot. reply start to begin"]
##    intro_text = ['hello', 'hi', 'how are you']
##    start_text = ['start', 'begin']
##    agree_text = ['yes', 'yeah']
##    disagree_text = ['no', 'nah']
##    if any(w in x for w in intro_text):
##        bot_reply = ["Hi im bot! to begin reply start", "Hi, to begin reply start"]
##    elif any(w in x for w in start_text):
##        bot_reply = ["Lets Begin? reply yes or no only.", "Beginning.. reply yes or no only."]
##    elif any(w in x for w in agree_text):
##        bot_reply = ["Game Starting...", "Starting"]
##    elif any(w in x for w in disagree_text):
##        bot_reply = ["Exiting.. Thank you.", "Exiting.."]
##    else:
##        bot_reply
##
##    return random.choice(bot_reply)
    
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
