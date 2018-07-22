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
        response = "Sorry, I didnt get that. To begin survey reply play."

    return send_message(profile_id, response)

def get_response(recipient_id, message_received, message_received2=None):

	payload_id = message_received
	income = message_received2
	profile_id = recipient_id

	if payload_id == "start":
		response = "Ok lets begin. What is your age range?"
		answers = [QuickReply("18 - 30", "Q1 A"), QuickReply("31 - 60", "Q1 B")]
		get_response.newq = "q1"
	elif payload_id == "Q1 A":
		response = "Are you active in social media?"
		answers = [QuickReply("Yes", "Q2 A"), QuickReply("No", "Q2 B")]
		get_response.newq = "q1a"
	elif payload_id == "Q1 B":
		response = "Are you keen in social politics?"
		answers = [QuickReply("Yes", "Q2 A"), QuickReply("No", "Q2 B")]
		get_response.newq = "q1b"
	elif payload_id == "Q2 A" or payload_id == "Q2 B":
		response = "Will you be willing to test our products?"
		answers = [QuickReply("Yes", "Q3 A"), QuickReply("No", "Q3 B")]
		get_response.newq = "q2"
	elif payload_id == "Q3 A":
		response = "Whats your yearly income range?"
		answers = [QuickReply("30k - 100k", "Q4 A"), QuickReply("above 100k", "Q4 B")]
		get_response.newq = "q3a"
	elif payload_id == "Q3 B" or payload_id == "Q4 A" or payload_id == "Q4 B":
		# response = "Thank you for taking part. For more info visit below."
		answers = [GenericElement("Admin FB", "Thank you for taking part.", "https://www.facebook.com/testpageauto123/", "https://scontent.fkul13-1.fna.fbcdn.net/v/t1.0-9/36034614_180903916096270_6211548163522691072_n.jpg?_nc_cat=0&oh=a487fff7e3584a3305182f9aac9a460c&oe=5BA4A698", [ActionButton(ButtonType.WEB_URL, "Visit Page", "https://www.facebook.com/testpageauto123/")])]
		get_response.newq = None
		return send_generic(profile_id, answers)
	else:
		response = "Sorry, I didnt get that. For enquiries please contact below."
		answers = [ActionButton(ButtonType.WEB_URL, "Admin FB", "https://www.facebook.com/testpageauto123/")]
		return send_buttons(profile_id, response, answers)

	return send_quick_replies(profile_id, response, answers)

def sender_avoids(recipient_id, qnum):

	q_num = qnum
	response = None
	profile_id = recipient_id

	if q_num == 'q1':
		response = "Please choose one below"
		answers = [QuickReply("18 - 30", "Q1 A"), QuickReply("31 - 60", "Q1 B")]
	elif q_num == 'q1a':
		response = "Please choose one below"
		answers = [QuickReply("Yes", "Q2 A"), QuickReply("No", "Q2 B")]
	elif q_num == 'q1b':
		response = "Are you keen in social politics?"
		answers = [QuickReply("Yes", "Q2 A"), QuickReply("No", "Q2 B")]
	elif q_num == 'q2':
		response = "Will you be willing to test our products?"
		answers = [QuickReply("Yes", "Q3 A"), QuickReply("No", "Q3 B")]
	elif q_num == 'q3a':
		response = "Whats your yearly income range?"
		answers = [QuickReply("30k - 100k", "Q4 A"), QuickReply("above 100k", "Q4 B")]
	elif q_num == None:
		response = "How may I help you ?"
		answers = [QuickReply("30k - 100k", "Q4 A"), QuickReply("above 100k", "Q4 B")]

	return send_quick_replies(profile_id, response, answers)
