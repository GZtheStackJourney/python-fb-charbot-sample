from utils import wit_response

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