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


def get_response(recipient_id, message_received, message_received2=None):

	x = message_received
	income = message_received2
	profile_id = recipient_id

	if x == "Q1 A":
		response = "Are you active in social media?"
		answers = [QuickReply("Yes", "Q2 A"), QuickReply("No", "Q2 B")]
	elif x == "Q1 B":
		response = "Are you keen in social politics?"
		answers = [QuickReply("Yes", "Q2 A"), QuickReply("No", "Q2 B")]
	elif x == "Q2 A" or x == "Q2 B":
		response = "Will you be willing to test our products?"
		answers = [QuickReply("Yes", "Q3 A"), QuickReply("No", "Q3 B")]
	elif x == "Q3 A":
		response = "Whats your yearly income range?"
		answers = [QuickReply("30k - 100k", "Q4 A"), QuickReply("above 100k", "Q4 B")]
	elif x == "Q3 B":
		response = "Thank you for taking part. For more info visit below."
		answers = [ActionButton(ButtonType.WEB_URL, "Admin FB", "https://www.facebook.com/testpageauto123/")]
		return send_buttons(profile_id, response, answers)
	else:
		response = "Sorry, I didnt get that."
		return send_message(profile_id, response)

	return send_quick_replies(profile_id, response, answers)