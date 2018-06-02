import os
import sys
import json
import random
from utils import wit_response
from datetime import datetime
from enum import Enum
import logging

import requests
from flask import Flask, request


ATTACHMENT_FIELD = "attachment"
TYPE_FIELD = "type"
TEMPLATE_TYPE_FIELD = "template_type"
TEXT_FIELD = "text"
TITLE_FIELD = "title"
SUBTITLE_FIELD = "subtitle"
IMAGE_FIELD = "image_url"
BUTTONS_FIELD = "buttons"
PAYLOAD_FIELD = "payload"
URL_FIELD = "url"
ELEMENTS_FIELD = "elements"
QUICK_REPLIES_FIELD = "quick_replies"
CONTENT_TYPE_FIELD = "content_type"

# received message fields
POSTBACK_FIELD = "postback"

class ContentType(Enum):
    TEXT = "text"
    LOCATION = "location"

class QuickReply:
    def __init__(self, title, payload,
                 image_url=None,
                 content_type=ContentType.TEXT):
        self.title = title
        self.payload = payload
        self.image_url = image_url
        self.content_type = content_type

    def to_dict(self):
        reply_dict = {CONTENT_TYPE_FIELD: self.content_type.value,
                      PAYLOAD_FIELD: self.payload}
        if self.title:
            reply_dict[TITLE_FIELD] = self.title
        if self.image_url:
            reply_dict[IMAGE_FIELD] = self.image_url
        log(reply_dict)
        return reply_dict

def set_get_started_button_payload(payload):
	    params = {
	        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
	    }
	    headers = {
	        "Content-Type": "application/json"
	    }
	    data = json.dumps({
	    		"setting_type": "call_to_actions",
                "thread_state": "new_thread",
                "call_to_actions": [{"payload": payload}]


	            })

	    r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=data)
	    if r.status_code != 200:
	        log(r.status_code)
	        log(r.text)

def set_greeting_text(message_text):

        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }
        data = json.dumps({
                "setting_type": "greeting",
                "greeting": {"text": message_text}
                })

        r = requests.post("https://graph.facebook.com/v2.6/me/thread_settings", params=params, headers=headers, data=data)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def quick_replies(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text,
            "quick_replies":[
              {
                "content_type":"text",
                "title":"Type A",
                "payload":"<POSTBACK_PAYLOAD>",
                # "image_url":"http://example.com/img/red.png"
              },
              {
                "content_type":"text",
                "title":"Type B",
                "payload":"<POSTBACK_PAYLOAD>",
              }
            ]
        }
    })

    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_quick_replies(recipient_id, message_text, reply_list):
        log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

        params = {
            "access_token": os.environ["PAGE_ACCESS_TOKEN"]
        }
        headers = {
            "Content-Type": "application/json"
        }
        replies = list(dict())
        for r in reply_list:
            replies.append(r.to_dict())
        data = json.dumps({
        "recipient": {
                        "id": recipient_id
                    },
                    "message": {
                        "text": message_text,
                        "quick_replies": replies
                    }
        })

        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            log(r.status_code)
            log(r.text)



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