##import sys
##sys.path.append("C:\\Users\\Liew\\Envs\\test_bot\\Lib\\site-packages")
from wit import Wit

access_token = "MWROYP2YAJFA2VQSKB5SHGR3PMJUP5G3"

client = Wit(access_token = access_token)

def wit_response(message_text):
    resp = client.message(message_text)
    categories = {'greetings':None, 'location':None}
    ##extract name and value of entity

    entities = list(resp['entities'])
    
    for entity in entities:
        categories[entity] = resp['entities'][entity][0]['value']
        
    return categories

def send_generic_message(self, recipient_id, elements, notification_type=NotificationType.regular):
        """Send generic messages to the specified recipient.
        https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template
        Input:
            recipient_id: recipient id to send to
            elements: generic message elements to send
        Output:
            Response from API as <dict>
        """
        return self.send_message(recipient_id, {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            }
        }, notification_type)

def get_reply(categories):

    if categories['greetings'] != None:

        element = {
                'title': 'Hello'
                'buttons': [{
                    'type': 'web_url',
                    'title': "Read More",
                    'url': '#'
                        }],
                }

    return element
    
    
##print(wit_response("I live in Malaysia"))


