from utils import wit_response
from method import *

def get_message(recipient_id, message_received):
    x = message_received.lower()
    profile_id = recipient_id
    response = None
    entity, value = wit_response(x)

    if entity == 'greetings':
        response = "Hi I'm bot nice to meet you"
    elif entity == 'location':
        response = "I see, I like {0} too".format(str(value))
    elif entity == 'fun' or value == 'play':
    	response = "Ok lets begin. What is your age range?"
    	answers = [QuickReply("18 - 30", "Q1 A"), QuickReply("31 - 60", "Q1 B")]
    	return send_quick_replies(profile_id, response, answers)
    else:
    	response = "Sorry, I didnt get that."

    if entity == None:
        response = "Sorry, I didnt get that."

    return response


