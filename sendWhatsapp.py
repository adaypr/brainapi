'''
Created on 10 sept. 2019

@author: WUIAPE03
'''
from twilio.rest import Client

def send_WhatsApp(to_whatsapp_number, from_whatsapp_number, text_to_send):
    # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
    client = Client()    
    client.messages.create(body=text_to_send,
                           from_=from_whatsapp_number,
                           to=to_whatsapp_number)