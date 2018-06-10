import os
import sys
import json
import random
from utils import wit_response
from getmsg import get_message, get_response
from method import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

import requests
from flask import Flask, request

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    qnum = db.Column(db.String(80))

    def __init__(self, name, qnum):
        self.name = name
        self.qnum = qnum

    def __repr__(self):
        return '<Name %r>' % self.name

db.create_all()
db.session.commit()

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
        set_greeting_text("Welcome!")
        set_get_started_button_payload("get started")


    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID

                    #query the db about the id, if no create a new one
                    check_user = User.query.filter_by(name=sender_id).first()
                    if not (check_User is None) {
                        get_q = check_user.qnum
                    }else {
                        new_user = User(sender_id, 'q1')
                        db.session.add(new_user)
                        db.session.commit()
                    }
                    #if there is an id add to variable, query which question the id is at and add to an variable
                    #update data base by variable and use dot syntax to alter the value.
                    
                    if messaging_event['message'].get('quick_reply'):
                        message_text = messaging_event["message"]["quick_reply"]["payload"]
                        message_text2 = messaging_event["message"]["text"]
                        get_response(sender_id, message_text, message_text2)
                    elif messaging_event['message'].get('text'):
                        message_text = messaging_event["message"]["text"]  # the message's text
                        get_message(sender_id, message_text) # sends the message's text to function to find
                    if messaging_event['message'].get('sticker_id'):
                        pass
                    if messaging_event['message'].get('attachments'):
                        pass

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
                            send_message(sender_id, "Hi, welcome to my page, to begin reply play.")

    return "ok", 200
 

#add recipient id and payload to qnum to database
#if no id create in db, create new id



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
