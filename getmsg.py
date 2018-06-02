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

    if entity == None:
        response = "Sorry, I didnt get that."

    return send_message(profile_id, response)


def get_response(recipient_id, message_received):

	x = message_received

	if x == "Q1 A":
		response = "Are you active in social media?"
    	answers = [QuickReply("Yes", "Q2 A"), QuickReply("No", "Q2 B")]
    elif x == "Q1 B":
    	response = "Are you keen in social politics"
    	answers = [QuickReply("Yes", "Q2 A"), QuickReply("No", "Q2 B")]


    return send_quick_replies(profile_id, response, answers)