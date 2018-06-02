from utils import wit_response
from method import *

def get_message(message_received):
    x = message_received.lower()
    response = None
    entity, value = wit_response(x)

    if entity == 'greetings':
        response = "Hi I'm bot nice to meet you"
    elif entity == 'location':
        response = "I see, I like {0} too".format(str(value))
    elif entity == 'fun' or value == 'play':
    	response = "Ok lets begin. What is your age range?"
    	answers = [QuickReply("18 - 30", "Q1 A"), QuickReply("31 - 60", "Q1 B")]
    	return send_quick_replies(recipient_id, response, answers)

    if entity == None:
        response = "Sorry, I didnt get that."

    return response


