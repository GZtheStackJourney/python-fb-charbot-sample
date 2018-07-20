import os
import sys
import json
import random
import time
from utils import wit_response
from getmsg import get_message, get_response, sender_avoids
from method import *
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

import requests
from flask import Flask, request

# https://cryptic-refuge-79635.herokuapp.com/
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
		# set_get_started_button_payload("get started")
		set_greeting_text("Welcome!")
		set_get_started_menu("get started")
		# set_persistent_menu("start")

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":
        # remove_persistent_menu()
        # set_persistent_menu("start")

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message

                    sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    typing(sender_id)
                    time.sleep(2)
                    #query the db about the id, if no create a new one
                    check_user = User.query.filter_by(name=sender_id).first()
                    if not (check_user is None):
                        get_q = check_user.qnum
                        print get_q
                    else:
                        print check_user
                        new_user = User(sender_id, None)
                        db.session.add(new_user)
                        db.session.commit()
                        
                    #if there is an id add to variable, query which question the id is at and add to an variable
                    #update data base by variable and use dot syntax to alter the value.
                    
                    if messaging_event['message'].get('quick_reply'):
                        message_text = messaging_event["message"]["quick_reply"]["payload"]
                        message_text2 = messaging_event["message"]["text"]
                        get_response(sender_id, message_text, message_text2)
                        print(get_response.newq)
                        current_user = User.query.filter_by(name=sender_id).first()
                        current_user.qnum = get_response.newq #update database
                        db.session.commit()
                    elif messaging_event['message'].get('text'):
                        message_text = messaging_event["message"]["text"]  # the message's text
                        ## if new_user.qnum is not an empty string then sender_avoids() else below
                        if not (get_q is None):
                            sender_avoids(sender_id, get_q)
                        else:
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
                            send_message(sender_id, "Hi, welcome to my page, you can chat with me or select Do Survey below")
                        elif payload_text == "start":
                            send_quick_replies(sender_id, "Ok lets begin. What is your age range?", [QuickReply("18 - 30", "Q1 A"), QuickReply("31 - 60", "Q1 B")])
                        elif payload_text == "SHOW_TEMPLATES":
                        	answers = [GenericElement("Admin FB", "Thank you for taking part.", "https://www.facebook.com/testpageauto123/", "https://scontent.fkul13-1.fna.fbcdn.net/v/t1.0-9/36034614_180903916096270_6211548163522691072_n.jpg?_nc_cat=0&oh=a487fff7e3584a3305182f9aac9a460c&oe=5BA4A698", [ActionButton(ButtonType.WEB_URL, "Visit Page", "https://www.facebook.com/testpageauto123/"), ActionButton(ButtonType.POSTBACK, "Random Image", None, "image")]), 
                        	GenericElement("LYL", "Yi Ling", "https://www.facebook.com/ylprudentialinsurance", "https://scontent.fkul13-1.fna.fbcdn.net/v/t1.0-9/29573382_1197007067102233_5848571075711617259_n.jpg?_nc_cat=0&oh=d4a5fed2bfee272ee6a45996f4103729&oe=5BEC8558", [ActionButton(ButtonType.WEB_URL, "Message Yi Ling", "https://www.messenger.com/t/ylprudentialinsurance")]), 
                        	GenericElement("LYT", "Yi Ting", "https://www.facebook.com/ivyliewprudentialagent/", "https://scontent.fkul13-1.fna.fbcdn.net/v/t1.0-9/28378087_1091917300948186_3375192295121555330_n.png?_nc_cat=0&_nc_eui2=AeFAAHgrRzYZ1ElQ9KolpooPp4w9w4r5dkxqh270E3dXeHRhEuvS5X0LPdVwBzadrybfEDXNchy4wK1hpGSmBo9qMmedozsTW_guXI71LDgZag&oh=f5fd32c9ca3f708e497a6ba655ef78c8&oe=5BAF3C11", [ActionButton(ButtonType.WEB_URL, "Visit Page", "https://www.facebook.com/ivyliewprudentialagent/")])]
                        	send_generic(sender_id, answers)
                        elif payload_text == "image":
                        	send_image(sender_id, "https://unsplash.it/400/600/?random")

# SHOW_TEMPLATES

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
